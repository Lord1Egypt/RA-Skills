#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v1 人设适配层——把三层提取的结果翻译回 v1 人设字段

**为什么有这个文件**：M3a 的三层提取（声线/思维/性格）是蒸馏的**中间产物**，
不是最终存储形态。love-companion 本来就有自己的人设体系——`persona.json` 的
姓名/性格/对话风格/背景故事/相处模式/亲密尺度/内容边界，
以及 8 套开箱即用的预设。如果另外立一套人格文件来存提取结果，
用户就会面对两套人设：`/恋人配置` 改的是 A，蒸馏出来的是 B，谁也说不清谁生效。

所以本模块只做一件事：**把三层提取的结果翻译回 v1 人设字段**，
使人设的真相源始终只有一个（`persona.json`），蒸馏只是"用素材校准它"。

映射关系（三层 → v1）：
    声线.口头禅/语气词/句式/标点/emoji  → 对话风格.口头禅/语气/语言习惯
    性格.情绪反应/冲突应对              → 性格.核心特质/小脾气/情绪表达
    思维.价值观/关注顺序                → 背景故事（补充）
    性格.亲密度基线/思维.决策逻辑        → 相处模式.主动程度/关心方式

**绝不覆盖**：亲密尺度、内容边界、对用户的称呼——这三样是用户显式设置的安全与
体验项，蒸馏素材无权改动。
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# 允许 `python scripts/persona/adapt.py` 直接跑（此时 sys.path[0] 是脚本所在目录）
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


def _sentence_shape(voice: Dict[str, Any]) -> str:
    """句式描述的唯一出处：优先用提取出的句式，没有就按平均句长推导。

    只进 v1 对话风格.语气——语言习惯不再重复写一遍（排查缺陷 3）。
    """
    shape = (voice.get("句式") or "").strip()
    if shape:
        return shape
    avg = voice.get("平均句长")
    if isinstance(avg, (int, float)) and avg:
        if avg <= 12:
            return "短句连发，一条消息一句话"
        if avg >= 40:
            return "会把话说完整，偏长句"
        return "长短句交替"
    return ""

# 蒸馏无权改动的字段（用户显式设置）
IMMUTABLE_FIELDS = ("亲密尺度", "内容边界", "对用户的称呼", "姓名", "性别", "年龄")

# 冲突应对 → v1「小脾气」
CONFLICT_TO_QUIRK: Dict[str, str] = {
    "回避": "闹别扭时先不说话，缓过来才肯开口",
    "妥协": "吵完会先低头，嘴上说没事其实在意",
    "对抗": "不高兴了会直接怼回去，事后才软下来",
    "冷战": "生气了会说『嗯』『哦』，等对方来哄",
    "就事论事": "有分歧就讲道理，不太会翻旧账",
}

# 决策逻辑 → v1「关心方式」
DECISION_TO_CARE: Dict[str, str] = {
    "直觉型": "凭感觉察觉你不开心，先哄再说",
    "权衡型": "会帮你把事情捋一遍，再给建议",
    "依赖型": "什么都先问你的意思，替你拿主意时会犹豫",
    "果断型": "发现问题直接给方案，不绕弯子",
    "混合型": "看情况，小事陪你聊，大事帮你想办法",
}

# 亲密度基线 → v1「主动程度」
INTIMACY_TO_INITIATIVE: Dict[str, str] = {"高": "高", "中": "中", "低": "低"}


def _modal_to_tone(voice: Dict[str, Any]) -> str:
    """声线的语气词/句式 → v1 对话风格.语气"""
    tails = voice.get("语气词") or []
    shape = _sentence_shape(voice)
    if tails and shape:
        return f"句尾常带{'、'.join(tails[:3])}；{shape}"
    if tails:
        return f"句尾常带{'、'.join(tails[:3])}"
    return shape or ""


def _emoji_to_habit(voice: Dict[str, Any]) -> str:
    """标点/emoji → v1 对话风格.语言习惯（句式归「语气」，这里不重复）"""
    parts: List[str] = []
    freq = voice.get("emoji频率") or 0
    if isinstance(freq, (int, float)):
        if freq >= 0.5:
            parts.append("爱用表情")
        elif freq <= 0.05:
            parts.append("几乎不用表情")
    punct = voice.get("标点习惯")
    if punct and punct != "少用标点":
        parts.append(f"标点偏好{punct}")
    return "；".join(parts)


