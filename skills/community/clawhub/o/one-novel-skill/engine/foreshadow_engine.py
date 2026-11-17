#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
foreshadow_engine.py — 三级伏笔闭环算法引擎

参考：《网络小说全维度创新创作与AI工业化稳态落地深度研究报告（进阶迭代版）》
第4章 §4.1.3 三级伏笔闭环算法

核心功能：
  - 短/中/长三级伏笔登记与台账管理
  - 伏笔回收节点进度监控
  - 自动触发器：临近回收章节推送铺垫/回收方案
  - 闭环校验：未完成的伏笔禁止主线推进

伏笔分级：
  - 短线（3-10章回收）
  - 中线（20-50章回收）
  - 长线（100章以上闭环）
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any

_log = logging.getLogger("foreshadow_engine")


class ForeshadowEngine:
    """三级伏笔闭环算法引擎"""

    def __init__(self, book_dir: str = ""):
        self.book_dir = Path(book_dir) if book_dir else None
        self._foreshadows: List[Dict] = []
        self._loaded = False

    # ========== 伏笔登记 ==========

    def register(
        self,
        content: str,
        level: str = "short",
        plant_chapter: int = 0,
        reveal_chapter: int = 0,
        related_chars: List[str] = None,
        desc: str = "",
    ) -> bool:
        """登记一条伏笔

        level: short(3-10章) / medium(20-50章) / long(100+章)
        """
        level = level.lower()
        if level not in ("short", "medium", "long"):
            _log.warning(f"未知伏笔级别: {level}，使用 short")
            level = "short"

        # 自动计算回收章节
        if reveal_chapter <= 0:
            if level == "short":
                reveal_chapter = plant_chapter + 6  # 3-10中间值
            elif level == "medium":
                reveal_chapter = plant_chapter + 35  # 20-50中间值
            else:
                reveal_chapter = plant_chapter + 150  # 100+中间值

        entry = {
            "id": f"FS-{plant_chapter:03d}-{len(self._foreshadows) + 1:02d}",
            "content": content,
            "level": level,
            "plant_chapter": plant_chapter,
            "reveal_chapter": reveal_chapter,
            "related_chars": related_chars or [],
            "desc": desc or content[:60],
            "status": "planted",  # planted / triggered / revealed / closed / abandoned
            "created_at": datetime.now().isoformat(),
            "revealed_at": "",
            "triggered_at": "",
        }
        self._foreshadows.append(entry)
        _log.info(f"伏笔登记: {entry['id']} [{level}] ch{plant_chapter}->{reveal_chapter}: {entry['desc']}")
        return True

    def register_from_text(self, text: str, chapter: int) -> int:
        """从章节文本自动提取潜在伏笔并登记，返回登记数"""
        if not text or not isinstance(text, str):
            return 0
        import re
        count = 0
        # 检测"疑问/悬念/秘密/奇怪"类语句
        markers = [
            (r"(难道|是不是|不对劲|有问题|奇怪|诡异|反常).{5,30}[。？?]", "short"),
            (r"(秘密|真相|谜|传说|预言|诅咒|宿命).{5,50}[。]?", "medium"),
            (r"(终极|最终|真正的|背后|隐藏|古老|远古).{5,50}[。]?", "long"),
        ]
        for pattern, level in markers:
            matches = re.findall(pattern, text)
            for m in matches[:3]:  # 每种最多3条
                self.register(
                    content=m,
                    level=level,
                    plant_chapter=chapter,
                    desc=m[:80],
                )
                count += 1
        return count

    # ========== 进度监控 ==========

    def check_pending(self, current_chapter: int) -> List[Dict]:
        """检查当前章节前有哪些待回收伏笔"""
        pending = []
        for fs in self._foreshadows:
            if fs["status"] == "planted" and fs["reveal_chapter"] <= current_chapter:
                pending.append(fs)
        return pending

    def check_upcoming(self, current_chapter: int, lookahead: int = 5) -> List[Dict]:
        """检查未来几章内需要回收的伏笔"""
        upcoming = []
        for fs in self._foreshadows:
            if fs["status"] == "planted":
                due = fs["reveal_chapter"] - current_chapter
                if 0 <= due <= lookahead:
                    upcoming.append({**fs, "due_in": due})
        return upcoming

    def get_overdue(self, current_chapter: int) -> List[Dict]:
        """获取已过回收期限但未处理的伏笔"""
        return [
            fs for fs in self._foreshadows
            if fs["status"] == "planted" and fs["reveal_chapter"] < current_chapter - 5
        ]

    # ========== 状态更新 ==========

    def trigger(self, foreshadow_id: str, chapter: int) -> bool:
        """触发伏笔（进入铺垫阶段）"""
        for fs in self._foreshadows:
            if fs["id"] == foreshadow_id and fs["status"] == "planted":
                fs["status"] = "triggered"
                fs["triggered_at"] = datetime.now().isoformat()
                _log.info(f"伏笔触发: {foreshadow_id} @ ch{chapter}")
                return True
        return False

    def reveal(self, foreshadow_id: str, chapter: int) -> bool:
        """回收伏笔"""
        for fs in self._foreshadows:
            if fs["id"] == foreshadow_id and fs["status"] in ("planted", "triggered"):
                fs["status"] = "revealed"
                fs["revealed_at"] = datetime.now().isoformat()
                _log.info(f"伏笔回收: {foreshadow_id} @ ch{chapter}")
                return True
        return False

    def close(self, foreshadow_id: str) -> bool:
        """闭环伏笔（完全解决）"""
        for fs in self._foreshadows:
            if fs["id"] == foreshadow_id and fs["status"] == "revealed":
                fs["status"] = "closed"
                _log.info(f"伏笔闭环: {foreshadow_id}")
                return True
        return False

    def abandon(self, foreshadow_id: str) -> bool:
        """废弃伏笔"""
        for fs in self._foreshadows:
            if fs["id"] == foreshadow_id and fs["status"] in ("planted", "triggered"):
                fs["status"] = "abandoned"
                _log.warning(f"伏笔废弃: {foreshadow_id}")
                return True
        return False

    # ========== 分析 ==========

    def analyze_chapter(self, text: str, chapter: int, block_on_overdue: bool = False) -> List[str]:
        """分析单章伏笔情况
        
        Args:
            block_on_overdue: 如果为True，有过期未回收伏笔时返回阻断信号
        """
        issues = []
        blocked = False

        # 1. 检查过期待回收的伏笔（阻断型）
        overdue = self.get_overdue(chapter)
        if overdue:
            names = ", ".join(f["id"] for f in overdue[:3])
            issues.append(f"[伏笔-阻断] {len(overdue)} 条伏笔已过回收期未处理")
            issues.append(f"  → 逾期伏笔: {names}")
            for f in overdue:
                issues.append(f"  → FS {f['id']}: 埋于第{f['plant_chapter']}章，计划回收第{f['reveal_chapter']}章，逾期{chapter - f['reveal_chapter']}章")
            if block_on_overdue:
                blocked = True

        # 2. 检查即将到期的伏笔
        upcoming = self.check_upcoming(chapter, lookahead=3)
        if upcoming:
            names = ", ".join(f"{f['id']}(ch{f['reveal_chapter']})" for f in upcoming[:3])
            issues.append(f"[伏笔] {len(upcoming)} 条伏笔即将到期: {names}")

        # 3. 统计伏笔健康度
        total = len(self._foreshadows)
        revealed = sum(1 for f in self._foreshadows if f["status"] in ("revealed", "closed"))
        abandoned = sum(1 for f in self._foreshadows if f["status"] == "abandoned")
        if total > 0:
            closure_rate = revealed / total * 100
            if total > 5 and closure_rate < 30:
                issues.append(f"[伏笔] 回收率 {closure_rate:.0f}% ({revealed}/{total})，建议加强伏笔闭环")
            if abandoned / max(total, 1) > 0.2:
                issues.append(f"[伏笔] 废弃率 {(abandoned/total*100):.0f}% 偏高，建议减少无效埋点")

        # 4. 自动登记新伏笔
        new_count = self.register_from_text(text, chapter)
        if new_count > 0:
            _log.info(f"自动登记 {new_count} 条新伏笔 (ch{chapter})")

        if blocked:
            issues.append("[伏笔-阻断BLOCKED] 请先回收逾期伏笔再继续写作")
        return issues

    def health_report(self, current_chapter: int) -> Dict[str, Any]:
        """输出伏笔健康报告"""
        total = len(self._foreshadows)
        planted = sum(1 for f in self._foreshadows if f["status"] == "planted")
        triggered = sum(1 for f in self._foreshadows if f["status"] == "triggered")
        revealed = sum(1 for f in self._foreshadows if f["status"] in ("revealed", "closed"))
        abandoned = sum(1 for f in self._foreshadows if f["status"] == "abandoned")
        overdue_count = len(self.get_overdue(current_chapter))
        by_level = {"short": 0, "medium": 0, "long": 0}
        for f in self._foreshadows:
            by_level[f["level"]] = by_level.get(f["level"], 0) + 1

        return {
            "total": total,
            "planted": planted,
            "triggered": triggered,
            "revealed": revealed,
            "abandoned": abandoned,
            "overdue": overdue_count,
            "by_level": by_level,
            "health": "good" if overdue_count == 0 and revealed > total * 0.3 else "need_attention",
        }

    # ========== 持久化 ==========

    def load_from_state(self, state_data: dict):
        fs_data = state_data.get("foreshadows", [])
        if fs_data:
            self._foreshadows = fs_data
            self._loaded = True
            _log.info(f"ForeshadowEngine: loaded {len(fs_data)} foreshadows")

    def to_dict(self) -> dict:
        return {"foreshadows": self._foreshadows[-500:]}  # 保留最新500条

    def save_to_file(self):
        """保存到追踪目录"""
        if not self.book_dir:
            return
        path = self.book_dir / "追踪" / "foreshadows.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    def load_from_file(self):
        """从追踪目录加载"""
        if not self.book_dir:
            return
        path = self.book_dir / "追踪" / "foreshadows.json"
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                self._foreshadows = data.get("foreshadows", [])
                self._loaded = True
            except Exception as e:
                _log.warning(f"ForeshadowEngine: 加载失败 {e}")

    def reset(self):
        self._foreshadows.clear()
        self._loaded = False
