#!/usr/bin/env python3

DEFAULT_STYLE = {
    "role_en": "Execution Agent",
    "palette": ("#FF7548", "#0D8F87", "#FFE27A"),
    "badge": "AGENT",
    "backdrop": "grid",
    "prop": "checklist",
    "expression": "confident",
    "scene_en": "a crisp execution board and floating action stickers behind it, staged like a retro game character select screen",
    "scene_zh": "背后是清晰的执行看板和动作贴纸，像复古游戏角色选择界面",
    "mood_en": "capable, memorable, high-share social poster energy, retro arcade confidence",
    "mood_zh": "能干、好记、有海报感，带一点复古街机气质",
    "props_en": ["checklist tablet", "action stickers", "workflow board"],
    "props_zh": ["清单平板", "动作贴纸", "流程看板"],
}


ROLE_STYLE_MAP = {
    "销售线索运营助手": {
        "role_en": "Sales Pipeline Agent",
        "palette": ("#FF7548", "#0D8F87", "#FFE27A"),
        "badge": "PIPELINE",
        "backdrop": "pipeline",
        "prop": "phone",
        "expression": "confident",
        "scene_en": "a glowing CRM phone in one claw, pipeline bars and outbound mail stickers behind it",
        "scene_zh": "一只钳子里举着发亮的 CRM 手机，背后是 pipeline 柱状条和外联贴纸",
        "mood_en": "playful closer energy, sharp and proactive",
        "mood_zh": "像会推进成交的角色，机灵、主动",
        "props_en": ["CRM phone", "pipeline dashboard", "outbound mail stickers"],
        "props_zh": ["CRM 手机", "pipeline 看板", "外联贴纸"],
    },
    "招聘流程助手": {
        "role_en": "Hiring Workflow Agent",
        "palette": ("#7B61FF", "#22A699", "#FFD166"),
        "badge": "HIRING",
        "backdrop": "hiring",
        "prop": "clipboard",
        "expression": "sharp",
        "scene_en": "holding a candidate clipboard, with interview cards and calendar blocks behind it",
        "scene_zh": "拿着候选人夹板，背后是面试卡片和日历格",
        "mood_en": "fast, organized, great at moving people through stages",
        "mood_zh": "利落、有条理，像会推流程的人",
        "props_en": ["candidate clipboard", "interview cards", "calendar blocks"],
        "props_zh": ["候选人夹板", "面试卡片", "日历格"],
    },
    "客户支持助手": {
        "role_en": "Customer Support Agent",
        "palette": ("#3AA6FF", "#19A974", "#FFE27A"),
        "badge": "SUPPORT",
        "backdrop": "support",
        "prop": "headset",
        "expression": "steady",
        "scene_en": "wearing a headset, with chat bubbles, shield icons, and route arrows behind it",
        "scene_zh": "戴着耳机，背后是聊天气泡、盾牌图标和升级路线箭头",
        "mood_en": "steady, reassuring, calm under pressure",
        "mood_zh": "稳、能接住情绪、让人放心",
        "props_en": ["headset", "reply bubbles", "escalation arrows"],
        "props_zh": ["耳机", "回复气泡", "升级箭头"],
    },
    "产品内容策略助手": {
        "role_en": "Product Content Strategy Agent",
        "palette": ("#FF6B6B", "#4ECDC4", "#FFE66D"),
        "badge": "LAUNCH",
        "backdrop": "strategy",
        "prop": "megaphone",
        "expression": "curious",
        "scene_en": "holding a launch megaphone, with sticky notes, product blocks, and signal sparkles behind it",
        "scene_zh": "举着发布喇叭，背后是便利贴、产品模块和信号火花",
        "mood_en": "inventive, signal-driven, ready to frame the story",
        "mood_zh": "会看信号，也会把故事讲出来",
        "props_en": ["launch megaphone", "sticky notes", "signal sparkles"],
        "props_zh": ["发布喇叭", "便利贴", "信号火花"],
    },
    "内容协作助手": {
        "role_en": "Content Collaboration Agent",
        "palette": ("#FF8A65", "#00A19A", "#FFE082"),
        "badge": "CONTENT",
        "backdrop": "content",
        "prop": "pencil",
        "expression": "curious",
        "scene_en": "holding a chunky marker, with draft cards and title stickers behind it",
        "scene_zh": "拿着粗记号笔，背后是草稿卡片和标题贴纸",
        "mood_en": "creative, quick, always ready to turn fuzziness into a draft",
        "mood_zh": "像会把模糊想法马上写出来的角色",
        "props_en": ["marker pen", "draft cards", "title stickers"],
        "props_zh": ["记号笔", "草稿卡片", "标题贴纸"],
    },
    "沟通流程助手": {
        "role_en": "Communication Workflow Agent",
        "palette": ("#FF8A65", "#00A19A", "#FFE082"),
        "badge": "REPLY",
        "backdrop": "reply",
        "prop": "chat",
        "expression": "steady",
        "scene_en": "holding a reply card, with stacked chat bubbles and tone sliders behind it",
        "scene_zh": "拿着回复卡片，背后是聊天气泡和语气滑杆",
        "mood_en": "consistent, articulate, good at reducing communication friction",
        "mood_zh": "口径稳定、表达清楚、降低沟通摩擦",
        "props_en": ["reply card", "chat bubbles", "tone sliders"],
        "props_zh": ["回复卡片", "聊天气泡", "语气滑杆"],
    },
    "执行流程助手": {
        "role_en": "Execution Workflow Agent",
        "palette": ("#FF7548", "#0D8F87", "#FFE27A"),
        "badge": "EXEC",
        "backdrop": "grid",
        "prop": "checklist",
        "expression": "confident",
        "scene_en": "holding a checklist tablet, with progress blocks and arrows behind it",
        "scene_zh": "拿着清单平板，背后是进度方块和箭头",
        "mood_en": "fast, practical, built to keep work moving",
        "mood_zh": "实干、直接、就是推进事情",
        "props_en": ["checklist tablet", "progress blocks", "arrow stickers"],
        "props_zh": ["清单平板", "进度方块", "箭头贴纸"],
    },
    "Coding Agent": {
        "role_en": "Coding Agent",
        "palette": ("#5B8CFF", "#18A999", "#FFD166"),
        "badge": "CODE",
        "backdrop": "grid",
        "prop": "terminal",
        "expression": "sharp",
        "scene_en": "holding a compact terminal slate with patch marks and validation lights",
        "scene_zh": "拿着一块小型终端面板，上面有补丁标记和验证灯",
        "mood_en": "precise, pragmatic, forward-moving, built to turn requests into verified changes",
        "mood_zh": "精确、务实、持续推进，像能把需求改成已验证结果的角色",
        "props_en": ["terminal slate", "patch marks", "validation lights"],
        "props_zh": ["终端面板", "补丁标记", "验证灯"],
    },
}