def apply_to_v1(base: Optional[Dict[str, Any]], extracted: Dict[str, Any],
                overwrite: bool = False) -> Dict[str, Any]:
    """把三层提取的结果合并进 v1 人设

    Args:
        base: 现有人设（v1 persona.json 结构，可为空）
        extracted: extract.extract_persona() 的产出（声线/思维/性格三层）
        overwrite: True 时蒸馏结果覆盖已有值；False 时只填空（保留用户手写的）

    Returns:
        v1 人设结构；IMMUTABLE_FIELDS 一律沿用 base
    """
    import copy
    out = copy.deepcopy(base) if base else {}

    voice = extracted.get("声线") or {}
    think = extracted.get("思维") or {}
    char = extracted.get("性格") or {}

    # ---- 声线 → 对话风格 ----
    style = out.setdefault("对话风格", {})
    if voice:
        _set(style, "口头禅", list(voice.get("口头禅") or [])[:5], overwrite)
        _set(style, "语气", _modal_to_tone(voice), overwrite)
        _set(style, "语言习惯", _emoji_to_habit(voice), overwrite)

    # ---- 性格 → 性格 ----
    persona_char = out.setdefault("性格", {})
    traits: List[str] = []
    for v in (think.get("价值观") or [])[:3]:
        traits.append(f"看重{v}")
    if char.get("情绪反应模式"):
        traits.append(char["情绪反应模式"])
    if traits:
        _set(persona_char, "核心特质", traits, overwrite)
    if char.get("冲突应对") in CONFLICT_TO_QUIRK:
        _set(persona_char, "小脾气", [CONFLICT_TO_QUIRK[char["冲突应对"]]], overwrite)
    if char.get("情绪反应模式"):
        _set(persona_char, "情绪表达", char["情绪反应模式"], overwrite)

    # ---- 思维 → 背景故事 / 相处模式 ----
    focus = think.get("关注顺序") or []
    if focus:
        line = "平时聊得最多的是" + "、".join(focus[:4])
        old = out.get("背景故事") or ""
        if line not in old:
            out["背景故事"] = (old + "；" + line).strip("；") if old else line

    relation = out.setdefault("相处模式", {})
    baseline = char.get("亲密度基线")
    if isinstance(baseline, (int, float)):
        level = "高" if baseline >= 0.7 else ("低" if baseline <= 0.35 else "中")
        _set(relation, "主动程度", INTIMACY_TO_INITIATIVE[level], overwrite)
    if think.get("决策逻辑") in DECISION_TO_CARE:
        _set(relation, "关心方式", DECISION_TO_CARE[think["决策逻辑"]], overwrite)

    # ---- 撒娇频率：由声线的语气词与 emoji 推断 ----
    sajiao = 0
    if voice.get("语气词"):
        sajiao += 1
    if (voice.get("emoji频率") or 0) >= 0.3:
        sajiao += 1
    if sajiao >= 2:
        _set(relation, "撒娇频率", "高", overwrite)
    elif sajiao == 1:
        _set(relation, "撒娇频率", "中", overwrite)

    # ---- 安全项：一律沿用用户设置 ----
    for field in IMMUTABLE_FIELDS:
        if base and field in base:
            out[field] = base[field]

    out["_蒸馏"] = {
        "语料量": extracted.get("语料量", 0),
        "声线置信度": (voice.get("置信度") or 0),
        "思维置信度": (think.get("置信度") or 0),
        "性格置信度": (char.get("置信度") or 0),
        "来源素材": extracted.get("来源素材") or [],
    }
    return out


def _set(target: Dict[str, Any], key: str, value: Any, overwrite: bool) -> None:
    """overwrite=False 时只填空，不覆盖用户手写的值"""
    if not value:
        return
    if overwrite or not target.get(key):
        target[key] = value


# ==================== 恋人行为卡（在线注入用） ====================

def is_configured(persona: Dict[str, Any]) -> bool:
    """用户到底有没有真的配置过人设

    v1 的 DEFAULT_PERSONA 自带「主动程度=中 / 撒娇频率=中 / 亲密尺度=3」，
    这些是默认值不是用户意图。若拿空壳去编译，注入的就是
    「主动程度：中。亲密尺度 3 级」这种纯噪音——按「能不注入就不注入」，
    没配置过就别注入。
    """
    if not persona:
        return False
    if (persona.get("姓名") or "").strip() or (persona.get("昵称") or "").strip():
        return True
    style = persona.get("对话风格") or {}
    if style.get("语气") or style.get("口头禅") or style.get("语言习惯"):
        return True
    char = persona.get("性格") or {}
    if char.get("核心特质") or char.get("情绪表达") or char.get("小脾气"):
        return True
    relation = persona.get("相处模式") or {}
    if relation.get("关心方式"):
        return True
    return bool(persona.get("背景故事") or persona.get("内容边界"))


