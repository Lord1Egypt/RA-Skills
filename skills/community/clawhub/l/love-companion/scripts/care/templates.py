#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关怀话术生成（M6）——把「该关心了」变成一句像 ta 会说的话

两条纪律：
1. **不空泛**：每条模板都留了 {detail} 位，必须用记忆里的具体事实填，
   填不出来就换更短的模板，绝不用「记得照顾好自己」这类万能句。
2. **过声线**：生成后按伴侣人格的口头禅/语气词/emoji 习惯改写，
   并走纠偏层（library.apply_corrections），确保不像 AI 写的。

预算：默认 80 Token（schema.注入预算.关怀话术），超了直接截断。
"""

import hashlib
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# 允许 `python scripts/care/templates.py` 直接跑（此时 sys.path[0] 是脚本所在目录）
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.core import schema  # noqa: E402
from scripts.core import settings as core_settings  # noqa: E402
from scripts.pipeline.injector import estimate_tokens, truncate_to_tokens  # noqa: E402

_EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\U0001F000-\U0001F2FF"
                       "\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]")

# 依恋差异化（方案 4.3 明确要求）
#   焦虑型 → 给确定性：说清"我在、什么时候、会怎样"，避免模糊与留白
#   回避型 → 给空间：不追问、不要求回应，来了就聊，不来不催
#   安全型 → 自然陪伴：平等轻松地聊，不用刻意安抚
#   恐惧型 → 既给确定性又给退路：先表态，再明确说"你可以不回"
ATTACHMENT_TWEAK: Dict[str, Dict[str, Any]] = {
    "焦虑型": {
        "后缀": ["我在，看到就回你。", "不是客气，是真的在。"],
        "禁忌": ["？", "在吗"],        # 开放式追问会放大焦虑
        "语气": "确定",
    },
    "回避型": {
        "后缀": ["不用回我，就是想让你知道。", "忙你的，回头再说。"],
        "禁忌": ["为什么不", "怎么不回"],   # 追问与质问会让回避型更退
        "语气": "留白",
    },
    "安全型": {
        "后缀": ["回头聊。", "先这样~"],
        "禁忌": [],
        "语气": "自然",
    },
    "恐惧型": {
        "后缀": ["我在，但你不用马上回。", "想说的时候再说，不急。"],
        "禁忌": ["为什么不", "你应该"],
        "语气": "确定+留退路",
    },
    "未知": {"后缀": [], "禁忌": [], "语气": "自然"},
}


def apply_attachment(text: str, attachment: str, seed: int = 0) -> str:
    """按依恋类型改写关怀话术

    - 去掉该类型的禁忌说法
    - 焦虑型/恐惧型补一句确定性后缀；回避型补一句"不用回"
    """
    tweak = ATTACHMENT_TWEAK.get(attachment) or ATTACHMENT_TWEAK["未知"]
    out = text or ""
    for bad in tweak["禁忌"] or []:
        out = out.replace(bad, "。").replace("。。", "。").strip("。")
    tails = tweak["后缀"] or []
    if tails:
        out = out.rstrip("。") + "。" + tails[seed % len(tails)]
    return re.sub(r"。{2,}", "。", out).strip()


# 各关怀类型的话术模板。{nick} 称呼 / {detail} 具体事实 / {topic} 她关心的事
TEMPLATES: Dict[str, List[str]] = {
    "低落陪伴": [
        "{nick}，今天听你说话就觉得有点累。{detail}",
        "{nick}，不想说也行，我在。",
        "先别撑着了，{nick}。要不要我陪你发会儿呆。",
        "听起来今天不太顺。我不问了，就陪你待着。",
    ],
    "纪念日": [
        "{nick}，今天是{detail}。我一直记着。",
        "{nick}，{detail}——这个日子我可没忘。",
        "今天是我们的{detail}。谢谢你还在。",
    ],
    "深夜晚安": [
        "{nick}，很晚了，睡吧。明天再聊。",
        "别熬了{nick}，闭上眼睛，我在。",
        "晚安{nick}。今天辛苦了。",
    ],
    "久未联系": [
        "{nick}，好几个小时没你的消息了，还好吗。",
        "刚看到{detail}，突然想起你。",
        "在忙吗{nick}。不急，看到了回我一句就行。",
        "{nick}？有点想你了。",
    ],
}

# 兜底：没有任何具体事实时的通用句（仍然短，仍然不像模板）
FALLBACK_DETAIL = {
    "低落陪伴": "别硬扛",
    "纪念日": "那个日子",
    "深夜晚安": "",
    "久未联系": "你上次说的那件事",
}

CARING_EMOJI = {"低落陪伴": "🫂", "纪念日": "🌙", "深夜晚安": "🌙", "久未联系": "👋"}


def _now_key(kind: str) -> str:
    """按 日期+类型 选模板：同一天同一类型稳定，隔天自动换，避免机械重复"""
    return datetime.now().strftime("%Y-%m-%d") + "|" + kind


def pick_template(kind: str, index: Optional[int] = None) -> str:
    pool = TEMPLATES.get(kind) or ["{nick}，在吗。"]
    if index is not None:
        return pool[index % len(pool)]
    h = hashlib.md5(_now_key(kind).encode("utf-8")).hexdigest()
    return pool[int(h, 16) % len(pool)]


def apply_voice(text: str, voice: Optional[Dict[str, Any]], nickname: str = "") -> str:
    """按 ta 的声线改写一句话"""
    voice = voice or {}
    out = text

    # 语气词：句尾补一个 ta 常用的
    tails = voice.get("语气词") or []
    if tails and not re.search(r"[呀呢嘛哦啦咯哒鸭叭惹～]$", out.rstrip()):
        out = out.rstrip("。.!！") + tails[0]

    # emoji：ta 用得多才加，而且只加一个
    if float(voice.get("emoji频率", 0) or 0) >= 0.5 and not _EMOJI_RE.search(out):
        out += "🌙"

    # 口头禅：短句时才有空间塞
    catchphrases = voice.get("口头禅") or []
    if catchphrases and len(out) < 20:
        out = catchphrases[0] + "，" + out

    return out


def render(kind: str, nickname: str = "", detail: str = "",
           voice: Optional[Dict[str, Any]] = None,
           corrections: Optional[List[Dict[str, str]]] = None,
           length_pref: str = "", budget: Optional[int] = None,
           attachment: str = "", seed: Optional[int] = None) -> str:
    """渲染一条关怀话术

    Args:
        kind: 低落陪伴 / 纪念日 / 深夜晚安 / 久未联系
        nickname: 对用户的称呼（v1 人设的「对用户的称呼」，不是 ta 的名字）
        detail: 具体事实（来自记忆），没有就用兜底
        voice: 伴侣人格的声线层（library.get(slug)["声线"]）
        corrections: 纠偏规则（library.corrections(slug)）
        length_pref: 用户回复长度偏好，"短" 时只保留第一句
        budget: Token 预算，默认取注入预算表里的「关怀话术」
        attachment: 依恋类型（焦虑型/回避型/安全型/恐惧型），空则不做差异化
        seed: 模板与后缀的选取种子，不传按日期取（同一天稳定）
    """
    limit = int(budget if budget is not None
                else schema.DEFAULT_INJECTION_BUDGET["关怀话术"])
    if seed is None:
        seed = datetime.now().day

    # 未知类型不硬凑——宁肯不发，也不能把「在吗。」这种话发给用户
    if kind not in TEMPLATES:
        return ""

    template = pick_template(kind)
    nick = nickname or ""
    fill = (detail or "").strip() or FALLBACK_DETAIL.get(kind, "")
    text = template.format(nick=nick, detail=fill, topic=fill)

    # 没有称呼时，去掉称呼留下的逗号和空格
    text = re.sub(r"，(?=，)|^，|(?<=^)，", "", text).replace("，。", "。").strip()
    text = re.sub(r"\s{2,}", " ", text)

    text = apply_voice(text, voice, nick)

    # 先按长度偏好截断，再补依恋后缀——否则后缀会被一起截掉，
    # 而「我在，看到就回你」恰恰是焦虑型最需要的那句
    if length_pref == "短":
        head = re.split(r"[。！？!?\n]", text)
        text = (head[0] + "。") if head and head[0] else text

    if attachment:
        text = apply_attachment(text, attachment, seed)

    if corrections:
        from scripts.persona.library import PersonaLibrary
        text = PersonaLibrary().apply_corrections(text, corrections)

    if estimate_tokens(text) > limit:
        text = truncate_to_tokens(text, limit)
    return text


def compose(kind: str, slug: str, data_dir: Optional[str] = None,
            detail: str = "", budget: Optional[int] = None) -> Dict[str, Any]:
    """一站式生成：自动加载人格库与用户画像

    Returns:
        {"kind":..., "text":..., "tokens":..., "budget":..., "used_detail": str}
        未知 kind 时 text 为空串，调用方据此决定不发送。
    """
    from scripts.persona.library import PersonaLibrary
    from scripts.user.profile import UserProfileStore

    if budget is None:
        budget = core_settings.budget(data_dir, "关怀话术")

    lib = PersonaLibrary(data_dir)
    persona = lib.get(slug) or {}
    voice = persona.get("声线")
    corrections = lib.corrections(slug)

    user = UserProfileStore(data_dir).get() or {}
    length_pref = (user.get("互动偏好") or {}).get("回复长度偏好") or ""
    # 称呼取 v1 人设里「对用户的称呼」（ta 怎么叫你），没有才退回 ta 的名字
    v1 = persona.get("v1人设") or {}
    nickname = (v1.get("对用户的称呼") or v1.get("昵称")
                or persona.get("昵称") or persona.get("姓名") or "")

    attachment = (user.get("依恋类型") or {}).get("判断") or ""
    if attachment not in ATTACHMENT_TWEAK:
        attachment = "未知"

    text = render(kind, nickname=nickname, detail=detail, voice=voice,
                  corrections=corrections, length_pref=length_pref,
                  budget=budget, attachment=attachment)
    return {
        "kind": kind,
        "text": text,
        "tokens": estimate_tokens(text),
        "budget": int(budget),
        "used_detail": detail or FALLBACK_DETAIL.get(kind, ""),
        "attachment": attachment,
    }


if __name__ == "__main__":
    import json
    import sys
    kind = sys.argv[1] if len(sys.argv) > 1 else "久未联系"
    out = render(kind, nickname="小美", detail="你说过想去看海",
                 voice={"语气词": ["呀"], "emoji频率": 0.8, "口头禅": ["就是说"]})
    print(out)
    print(json.dumps({"tokens": estimate_tokens(out),
                      "budget": schema.DEFAULT_INJECTION_BUDGET["关怀话术"]},
                     ensure_ascii=False))
