#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双向人格镜像（M5）——伴侣人格克隆与用户理解的交汇层

方案 4.2 五件事：
1. 动态关系人格：同一人格在不同关系阶段呈现不同侧面
2. 双向记忆共鸣：用户偏好 ∩ 伴侣特征的交集，作为聊天素材
3. 关系演化建模：亲密度时间序列 + 趋势判定（升温/降温/倦怠/修复）
4. 跨角色一致性：回复是否跑偏出人设（生成后离线自检）
5. 元认知反馈：用户对回复的反馈回流，驱动下一次调整

数据位置：~/.love-companion/data/relations.json
红线：只依赖标准库；镜像结论只用于调节注入，不进记忆正文本体。
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 允许 `python scripts/persona/mirror.py` 直接跑（此时 sys.path[0] 是脚本所在目录）
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.core import settings as core_settings  # noqa: E402
from scripts.core.storage import read_json, write_json  # noqa: E402
from scripts.pipeline.injector import estimate_tokens  # noqa: E402

# 事件类型 → 亲密度增量（可正可负）
EVENT_DELTA = {
    "亲密": 0.06, "里程碑": 0.10, "日常": 0.01,
    "冲突": -0.08, "冷落": -0.04, "误解": -0.05, "和解": 0.05,
}

# 关系阶段阈值（按亲密度 0–1）
STAGES: Tuple[Tuple[float, str], ...] = (
    (0.25, "初识"), (0.45, "暧昧"), (0.70, "热恋"), (0.85, "稳定"), (1.01, "深度依恋"),
)

# 各阶段的「关系面」参数（动态关系人格）
FACE_BY_STAGE: Dict[str, Dict[str, Any]] = {
    "初识":   {"亲密度系数": 0.6, "称呼": "名字/昵称", "主动程度": "低", "话题边界": "避开私密与过去"},
    "暧昧":   {"亲密度系数": 0.8, "称呼": "昵称", "主动程度": "中", "话题边界": "可聊感受，不聊承诺"},
    "热恋":   {"亲密度系数": 1.0, "称呼": "宝贝类昵称", "主动程度": "高", "话题边界": "可谈未来"},
    "稳定":   {"亲密度系数": 0.95, "称呼": "固定昵称", "主动程度": "中", "话题边界": "可谈现实安排"},
    "深度依恋": {"亲密度系数": 1.0, "称呼": "专属称呼", "主动程度": "高", "话题边界": "无禁区，但需尊重回避点"},
}

_EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\U0001F000-\U0001F2FF"
                       "\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]")


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _parse_ts(ts: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(str(ts))
    except (TypeError, ValueError):
        return None


class MirrorModel:
    """双向人格镜像"""

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = core_settings.resolve_data_dir(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.file = self.data_dir / "relations.json"

    # ---------- IO ----------

    def _load(self) -> Dict[str, Any]:
        data = read_json(self.file, {})
        return data if isinstance(data, dict) else {}

    def _save(self, data: Dict[str, Any]) -> None:
        write_json(self.file, data)

    # ---------- 1. 关系演化建模 ----------

    def record(self, slug: str, kind: str, note: str = "", delta: Optional[float] = None) -> Dict[str, Any]:
        """记录一次关系事件（亲密/冲突/里程碑/和解/冷落…）"""
        if delta is None:
            delta = EVENT_DELTA.get(kind, 0.01)
        data = self._load()
        rel = data.setdefault(slug, {"events": [], "feedback": [], "stage": "", "intimacy": None})
        rel["events"].append({"ts": _now(), "kind": kind, "delta": float(delta), "note": note})
        rel["events"] = rel["events"][-300:]      # 只留最近 300 条，防止无限膨胀
        self._save(data)
        return rel

    def trend(self, slug: str, window: int = 5) -> float:
        """最近 N 次事件的亲密度平均增量（>0 升温，<0 降温）"""
        rel = self._load().get(slug) or {}
        events = (rel.get("events") or [])[-window:]
        if not events:
            return 0.0
        return round(sum(float(e.get("delta", 0)) for e in events) / len(events), 4)

    def intimacy(self, slug: str, half_life_days: float = 14.0) -> float:
        """当前亲密度 = 人格基线 + 事件增量（按时间半衰衰减）"""
        from scripts.persona.library import PersonaLibrary
        persona = PersonaLibrary(str(self.data_dir)).get(slug) or {}
        base = float((persona.get("性格") or {}).get("亲密度基线", 0.5) or 0.5)

        rel = self._load().get(slug) or {}
        now = datetime.now()
        score = base
        for e in (rel.get("events") or []):
            ts = _parse_ts(e.get("ts", ""))
            if ts is None:
                continue
            days = max(0.0, (now - ts).total_seconds() / 86400.0)
            score += float(e.get("delta", 0)) * (0.5 ** (days / half_life_days))
        return round(max(0.0, min(1.0, score)), 3)

    def stage(self, slug: str) -> str:
        """关系阶段；趋势显著为负判倦怠，近期有冲突后又回暖判修复"""
        rel = self._load().get(slug) or {}
        score = self.intimacy(slug)
        label = "初识"
        for threshold, name in STAGES:
            if score < threshold:
                label = name
                break

        trend = self.trend(slug)
        events = (rel.get("events") or [])[-5:]
        kinds = [e.get("kind") for e in events]
        if trend < -0.02:
            label = "倦怠"
        elif ("冲突" in kinds or "误解" in kinds) and trend > 0:
            label = "修复"

        data = self._load()
        rel = data.setdefault(slug, {"events": [], "feedback": [], "stage": "", "intimacy": None})
        rel["stage"], rel["intimacy"] = label, score
        self._save(data)
        return label

    def face(self, slug: str) -> Dict[str, Any]:
        """动态关系人格：当前阶段下 ta 呈现的那一面"""
        stage = self.stage(slug)
        base = dict(FACE_BY_STAGE.get(stage, FACE_BY_STAGE["初识"]))
        base["阶段"] = stage
        base["亲密度"] = self.intimacy(slug)
        base["趋势"] = self.trend(slug)
        return base

    # ---------- 2. 双向记忆共鸣 ----------

    def resonance(self, slug: str) -> Dict[str, Any]:
        """用户画像 ∩ 伴侣人格 → 共鸣点 / 互补点 / 雷区

        共鸣点：两边都感兴趣的话题（天然聊天素材）
        互补点：一边有、一边没有（可以互相带）
        雷区：用户的反感话题恰好是 ta 的高频关注（要避开）
        """
        from scripts.persona.library import PersonaLibrary
        from scripts.user.profile import UserProfileStore

        persona = PersonaLibrary(str(self.data_dir)).get(slug) or {}
        user = UserProfileStore(str(self.data_dir)).get() or {}

        user_likes = (user.get("互动偏好") or {}).get("喜欢的话题") or []
        user_hates = (user.get("互动偏好") or {}).get("反感的话题") or []
        partner_focus = (persona.get("思维") or {}).get("关注顺序") or []
        partner_values = (persona.get("思维") or {}).get("价值观") or []
        user_values = (user.get("情绪模式") or {}).get("触发点") or []

        likes_set, focus_set = set(user_likes), set(partner_focus)
        shared = [x for x in partner_focus if x in likes_set] or list(focus_set & likes_set)
        complement = [x for x in partner_focus if x not in likes_set][:3]
        mines = [x for x in partner_focus if x in set(user_hates)]

        value_shared = [v for v in partner_values if v in set(user_values)]
        return {
            "共鸣话题": shared[:5],
            "可带话题": complement,
            "雷区": mines,
            "价值观交集": value_shared,
            "置信度": round(min(
                1.0,
                (len(user_likes) + len(partner_focus)) / 20.0
            ), 2),
        }

    # ---------- 3. 跨角色一致性 ----------

    def consistency(self, reply: str, slug: str) -> Tuple[bool, List[str]]:
        """回复是否跑偏出人设（离线自检，不占主生成 Token）

        检查项：纠偏层命中 / 硬规则 / 句长严重偏离 / emoji 过量 / 编造式承诺
        """
        from scripts.persona.library import PersonaLibrary

        issues: List[str] = []
        lib = PersonaLibrary(str(self.data_dir))
        persona = lib.get(slug)
        if persona is None:
            return True, []
        v1 = persona.get("v1人设") or {}

        for c in lib.corrections(slug):
            wrong = (c.get("wrong") or "").strip()
            if wrong and wrong in (reply or ""):
                issues.append(f"命中纠偏：出现「{wrong}」")

        voice = persona.get("声线") or {}
        avg_len = float(voice.get("平均句长", 0) or 0)
        if avg_len >= 8 and len(reply or "") > avg_len * 4:
            issues.append(f"篇幅偏离：ta 平均说 {avg_len:.0f} 字，这条 {len(reply)} 字")

        expected = float(voice.get("emoji频率", 0) or 0)
        got = len(_EMOJI_RE.findall(reply or ""))
        if expected <= 0.2 and got > 0:
            issues.append("emoji 过量：ta 几乎不用表情")
        elif expected > 0 and got > int(expected * 3) + 1:
            issues.append(f"emoji 过量：ta 平均 {expected:.1f} 个/条，这条 {got} 个")

        # 真实性红线：不得编造共同经历
        if re.search(r"(我们(曾经|之前)说过|你说过|你记得吗)", reply or ""):
            issues.append("疑似编造共同经历")

        # 内容边界：v1 人设里用户明确划的红线。
        # 用户写的是「不谈前任」，真正的禁区是「前任」，靠 core/boundary 还原
        from scripts.core import boundary
        for b in boundary.hit(reply or "", v1.get("内容边界") or []):
            issues.append(f"触碰内容边界：{b}")

        return (not issues), issues

    # ---------- 4. 元认知反馈 ----------

    def feedback(self, slug: str, ok: bool, note: str = "") -> Dict[str, Any]:
        """用户对回复的反馈回流（喜欢/不喜欢）"""
        data = self._load()
        rel = data.setdefault(slug, {"events": [], "feedback": [], "stage": "", "intimacy": None})
        rel["feedback"].append({"ts": _now(), "ok": bool(ok), "note": note})
        rel["feedback"] = rel["feedback"][-200:]
        self._save(data)
        return self.feedback_stats(slug)

    def feedback_stats(self, slug: str) -> Dict[str, Any]:
        """反馈统计：差评率过高 → 建议降级语气强度"""
        rel = self._load().get(slug) or {}
        fb = (rel.get("feedback") or [])[-20:]
        if not fb:
            return {"样本": 0, "好评率": None, "建议": "暂无反馈"}
        good = sum(1 for f in fb if f.get("ok"))
        rate = good / len(fb)
        if rate >= 0.8:
            advice = "表现稳定，可维持当前强度"
        elif rate >= 0.5:
            advice = "好评率一般，建议语气强度下调一档"
        else:
            advice = "好评率偏低，建议回退到上一版人格并复核纠偏层"
        return {"样本": len(fb), "好评率": round(rate, 2), "建议": advice}

    # ---------- 汇总 ----------

    def brief(self, slug: str, budget: int = 60) -> str:
        """给在线注入的一句关系状态（默认 60 Token，从人格预算里分）"""
        face = self.face(slug)
        res = self.resonance(slug)
        parts = [f"关系阶段：{face['阶段']}（亲密度 {face['亲密度']}）"]
        if res.get("共鸣话题"):
            parts.append("共鸣话题：" + "、".join(res["共鸣话题"][:3]))
        if res.get("雷区"):
            parts.append("避雷：" + "、".join(res["雷区"][:2]))
        text = "；".join(parts)
        while estimate_tokens(text) > budget and "；" in text:
            text = text.rsplit("；", 1)[0]
        return text

    def clear(self, slug: str) -> bool:
        data = self._load()
        if slug not in data:
            return False
        data.pop(slug)
        self._save(data)
        return True


if __name__ == "__main__":
    import sys
    m = MirrorModel()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "brief" and len(sys.argv) > 2:
        print(m.brief(sys.argv[2]))
    elif cmd == "face" and len(sys.argv) > 2:
        print(json.dumps(m.face(sys.argv[2]), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(m._load(), ensure_ascii=False, indent=2))
