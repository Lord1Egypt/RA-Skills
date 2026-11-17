from __future__ import annotations

import re
from dataclasses import dataclass


PIPELINE_PROFILES = [
    "logic",
    "character",
    "relationship",
    "voice",
    "register",
    "capability",
    "serial",
    "world",
    "process",
    "momentum",
    "salience",
    "recurrence",
    "repetition",
    "physical",
    "ai-trace",
    "ending",
    "texture",
    "style-match",
    "fidelity",
    "preservation",
    "numbers",
    "sources",
    "proofread",
]
CORE_AUTO_PROFILES = {"logic", "ai-trace", "proofread"}


@dataclass(frozen=True)
class ProfileDecision:
    profile: str
    selected: bool
    reason: str


CHARACTER_PATTERN = re.compile(
    r"[\u4e00-\u9fff]{1,4}(?:说|问|答|想|看|走|笑|哭|摇头|点头)|"
    r"\b(?:he|she|they|said|asked|replied|thought|character)\b",
    re.IGNORECASE,
)
RELATIONSHIP_PATTERN = re.compile(
    r"[“”「」『』]|(?:说|问|告诉|提到)[:：,，]|答道|董事长|总经理|掌门|师父|师兄|师姐|夫妻|丈夫|妻子|老公|老婆|"
    r"恋人|情人|出轨|秘密|敌对|盟友|上司|下属|朋友|背叛|信任|"
    r"\b(?:said|asked|told|mentioned|boss|manager|lover|spouse|husband|wife|rival|ally|secret|betray|trust)\b",
    re.IGNORECASE,
)
PHYSICAL_PATTERN = re.compile(
    r"前排|后排|左侧|右侧|座位|椅子|床|桌|门|窗|隔板|车内|房间|电梯|走廊|"
    r"站在|坐在|躺在|走到|移到|伸手|触碰|穿着|鞋|裙|外套|伤口|拿着|放下|"
    r"\b(?:front|rear|left|right|seat|chair|bed|table|door|room|corridor|moved|"
    r"reached|touched|wearing|shoes|coat|injury|carried)\b",
    re.IGNORECASE,
)
NUMBER_PATTERN = re.compile(
    r"(?:\d+(?:\.\d+)?|[零一二两三四五六七八九十百千万点]+)\s*(?:毫米|厘米|米|公里|秒|分钟|小时|次|岁|元|%|"
    r"mm|cm|km|meters?|seconds?|minutes?|hours?|times?)",
    re.IGNORECASE,
)
NARRATIVE_PATTERN = re.compile(
    r"(?:第[一二三四五六七八九十百\d]+章|上一章|前文|回想|那天|他说|她说|"
    r"走到|坐在|望着|心里|翌日|次日)|"
    r"\b(?:chapter|previously|earlier|he said|she said|walked|sat|remembered)\b",
    re.IGNORECASE,
)
DIALOGUE_MARK_PATTERN = re.compile(r"[“「『\"]")
DIALOGUE_ATTRIBUTION_PATTERN = re.compile(
    r"(?:说|问|答|道|喊|低声|笑道|反问| replied| said| asked| whispered)",
    re.IGNORECASE,
)
IMAGERY_PATTERN = re.compile(r"像|仿佛|如同|宛如|好似|犹如|\blike\b|\bas if\b", re.IGNORECASE)
DETAIL_PATTERN = re.compile(
    r"(?:[今现]年)?\d{1,3}岁|身高|体重|职业|结婚[了]?\d|任职|毕业于|"
    r"\b(?:aged?|height|weighs?|occupation|married|graduated)\b",
    re.IGNORECASE,
)
SHOW_GLOSS_PATTERN = re.compile(
    r"(?:握紧|攥紧|避开目光|垂下眼|停住脚步|手指发抖|呼吸一滞).{0,50}"
    r"(?:愤怒|紧张|害怕|犹豫|不安|羞愧|嫉妒|悲伤)",
    re.DOTALL,
)
CHAPTER_HEADING_PATTERN = re.compile(
    r"(?m)^\s*(?:#{1,6}\s*)?(?:第\s*[一二三四五六七八九十百零〇\d]+\s*[章节回卷]|"
    r"chapter\s+\d+)[^\n]*$",
    re.IGNORECASE,
)
SCENE_TIME_PATTERN = re.compile(
    r"(?:(?:凌晨|清晨|早上|上午|中午|下午|傍晚|晚上|夜里)\s*"
    r"(?:\d{1,2}|[一二三四五六七八九十两]+)\s*(?:点|时)(?:半|\d{1,2}分)?|"
    r"(?:\d{1,2}|[一二三四五六七八九十两]+)\s*点(?:半|\d{1,2}分)?|"
    r"\d{1,2}\s*时(?:\d{1,2}分)?)",
)
SCENE_PLACE_PATTERN = re.compile(
    r"[\u4e00-\u9fffA-Za-z0-9]{2,18}(?:机场|航站楼|车站|酒店|大厦|公寓|办公室|"
    r"宿舍|宫殿|广场|餐厅|咖啡馆|会所|小区|街口|路口|码头|医院|学校)",
)
SCENE_LIGHT_PATTERN = re.compile(
    r"落日|夕阳|阳光|晨光|暮色|夜色|灯光|月光|雨|雪|雾|夜风|微风|冷风",
)
SCENE_APPEARANCE_PATTERN = re.compile(
    r"身穿|穿着|外套|短裙|长裙|西装|制服|高跟鞋|平底鞋|长发|短发|妆容",
)
SCENE_FEELING_PATTERN = re.compile(
    r"莫名|说不清|无法形容|不知为何|不知道为什么|一股.{0,16}(?:感觉|情绪)|"
    r"(?:疲惫|紧张|幸福|不安|心动)中带着?",
)
FORMULAIC_INTROSPECTION_PATTERN = re.compile(
    r"不是那种.{0,45}而是|像是.{0,35}(?:又像是|却又像)|"
    r"(?:他|她|我)不知道为什么|(?:他|她|我)?莫名(?:地|其妙|就)?|"
    r"说不清(?:是什么|为什么)|无法形容(?:的|这种)",
)
REPETITION_EXPOSITION_PATTERN = re.compile(
    r"(?:他|她|我|他们|她们).{0,12}(?:知道|明白|发现|意识到|心里清楚|看在眼里)|"
    r"一边.{0,48}(?:一边|又)|(?:先|一会儿).{0,48}(?:再|一会儿)|"
    r"\b(?:he|she|they|i)\s+(?:knew|realized|understood|could see)|"
    r"\b(?:while\b.{0,80}\b(?:and|while)\b|first\b.{0,80}\bthen\b)",
    re.IGNORECASE,
)
WORLD_STRONG_PATTERN = re.compile(
    r"世界观|架空|世界规则|时代背景|历史背景|科技水平|制度设定|"
    r"(?:唐|宋|元|明|清)朝|民国|古代|赛博朋克|蒸汽朋克|修仙|魔法体系|星际|"
    r"\b(?:worldbuilding|world rules?|alternate history|historical setting|"
    r"cyberpunk|steampunk|magic system)\b",
    re.IGNORECASE,
)
PROCESS_PATTERN = re.compile(
    r"调查|侦查|研发|实验|谈判|会谈|审讯|诊断|手术|施工|经营|贷款|招标|"
    r"审判|训练|修炼|炼制|战斗|破案|制作|推演|取证|审批|"
    r"\b(?:investigat(?:e|ion)|research|experiment|negotiat(?:e|ion)|interrogation|"
    r"diagnosis|surgery|construction|trial|training|crafting|battle plan|approval)\b",
    re.IGNORECASE,
)
PROCESS_RESULT_PATTERN = re.compile(
    r"终于|成功|失败|完成|解决|达成|通过|获批|查明|证明|结果|结论|"
    r"\b(?:finally|succeeded|failed|completed|solved|approved|result|conclusion)\b",
    re.IGNORECASE,
)
REGISTER_PATTERN = re.compile(
    r"方言|口音|地域|籍贯|母语|外语|双语|多语|翻译|敬语|敬称|称谓|语气词|口头禅|"
    r"国籍|出生地|成长地|东北人|广东人|美国人|日本人|韩国人|"
    r"东北话|粤语|广东话|京片子|北京话|普通话|英语|日语|韩语|法语|西班牙语|"
    r"移民|留学|语言习惯|说话习惯|"
    r"\b(?:dialect|accent|native language|bilingual|multilingual|translation|honorific|"
    r"register|code-switch|discourse particle|speech habit|slang|idiolect|nationality|"
    r"birthplace|upbringing|American|Japanese|Korean)\b",
    re.IGNORECASE,
)
CAPABILITY_PATTERN = re.compile(
    r"战力|境界|等级|阶位|段位|修为|异能|能力|技能|招式|法术|装备|武器|伤势|"
    r"体力|法力|灵力|资源|冷却|克制|越级|突破|升级|训练|权限|权力等级|"
    r"\b(?:power level|rank|tier|ability|skill|spell|equipment|weapon|injury|stamina|"
    r"mana|resource|cooldown|counter|level up|training|authority level)\b",
    re.IGNORECASE,
)


