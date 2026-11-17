#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主动关怀触发（M6）——决定「该不该主动开口」

方案 4.3 的难点不在话术，在于**时机与分寸**。三道闸门，缺一不可：
1. 冷却：距上次主动关怀不足 N 小时，不打扰
2. 静默：深夜/凌晨时段一律不主动（数据主权 > 存在感）
3. 频次：每日上限，超了当天不再触发

信号来源（全部本地，零外部依赖）：
- 久未联系：用户信号的最后时间戳
- 情绪低谷：最近若干条信号里的负面情绪占比
- 纪念日：记忆库「里程碑」类目下带日期的条目
- 深夜：当前时段

⚠️ 已知约束：本模块只做**判定与话术生成**，是否真的发出去取决于 IM 通道
是否支持主动消息。通道不支持时，退化为「下次对话开头带一句」。
"""

import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 允许 `python scripts/care/trigger.py` 直接跑（此时 sys.path[0] 是脚本所在目录）
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.core import settings as core_settings  # noqa: E402
from scripts.core.storage import read_json, write_json  # noqa: E402

DEFAULT_CONFIG: Dict[str, Any] = {
    "开关": True,
    "冷却小时": 6,        # 两次主动关怀的最小间隔
    "每日上限": 2,        # 每天最多主动几次
    "静默时段": [0, 1, 2, 3, 4, 5, 6, 7],   # 这些整点不主动说话
    "久未联系小时": 10,   # 超过这么久没互动，判定为「该关心一下」
    "负面情绪阈值": 0.4,  # 最近 10 条里负面占比超过它，判定情绪低谷
    "深夜起始": 22,       # 22 点之后算深夜，触发晚安类关怀
}

NEGATIVE_EMOTIONS = ("疲惫", "低落", "焦虑", "生气")

# 日期识别：2026-05-20 / 2026/5/20 / 5月20日 / 5-20
_DATE_RE = re.compile(r"(?:(\d{4})\s*[-/年]\s*)?(\d{1,2})\s*[-/月]\s*(\d{1,2})\s*日?")


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _parse_ts(ts: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(str(ts))
    except (TypeError, ValueError):
        return None


class CareTrigger:
    """主动关怀触发判定"""

    def __init__(self, data_dir: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        self.data_dir = core_settings.resolve_data_dir(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.data_dir / "care_state.json"
        self.config = dict(DEFAULT_CONFIG)
        if config:
            self.config.update(config)

    # ---------- 状态 ----------

    _DEFAULT_STATE = {"last_care_at": None, "day": None, "count": 0, "history": []}

    def _load_state(self) -> Dict[str, Any]:
        data = read_json(self.state_file, dict(self._DEFAULT_STATE))
        return data if isinstance(data, dict) else dict(self._DEFAULT_STATE)

    def _save_state(self, state: Dict[str, Any]) -> None:
        write_json(self.state_file, state)

    def mark_sent(self, kind: str, now: Optional[datetime] = None) -> Dict[str, Any]:
        """关怀已发出，更新冷却与当日计数"""
        now = now or datetime.now()
        state = self._load_state()
        today = now.strftime("%Y-%m-%d")
        if state.get("day") != today:
            state["day"], state["count"] = today, 0
        state["last_care_at"] = now.isoformat(timespec="seconds")
        state["count"] = int(state.get("count", 0)) + 1
        state.setdefault("history", []).append({"ts": state["last_care_at"], "kind": kind})
        state["history"] = state["history"][-100:]
        self._save_state(state)
        return state

    # ---------- 信号 ----------

    def _user_signals(self) -> List[Dict[str, Any]]:
        data = read_json(self.data_dir / "user_signals.json", [])
        return data if isinstance(data, list) else []

    def hours_since_contact(self, now: Optional[datetime] = None) -> Optional[float]:
        """距用户最后一次发言多少小时；无信号返回 None"""
        now = now or datetime.now()
        signals = self._user_signals()
        if not signals:
            return None
        last = _parse_ts(signals[-1].get("ts", ""))
        if last is None:
            return None
        return round(max(0.0, (now - last).total_seconds() / 3600.0), 2)

    def negative_ratio(self, window: int = 10) -> float:
        """最近 window 条信号里负面情绪占比"""
        signals = self._user_signals()[-window:]
        if not signals:
            return 0.0
        bad = sum(1 for s in signals if (s.get("emotion") or "") in NEGATIVE_EMOTIONS)
        return round(bad / len(signals), 3)

    def milestone_today(self, now: Optional[datetime] = None) -> Optional[str]:
        """今天是否有纪念日（来自记忆库「里程碑」条目）"""
        now = now or datetime.now()
        from scripts.memory.store import MemoryStore
        entries = MemoryStore(str(self.data_dir)).by_type("里程碑")
        for e in entries:
            for m in _DATE_RE.finditer(str(e.get("content", ""))):
                year, month, day = m.group(1), int(m.group(2)), int(m.group(3))
                if month == now.month and day == now.day:
                    return str(e.get("content", ""))
                _ = year      # 带年份的条目：同年同月日算命中；跨年则按月日算周年
        return None

    # ---------- 闸门 ----------

    def _gates(self, now: datetime) -> Tuple[bool, str]:
        """三道闸门，返回 (是否放行, 拦截原因)"""
        if not self.config.get("开关", True):
            return False, "关怀开关已关闭"

        if now.hour in (self.config.get("静默时段") or []):
            return False, f"静默时段（{now.hour} 点）"

        state = self._load_state()
        today = now.strftime("%Y-%m-%d")
        if state.get("day") == today and int(state.get("count", 0)) >= int(self.config["每日上限"]):
            return False, f"今日已达上限（{self.config['每日上限']} 次）"

        last = _parse_ts(state.get("last_care_at") or "")
        if last is not None:
            elapsed = (now - last).total_seconds() / 3600.0
            if elapsed < float(self.config["冷却小时"]):
                return False, f"冷却中（还需 {self.config['冷却小时'] - elapsed:.1f} 小时）"

        return True, ""

    # ---------- 判定 ----------

    def evaluate(self, now: Optional[datetime] = None) -> Dict[str, Any]:
        """综合判定现在是否该主动关怀

        Returns:
            {"should": bool, "kind": str|None, "reason": str, "next_hint": str}
            kind ∈ 低落陪伴 / 纪念日 / 深夜晚安 / 久未联系
        """
        now = now or datetime.now()

        # 用户明确不喜欢主动 → 直接不打扰（数据主权优先）
        try:
            from scripts.user.profile import UserProfileStore
            pref = (UserProfileStore(str(self.data_dir)).get().get("互动偏好") or {}).get("主动程度偏好")
        except Exception:  # noqa: BLE001 - 画像读取失败不得阻塞关怀判定
            pref = None
        if pref == "低":
            return {"should": False, "kind": None, "reason": "用户主动程度偏好为低", "next_hint": ""}

        ok, why = self._gates(now)
        if not ok:
            return {"should": False, "kind": None, "reason": why, "next_hint": ""}

        # 按优先级选信号：情绪低谷 > 纪念日 > 深夜 > 久未联系
        if self.negative_ratio() >= float(self.config["负面情绪阈值"]):
            return {"should": True, "kind": "低落陪伴",
                    "reason": f"负面情绪占比 {self.negative_ratio()}", "next_hint": "别追问原因，先陪着"}

        milestone = self.milestone_today(now)
        if milestone:
            return {"should": True, "kind": "纪念日", "reason": milestone, "next_hint": "提具体的事，别空泛祝贺"}

        if now.hour >= int(self.config["深夜起始"]):
            return {"should": True, "kind": "深夜晚安", "reason": f"已过 {self.config['深夜起始']} 点",
                    "next_hint": "简短，不要开启新话题"}

        idle = self.hours_since_contact(now)
        if idle is not None and idle >= float(self.config["久未联系小时"]):
            return {"should": True, "kind": "久未联系", "reason": f"已 {idle:.1f} 小时没说话",
                    "next_hint": "轻描淡写地出现，不要兴师问罪"}

        return {"should": False, "kind": None, "reason": "无触发信号", "next_hint": ""}

    def next_eligible(self, now: Optional[datetime] = None) -> Optional[str]:
        """下次可能触发的时间（冷却结束后），用于排程提示"""
        now = now or datetime.now()
        state = self._load_state()
        last = _parse_ts(state.get("last_care_at") or "")
        if last is None:
            return now.isoformat(timespec="seconds")
        return (last + timedelta(hours=float(self.config["冷却小时"]))).isoformat(timespec="seconds")

    def reset(self) -> None:
        self._save_state({"last_care_at": None, "day": None, "count": 0, "history": []})


if __name__ == "__main__":
    import sys
    t = CareTrigger()
    if len(sys.argv) > 1 and sys.argv[1] == "reset":
        t.reset()
        print("已重置关怀状态")
    else:
        print(json.dumps(t.evaluate(), ensure_ascii=False, indent=2))