def get_role_style(role: str) -> dict:
    style = dict(DEFAULT_STYLE)
    style.update(ROLE_STYLE_MAP.get(role, {}))
    return style


def truncate_text(text: str, limit: int) -> str:
    compact = " ".join(str(text).split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "…"


def build_badge_text(tags: list[str], fallback: str, limit: int = 20) -> str:
    chosen = [tag.strip() for tag in tags if tag and tag.strip()][:2]
    if chosen:
        return truncate_text(" · ".join(chosen), limit)
    return truncate_text(fallback, limit)


def infer_expression(role: str, persona_tags: list[str]) -> str:
    combined = " ".join([role] + list(persona_tags))
    if any(token in combined for token in ["支持", "客服", "reply", "稳", "support"]):
        return "steady"
    if any(token in combined for token in ["招聘", "候选", "hiring", "interview"]):
        return "sharp"
    if any(token in combined for token in ["产品", "内容", "策略", "draft", "signal"]):
        return "curious"
    return get_role_style(role)["expression"]


def role_theme(role: str) -> dict:
    primary, secondary, accent = get_role_style(role)["palette"]
    return {
        "background": "#FFF7DF",
        "border": "#111111",
        "accent": primary,
        "tag_colors": [accent, "#FFFFFF", secondary],
    }


def build_selfie_prompt(
    agent_name: str,
    role: str,
    tagline: str,
    capabilities: list[str],
    persona_tags: list[str] | None = None,
    lang: str = "en",
    visual_identity: dict | None = None,
) -> str:
    style = get_role_style(role)
    tags = [tag for tag in (persona_tags or []) if tag][:3]
    caps = [cap for cap in capabilities if cap][:3]
    palette = ", ".join(style["palette"])
    visual_identity = visual_identity or {}
    character_style = visual_identity.get("character_style", "agent-avatar")
    visual_brief = str(visual_identity.get("visual_brief", "")).strip()
    subject_zh = "拟人化龙虾 agent 吉祥物" if character_style == "lobster" else "拟人化 AI agent 角色"
    subject_en = "an anthropomorphic lobster agent mascot" if character_style == "lobster" else "an anthropomorphic AI agent character"

    if lang == "zh":
        prop_text = "、".join(style["props_zh"])
        caps_text = "、".join(caps) if caps else "角色感、行动力、记忆点"
        tags_text = "、".join(tags) if tags else caps_text
        return (
            f"Agent 自拍海报，角色名 {agent_name}，定位 {role}。"
            f"3/4 构图的人物头像，{subject_zh}，{style['scene_zh']}。"
            f"整体气质：{style['mood_zh']}；标准 8-bit 像素风，透明背景或完全留白背景，粗黑边，主色 {palette}，低分辨率块面，强轮廓。"
            f"只保留和能力直接相关的少量道具：{prop_text}。"
            f"让人一眼感受到：{tagline}。"
            f"人格标签：{tags_text}。能力关键词：{caps_text}。"
            f"{visual_brief}"
            f"不要堆文字，不要复杂背景，不要画场景，不要写实摄影，不要平滑渐变，不要半写实插画。"
        )

    prop_text = ", ".join(style["props_en"])
    caps_text = ", ".join(caps) if caps else "memorable, useful, shareable"
    tags_text = ", ".join(tags) if tags else caps_text
    return (
        f"Selfie-style share poster of {subject_en} named {agent_name}, {style['role_en']}. "
        f"3/4 portrait, collectible character design, {style['scene_en']}. "
        f"Mood: {style['mood_en']}. Standard 8-bit pixel art style, transparent or fully empty background, bold black outlines, readable silhouette, palette {palette}, low-resolution sprite logic. "
        f"Show abilities through a minimal set of props only: {prop_text}. "
        f"Convey this value immediately: {tagline}. Persona cues: {tags_text}. Capability keywords: {caps_text}. "
        f"{visual_brief} "
        f"No text overlay, no scenery, no interface background, no photorealism, no clutter, no smooth gradients, no painterly rendering."
    )