def _match_reason(pattern: re.Pattern[str], text: str, label: str) -> tuple[bool, str]:
    match = pattern.search(text)
    if not match:
        return False, f"No {label} cues found in the draft."
    cue = match.group(0).strip()
    return True, f"Detected {label} cue: {cue!r}."


# Routing cues only: these locate interpersonal actions, not missing responses.
INTERACTION_PATTERN = re.compile(
    r"(?:双向互动|互动承接|动作回应|人物反应|无声互动)|"
    r"(?:递给|交给|递向|递到.{0,12}手|伸手.{0,12}(?:他|她|对方)|"
    r"(?:拉住|扶住|碰了碰|拍了拍|靠近|走向|跟着|跟上)(?:他|她|对方)|"
    r"(?:他|她|我|对方).{0,12}(?:跟来|跟过来|没有回应|没有反应))|"
    r"\b(?:wordless interaction|reciprocal response|interaction uptake|missing reactions?)\b|"
    r"\b(?:hand(?:s|ed|ing)?|pass(?:es|ed|ing)?|offer(?:s|ed|ing)?)\s+(?:him|her|them|me|you)\b|"
    r"\b(?:hand(?:s|ed|ing)?|pass(?:es|ed|ing)?|offer(?:s|ed|ing)?)\b[^.!?\n]{0,55}\bto (?:him|her|them|me|you)\b|"
    r"\b(?:touch(?:es|ed|ing)?|approach(?:es|ed|ing)?|follow(?:s|ed|ing)?)\s+(?:him|her|them|me|you)\b",
    re.IGNORECASE,
)