def lover_card(persona: Optional[Dict[str, Any]], budget: int = 100) -> str:
    """把 v1 人设编译成在线注入的「恋人行为卡」

    这是 love-companion 自己的形态：由 v1 人设字段编译，不是三层提取的原始结构。
    没有蒸馏过素材的用户同样能用——8 套预设本身就是完整的 v1 人设。

    Args:
        persona: v1 人设结构（persona.json）
        budget: Token 上限，默认 100（人格指令预算）
    """
    from scripts.pipeline.injector import estimate_tokens, truncate_to_tokens

    persona = persona or {}
    if not isinstance(persona, dict):
        return ""

    must: List[str] = []      # 安全约束，截断时必须保住
    nice: List[str] = []      # 风格描述，可以砍

    name = persona.get("姓名") or persona.get("昵称") or ""
    call = persona.get("对用户的称呼") or ""
    if name or call:
        head = f"你是{name}" if name else "你是用户的恋人"
        if call:
            head += f"，叫他「{call}」"
        must.append(head)

    style = persona.get("对话风格") or {}
    style_bits = []
    if style.get("语气"):
        style_bits.append(style["语气"])
    if style.get("口头禅"):
        style_bits.append("口头禅：" + "、".join(style["口头禅"][:3]))
    if style.get("语言习惯"):
        style_bits.append(style["语言习惯"])
    if style_bits:
        nice.append("说话方式：" + "；".join(style_bits))

    char = persona.get("性格") or {}
    char_bits = []
    if char.get("核心特质"):
        char_bits.append("、".join(char["核心特质"][:3]))
    if char.get("小脾气"):
        char_bits.append("、".join(char["小脾气"][:2]))
    if char.get("情绪表达"):
        char_bits.append(char["情绪表达"])
    if char_bits:
        nice.append("性格：" + "；".join(char_bits))

    relation = persona.get("相处模式") or {}
    rel_bits = []
    if relation.get("关心方式"):
        rel_bits.append(f"关心方式：{relation['关心方式']}")
    if relation.get("主动程度"):
        rel_bits.append(f"主动程度：{relation['主动程度']}")
    if relation.get("撒娇频率"):
        rel_bits.append(f"撒娇频率：{relation['撒娇频率']}")
    if rel_bits:
        nice.append("；".join(rel_bits))

    # ---- 以下两条是约束，不是描述：截断绝不能把它们砍掉 ----
    scale = persona.get("亲密尺度")
    if isinstance(scale, int):
        must.append(f"亲密尺度 {scale} 级")

    bounds = persona.get("内容边界") or []
    if bounds:
        must.append("不碰：" + "、".join(bounds[:3]))

    must_text = "。".join(p for p in must if p)
    nice_text = "。".join(p for p in nice if p)

    room = budget - estimate_tokens(must_text) - 1
    if room <= 0 or not nice_text:
        card = must_text                      # 预算太紧，只保约束
    else:
        # 风格在前、约束压后，读起来像「先说人设，最后交代规矩」
        card = (truncate_to_tokens(nice_text, room) + "。" + must_text).strip("。")

    return truncate_to_tokens(card, budget)


def from_v1_file(data_dir: Optional[str] = None, budget: int = 100) -> str:
    """直接读 v1 的 persona.json 生成行为卡（未蒸馏素材的用户走这条）

    没配置过人设就返回空串——空壳不该产生注入。
    """
    import os
    from pathlib import Path
    from scripts.manager import LoveCompanionManager

    resolved = data_dir or os.environ.get("LOVE_COMPANION_DATA_DIR", "~/.love-companion/data")
    manager = LoveCompanionManager(str(Path(os.path.expanduser(str(resolved)))))
    persona = manager.get_persona()
    if not is_configured(persona):
        return ""
    return lover_card(persona, budget=budget)


if __name__ == "__main__":
    card = from_v1_file()
    print(card or "（v1 persona.json 为空，先 /恋人配置 或 /恋人套用 N）")
