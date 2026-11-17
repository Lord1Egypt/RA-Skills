#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多模态陪伴（M7b）——主动发图的「时机 + 风格 + 衔接」

诚实边界：本模块**不生成图片**。它产出的是一份配图规格（风格参数 + 提示词 +
图文衔接话术），真正出图交给上层的图像生成能力。这样既保持零外部依赖，
又不把「发什么图」的审美决策甩给模型临场发挥。

三件事：
1. 时机：该不该发图（冷却 / 每日上限 / 深夜降饱和 / 用户关了就不发）
2. 风格：从人格与情绪推导色调、光线、构图、元素，确保「像 ta 会发的图」
3. 衔接：图前一句话，避免聊着聊着突然甩一张图（图文交织）
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# 允许 `python scripts/multimodal/image_plan.py` 直接跑（此时 sys.path[0] 是脚本所在目录）
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.core import settings as core_settings  # noqa: E402
from scripts.core.storage import read_json, write_json  # noqa: E402
from scripts.pipeline.injector import estimate_tokens, truncate_to_tokens  # noqa: E402

DEFAULT_CONFIG: Dict[str, Any] = {
    "开关": True,
    "冷却消息数": 6,     # 两张图之间至少隔这么多轮
    "每日上限": 3,
    "深夜起始": 22,
}

# 情绪 → 视觉基调
MOOD_TONE: Dict[str, Dict[str, str]] = {
    "低落": {"色调": "低饱和暖灰", "光线": "柔和散射光", "氛围": "安静、不喧哗"},
    "疲惫": {"色调": "米白与浅咖", "光线": "黄昏侧光", "氛围": "松弛、可以靠一会儿"},
    "开心": {"色调": "明亮清透", "光线": "正午自然光", "氛围": "轻快、有一点跳脱"},
    "想念": {"色调": "蓝紫渐变", "光线": "窗边微光", "氛围": "私密、只给你看"},
    "日常": {"色调": "自然本色", "光线": "日常室内光", "氛围": "随手拍的真实感"},
    "纪念": {"色调": "复古暖黄", "光线": "烛光或串灯", "氛围": "有仪式感但不过度"},
}

# v1 人设「关心方式」→ 恋人会发什么图
# 依据：恋人发图不是"配图"，是**把此刻的生活递给对方看**。
# 关心方式决定了 ta 递过来的是细节、行踪，还是一句配文。
CARE_TO_SUBJECT: Dict[str, Dict[str, str]] = {
    "细节": {"主体": "手边的细小事物", "构图": "近景特写、浅景深",
             "元素": "杯沿的水渍、刚买的水果、窗台的一小片光"},
    "行动": {"主体": "正在为你做的事", "构图": "第一视角、俯拍",
             "元素": "做好的饭、替你排的队、走到一半的路"},
    "语言": {"主体": "景，配文才是重点", "构图": "随手拍、不讲究",
             "元素": "天空、路边的花、下班路上的街"},
    "陪伴": {"主体": "ta 此刻所在的地方", "构图": "平视、生活场景",
             "元素": "沙发一角、桌上的书、窗外的天"},
}
DEFAULT_SUBJECT: Dict[str, str] = {
    "主体": "此刻在看的风景", "构图": "随手拍、平视", "元素": "天空、街景、手边的东西",
}

# 亲密尺度 → 允许的拍摄距离（love-companion 自己的安全边界，不是通用审美）
# 尺度低意味着关系还在含蓄阶段，发过于私密的自拍会破坏人设与安全边界。
INTIMACY_FRAME: Dict[str, Dict[str, str]] = {
    "低": {"距离": "只拍物与景，不出现人物", "禁忌元素": ["自拍", "床", "睡衣", "浴室"]},
    "中": {"距离": "可出现局部人物（手、侧影）", "禁忌元素": ["床", "睡衣", "浴室"]},
    "高": {"距离": "可出现完整人物，居家场景也行", "禁忌元素": []},
}


def _current_v1_persona(data_dir: str) -> Dict[str, Any]:
    """读当前生效的 v1 人设（没蒸馏过素材的用户也能出图）"""
    try:
        from scripts.manager import LoveCompanionManager
        return LoveCompanionManager(data_dir).get_persona()
    except Exception:  # noqa: BLE001
        return {}