def has_directed_interaction(text: str) -> bool:
    return bool(INTERACTION_PATTERN.search(text))


def _voice_reason(text: str, context_active: bool = False) -> tuple[bool, str]:
    if has_directed_interaction(text):
        return True, "Directed interpersonal action requires recipient and bidirectional uptake review."
    dialogue_marks = len(DIALOGUE_MARK_PATTERN.findall(text))
    attributions = len(DIALOGUE_ATTRIBUTION_PATTERN.findall(text))
    sustained = dialogue_marks >= 4 and attributions >= 2
    paired = dialogue_marks >= 2 and attributions >= 2
    context_backed = context_active and dialogue_marks >= 2 and attributions >= 1
    selected = sustained or paired or context_backed
    if not selected:
        return False, "No sustained or context-backed multi-speaker dialogue cues found in the draft."
    if sustained:
        basis = "sustained"
    elif paired:
        basis = "paired"
    else:
        basis = "context-backed"
    return True, (
        f"Detected {basis} dialogue: {dialogue_marks} openings and "
        f"{attributions} attribution cues."
    )


def _register_reason(text: str, context: str = "") -> tuple[bool, str]:
    dialogue_marks = len(DIALOGUE_MARK_PATTERN.findall(text))
    attributions = len(DIALOGUE_ATTRIBUTION_PATTERN.findall(text))
    register_match = REGISTER_PATTERN.search("\n".join((text, context)))
    selected = bool(register_match) and dialogue_marks >= 2 and attributions >= 1
    if not selected:
        return False, "No dialogue combined with explicit language, dialect, honorific, or register evidence."
    return True, f"Detected dialogue with register evidence: {register_match.group(0)!r}."


def _capability_reason(text: str, context: str = "") -> tuple[bool, str]:
    if not context:
        return False, "No continuity context was supplied for capability-state comparison."
    match = CAPABILITY_PATTERN.search("\n".join((text, context)))
    if not match:
        return False, "No power, ability, equipment, injury, resource, or authority constraint was found."
    return True, f"Detected context-backed capability constraint: {match.group(0)!r}."


def _serial_reason(text: str, context_active: bool) -> tuple[bool, str]:
    if not context_active:
        return False, "No prior chapter or continuity context was supplied."
    match = NARRATIVE_PATTERN.search(text)
    if not match:
        return False, "Context exists, but the draft has no serialized narrative cue."
    return True, f"Prior context supplied with serialized narrative cue: {match.group(0)!r}."


def _longest_short_paragraph_run(text: str) -> int:
    longest = current = 0
    for paragraph in (part.strip() for part in re.split(r"\n\s*\n", text)):
        if paragraph and len(paragraph) <= 24:
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest


def _texture_reason(text: str) -> tuple[bool, str]:
    imagery = len(IMAGERY_PATTERN.findall(text))
    detail = len(DETAIL_PATTERN.findall(text))
    short_run = _longest_short_paragraph_run(text)
    show_gloss = bool(SHOW_GLOSS_PATTERN.search(text))
    opening_stack = _has_scene_opening_stack(text)
    introspection = len(FORMULAIC_INTROSPECTION_PATTERN.findall(text))
    narrative = bool(NARRATIVE_PATTERN.search(text) or CHARACTER_PATTERN.search(text))
    selected = narrative and (
        imagery >= 5
        or detail >= 3
        or short_run >= 4
        or show_gloss
        or opening_stack
        or introspection >= 3
    )
    if not selected:
        return False, (
            "No dense imagery, detail inventory, fragment run, cinematic opening stack, "
            "formulaic introspection, or show-then-gloss cluster found."
        )
    return True, (
        "Detected prose-texture cues: "
        f"imagery={imagery}, detail={detail}, short-paragraph-run={short_run}, "
        f"show-then-gloss={'yes' if show_gloss else 'no'}, "
        f"opening-stack={'yes' if opening_stack else 'no'}, introspection={introspection}."
    )


def _scene_opening_cues(fragment: str) -> int:
    patterns = (
        SCENE_TIME_PATTERN,
        SCENE_PLACE_PATTERN,
        SCENE_LIGHT_PATTERN,
        SCENE_APPEARANCE_PATTERN,
        SCENE_FEELING_PATTERN,
    )
    return sum(bool(pattern.search(fragment)) for pattern in patterns)


def _has_scene_opening_stack(text: str) -> bool:
    openings = [text[:700]]
    openings.extend(text[match.end() : match.end() + 700] for match in CHAPTER_HEADING_PATTERN.finditer(text))
    return any(_scene_opening_cues(opening) >= 4 for opening in openings)


def _momentum_reason(text: str) -> tuple[bool, str]:
    headings = len(CHAPTER_HEADING_PATTERN.findall(text))
    continuation_marks = len(re.findall(r"待续|未完待续|下回|下一章|to be continued", text, re.IGNORECASE))
    selected = headings >= 2 or continuation_marks >= 2
    if not selected:
        return False, "No multi-chapter or repeated continuation structure found in the draft."
    return True, (
        "Detected serial momentum structure: "
        f"chapter-headings={headings}, continuation-marks={continuation_marks}."
    )


def _world_reason(text: str) -> tuple[bool, str]:
    match = WORLD_STRONG_PATTERN.search(text)
    if not match:
        return False, "No explicit era, world-rule, technology-system, or speculative-setting cue found."
    return True, f"Detected explicit world-constraint cue: {match.group(0)!r}."


def _process_reason(text: str) -> tuple[bool, str]:
    cues = list(PROCESS_PATTERN.finditer(text))
    has_result = bool(PROCESS_RESULT_PATTERN.search(text))
    selected = len(cues) >= 2 or (bool(cues) and has_result)
    if not selected:
        return False, "No sustained consequential process or process-to-result cue found."
    return True, (
        f"Detected consequential process cues={len(cues)} and "
        f"result cue={'yes' if has_result else 'no'}."
    )