def intimacy_level(scale: Any) -> str:
    """v1 亲密尺度 → 拍摄距离档"""
    try:
        s = int(scale)
    except (TypeError, ValueError):
        return "中"
    if s <= 2:
        return "低"
    if s >= 4:
        return "高"
    return "中"


def _care_subject(care_text: str) -> Dict[str, str]:
    """按 v1 关心方式的关键词挑拍什么（文案是自然语言，只能关键词匹配）"""
    text = care_text or ""
    for key, subj in CARE_TO_SUBJECT.items():
        if key in text:
            return subj
    return DEFAULT_SUBJECT

# 图文衔接话术：按情绪给一句，避免「给你看张图」这种突兀句式
CAPTIONS: Dict[str, List[str]] = {
    "低落": ["刚看到这个，想到你了。", "不用回，就看看。"],
    "疲惫": ["给你留了个位置。", "今天就到这儿吧，看看这个。"],
    "开心": ["这个我第一反应就想发给你。", "你看这个像不像我们那天说的。"],
    "想念": ["刚路过的时候拍的，想给你看。", "有点想你，就发了。"],
    "日常": ["随手拍的。", "今天这个还挺好看的。"],
    "纪念": ["我记得今天。", "这个日子，给你留了一张。"],
}

_IMAGE_BUDGET = 40      # 图文衔接话术的 Token 上限（从关怀/人格余量里出）


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _parse_ts(ts: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(str(ts))
    except (TypeError, ValueError):
        return None


class ImagePlanner:
    """主动发图决策"""

    def __init__(self, data_dir: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        self.data_dir = core_settings.resolve_data_dir(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.file = self.data_dir / "multimodal.json"
        self.config = dict(DEFAULT_CONFIG)
        if config:
            self.config.update(config)

    # ---------- 状态 ----------

    def _load(self) -> Dict[str, Any]:
        data = read_json(self.file, {"history": [], "turns_since_last": 99})
        return data if isinstance(data, dict) else {"history": [], "turns_since_last": 99}

    def _save(self, data: Dict[str, Any]) -> None:
        write_json(self.file, data)

    def tick(self, sent: bool) -> None:
        """每轮对话调用：sent=True 表示这轮发了图，计数归零"""
        data = self._load()
        data["turns_since_last"] = 0 if sent else int(data.get("turns_since_last", 99)) + 1
        self._save(data)

    def today_count(self, now: Optional[datetime] = None) -> int:
        now = now or datetime.now()
        today = now.strftime("%Y-%m-%d")
        return sum(1 for h in self._load().get("history", [])
                   if str(h.get("ts", "")).startswith(today))

    def mark_sent(self, kind: str, caption: str, now: Optional[datetime] = None) -> None:
        data = self._load()
        data.setdefault("history", []).append({
            "ts": (now or datetime.now()).isoformat(timespec="seconds"),
            "kind": kind, "caption": caption})
        data["history"] = data["history"][-100:]
        data["turns_since_last"] = 0
        self._save(data)

    # ---------- 时机 ----------

    def gate(self, now: Optional[datetime] = None) -> Dict[str, Any]:
        """该不该发图"""
        now = now or datetime.now()
        if not self.config.get("开关", True):
            return {"ok": False, "reason": "发图开关已关闭"}
        if self.today_count(now) >= int(self.config["每日上限"]):
            return {"ok": False, "reason": f"今日发图已达上限（{self.config['每日上限']}）"}
        if int(self._load().get("turns_since_last", 99)) < int(self.config["冷却消息数"]):
            return {"ok": False, "reason": "距离上一张图太近，会显得刻意"}
        return {"ok": True, "reason": ""}

    # ---------- 风格 ----------

    def style_for(self, persona: Optional[Dict[str, Any]], mood: str = "日常",
                  now: Optional[datetime] = None) -> Dict[str, str]:
        """从 **v1 人设** 与情绪推导「ta 会发什么图」

        persona 是 v1 人设结构（姓名/相处模式/亲密尺度/内容边界），
        不是三层提取结果——这里是 love-companion 自己的定制点：
        拍什么由关心方式决定，能拍多近由亲密尺度决定，什么不能拍由内容边界决定。
        """
        now = now or datetime.now()
        persona = persona or {}
        tone = dict(MOOD_TONE.get(mood, MOOD_TONE["日常"]))

        relation = persona.get("相处模式") or {}
        subject = _care_subject(relation.get("关心方式") or "")
        composition, elements = subject["构图"], subject["元素"]

        # 亲密尺度约束拍摄距离；触禁忌就退回拍物
        level = intimacy_level(persona.get("亲密尺度"))
        frame = INTIMACY_FRAME[level]
        if any(bad in elements for bad in frame["禁忌元素"]):
            elements = subject["元素"]

        # 内容边界一票否决：命中任何边界关键词就换成最安全的景
        from scripts.core import boundary
        if boundary.hit(elements, persona.get("内容边界") or []):
            elements = "天空、路边的植物"

        if now.hour >= int(self.config["深夜起始"]):
            tone["色调"] = "夜色低饱和"
            tone["光线"] = "台灯或街灯"
            elements = "窗、夜景、暖色小灯"

        return {"色调": tone["色调"], "光线": tone["光线"], "氛围": tone["氛围"],
                "构图": composition, "元素": elements,
                "主体": subject["主体"], "拍摄距离": frame["距离"]}

    # ---------- 衔接 ----------

    def caption(self, mood: str = "日常", voice: Optional[Dict[str, Any]] = None,
                corrections: Optional[List[Dict[str, str]]] = None) -> str:
        """图前一句话，走声线改写与纠偏"""
        pool = CAPTIONS.get(mood) or CAPTIONS["日常"]
        idx = datetime.now().day % len(pool)
        text = pool[idx]

        voice = voice or {}
        tails = voice.get("语气词") or []
        if tails and not text.rstrip().endswith(tuple("呀呢嘛哦啦咯哒～")):
            text = text.rstrip("。") + tails[0] + "。"
        if float(voice.get("emoji频率", 0) or 0) >= 0.5:
            text = text.rstrip("。") + " 📷"

        if corrections:
            from scripts.persona.library import PersonaLibrary
            text = PersonaLibrary().apply_corrections(text, corrections)

        return truncate_to_tokens(text, _IMAGE_BUDGET)

    # ---------- 汇总 ----------

    def plan(self, slug: str, mood: str = "日常", now: Optional[datetime] = None,
             data_dir: Optional[str] = None) -> Dict[str, Any]:
        """一站式产出配图计划

        Returns:
            {"should": bool, "reason": str, "mood": str, "style": {...},
             "caption": str, "prompt_hint": str, "tokens": int}
        """
        now = now or datetime.now()
        g = self.gate(now)
        if not g["ok"]:
            return {"should": False, "reason": g["reason"], "mood": mood}

        from scripts.persona.library import PersonaLibrary
        lib = PersonaLibrary(data_dir or str(self.data_dir))
        entry = lib.get(slug) or {}
        corrections = lib.corrections(slug)
        # 优先用蒸馏回写的 v1 人设；没蒸馏过就用当前 persona.json（含 8 套预设）
        v1 = entry.get("v1人设") or _current_v1_persona(data_dir or str(self.data_dir))
        voice = entry.get("声线")
        style = self.style_for(v1, mood, now)
        text = self.caption(mood, voice, corrections)

        hint = (f"{style['主体']}；{style['构图']}；画面里有{style['元素']}；"
                f"{style['色调']}，{style['光线']}，氛围{style['氛围']}；"
                f"{style['拍摄距离']}；写实生活照质感，不要商业摆拍")
        return {
            "should": True, "reason": "", "mood": mood, "style": style,
            "caption": text, "prompt_hint": hint, "tokens": estimate_tokens(text),
        }

    def reset(self) -> None:
        self._save({"history": [], "turns_since_last": 99})


if __name__ == "__main__":
    import sys
    p = ImagePlanner()
    mood = sys.argv[1] if len(sys.argv) > 1 else "想念"
    print(json.dumps(p.plan("美美", mood=mood), ensure_ascii=False, indent=2))