def _salience_reason(text: str) -> tuple[bool, str]:
    paragraphs = [part for part in re.split(r"\n\s*\n", text) if part.strip()]
    narrative = bool(NARRATIVE_PATTERN.search(text) or CHARACTER_PATTERN.search(text))
    selected = narrative and len(text) >= 4000 and len(paragraphs) >= 12
    if not selected:
        return False, "Draft is not a sufficiently long narrative for a separate attention-budget pass."
    return True, (
        f"Detected long narrative suitable for attention budgeting: "
        f"characters={len(text)}, paragraphs={len(paragraphs)}."
    )


def _recurrence_reason(text: str) -> tuple[bool, str]:
    headings = len(CHAPTER_HEADING_PATTERN.findall(text))
    if headings < 3:
        return False, "Fewer than three chapter headings; structural recurrence cannot be established."
    return True, f"Detected {headings} chapters for cross-chapter structural fingerprinting."


def _repetition_reason(text: str, serious_document: bool) -> tuple[bool, str]:
    if serious_document:
        return False, "Repetition/exposition review is reserved for narrative prose, not serious factual documents."
    markers = len(REPETITION_EXPOSITION_PATTERN.findall(text))
    narrative = bool(NARRATIVE_PATTERN.search(text) or CHARACTER_PATTERN.search(text))
    selected = narrative and len(text) >= 1400 and markers >= 4
    if not selected:
        return False, "No sufficiently long narrative with repeated explanation or choreography cues found."
    return True, f"Detected narrative repetition/exposition cues={markers} across {len(text)} characters."


def detect_audit_profiles(
    draft: str,
    reference_active: bool = False,
    original_active: bool = False,
    context_active: bool = False,
    source_active: bool = False,
    serious_document: bool = False,
    context: str = "",
    source_eligible: bool | None = None,
) -> list[ProfileDecision]:
    factual_sources_enabled = serious_document if source_eligible is None else source_eligible
    optional = {
        "character": _match_reason(CHARACTER_PATTERN, draft, "character-action or voice"),
        "relationship": _match_reason(RELATIONSHIP_PATTERN, draft, "dialogue or relationship"),
        "voice": (
            (False, "Fiction interaction review is excluded for serious documents.")
            if serious_document else _voice_reason(draft, context_active)
        ),
        "register": _register_reason(draft, context),
        "capability": _capability_reason(draft, context),
        "serial": _serial_reason(draft, context_active),
        "world": _world_reason(draft),
        "process": _process_reason(draft),
        "momentum": _momentum_reason(draft),
        "salience": _salience_reason(draft),
        "recurrence": _recurrence_reason(draft),
        "repetition": _repetition_reason(draft, serious_document),
        "physical": _match_reason(PHYSICAL_PATTERN, draft, "space, movement, appearance, or prop"),
        "texture": _texture_reason(draft),
        "numbers": _match_reason(NUMBER_PATTERN, draft, "exact-number"),
        "style-match": (
            reference_active,
            "Explicit reference material or style direction was supplied."
            if reference_active
            else "No explicit reference material or style direction was supplied.",
        ),
        "fidelity": (
            original_active,
            "An explicit pre-rewrite original was supplied."
            if original_active
            else "No pre-rewrite --original file was supplied.",
        ),
        "preservation": (
            False,
            "High-cost source-to-rewrite voice comparison; select it explicitly when needed."
            if original_active
            else "No pre-rewrite --original file was supplied.",
        ),
        "ending": (
            False,
            "Covered by the core ai-trace stage; select ending explicitly for an isolated pass.",
        ),
        "sources": (
            source_active and factual_sources_enabled,
            "Supplied factual sources and an eligible factual document type were detected."
            if source_active and factual_sources_enabled
            else (
                "Source files were supplied, but the draft is not a serious factual document."
                if source_active
                else "No factual --source files were supplied."
            ),
        ),
    }
    decisions: list[ProfileDecision] = []
    for profile in PIPELINE_PROFILES:
        if profile in CORE_AUTO_PROFILES:
            decisions.append(
                ProfileDecision(
                    profile=profile,
                    selected=True,
                    reason="Core pipeline stage retained for every draft.",
                )
            )
        else:
            selected, reason = optional[profile]
            decisions.append(ProfileDecision(profile, selected, reason))
    return decisions
