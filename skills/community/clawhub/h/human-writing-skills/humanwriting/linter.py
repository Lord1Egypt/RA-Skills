from __future__ import annotations

import json
import math
import re
from dataclasses import asdict, dataclass
from pathlib import Path


SEVERITY_WEIGHT = {"low": 2, "medium": 5, "high": 9}
NARRATIVE_STYLES = {"fiction", "webnovel", "self-media"}
FICTION_STYLES = {"fiction", "webnovel"}
ARGUMENTATIVE_STYLES = {"argumentative", "self-media"}
CHAPTER_HEADING_PATTERN = re.compile(
    r"(?m)^\s*(?:#{1,6}\s*)?(?:第\s*[一二三四五六七八九十百零〇\d]+\s*[章节回卷話话](?:\s+[^\n]{1,60})?|"
    r"(?:chapter|chapitre|cap[ií]tulo|capitulum|الفصل)\s+[^\n]{1,80})$",
    re.IGNORECASE,
)
MARKDOWN_HEADING_PATTERN = re.compile(
    r"(?m)^[ \t]{0,3}(?P<marks>#{1,6})[ \t]+(?P<label>[^#\n].*?)[ \t]*$"
)
BOLD_STANDALONE_HEADING_PATTERN = re.compile(
    r"(?m)^[ \t]*(?:\*\*|__)(?P<label>[^\n]{1,80}?)(?:\*\*|__)[ \t]*$"
)
STANDALONE_PARAGRAPH_PATTERN = re.compile(
    r"(?ms)(?:(?<=\n\n)|\A)[ \t]*(?P<label>[^\n]{1,60}?)[ \t]*(?=\n\n|\Z)"
)
TIME_CARD_PATTERN = re.compile(
    r"^(?:"
    r"(?:次日|翌日|第二天|当天|同日)?(?:清晨|早晨|上午|中午|下午|傍晚|晚上|夜里|深夜)"
    r"(?:\s*[零一二两三四五六七八九十百\d:：点时分半]+)?|"
    r"[零一二两三四五六七八九十百\d]+(?:天|小时|周|个月|年)(?:后|以后)|"
    r"(?:the\s+)?(?:next\s+)?(?:morning|afternoon|evening|night|dawn|noon|midnight)|"
    r"later\s+that\s+day|\d+\s+(?:minutes?|hours?|days?|weeks?|months?|years?)\s+later|"
    r"(?:翌朝|翌日|午前|午後|朝|昼|夕方|夜|深夜|その夜)(?:\s*\d{1,2}(?::\d{2}|時(?:\d{1,2}分)?)?)?|"
    r"(?:le\s+lendemain|ce\s+matin|cet\s+apr[eè]s-midi|ce\s+soir|le\s+matin|"
    r"l['’]apr[eè]s-midi|le\s+soir|la\s+nuit|midi|minuit)|"
    r"(?:a\s+la\s+ma[nñ]ana|por\s+la\s+tarde|por\s+la\s+noche|al\s+d[ií]a\s+siguiente|"
    r"esa\s+tarde|esa\s+noche|ma[nñ]ana|tarde|noche|mediod[ií]a)|"
    r"(?:de\s+manh[ãa]|[àa]\s+tarde|[àa]\s+noite|no\s+dia\s+seguinte|"
    r"na\s+manh[ãa]\s+seguinte|manh[ãa]|tarde|noite|meio-dia)|"
    r"(?:في\s+الصباح|صباحًا?|بعد\s+الظهر|في\s+المساء|مساءً|في\s+الليل|"
    r"في\s+اليوم\s+التالي|عند\s+الظهر|منتصف\s+الليل)|"
    r"(?:mane|meridie|vespere|nocte|postridie|postero\s+die|sequenti\s+die)"
    r")(?:\s*[-—:：]\s*[^\n]{1,24})?$",
    re.IGNORECASE,
)
SCENE_OPENING_CUE_PATTERNS = {
    "clock": re.compile(
        r"(?:(?:凌晨|清晨|早上|上午|中午|下午|傍晚|晚上|夜里)\s*"
        r"(?:\d{1,2}|[一二三四五六七八九十两]+)\s*(?:点|时)(?:半|\d{1,2}分)?|"
        r"(?:\d{1,2}|[一二三四五六七八九十两]+)\s*点(?:半|\d{1,2}分)?|"
        r"\d{1,2}\s*时(?:\d{1,2}分)?)"
    ),
    "place": re.compile(
        r"[\u4e00-\u9fffA-Za-z0-9]{2,18}(?:机场|航站楼|车站|酒店|大厦|公寓|办公室|"
        r"宿舍|宫殿|广场|餐厅|咖啡馆|会所|小区|街口|路口|码头|医院|学校)"
    ),
    "light-weather": re.compile(
        r"落日|夕阳|阳光|晨光|暮色|夜色|灯光|月光|雨|雪|雾|夜风|微风|冷风"
    ),
    "appearance": re.compile(
        r"身穿|穿着|外套|短裙|长裙|西装|制服|高跟鞋|平底鞋|长发|短发|妆容"
    ),
    "generalized-feeling": re.compile(
        r"莫名|说不清|无法形容|不知为何|不知道为什么|一股.{0,16}(?:感觉|情绪)|"
        r"(?:疲惫|紧张|幸福|不安|心动)中带着?"
    ),
}
FORMULAIC_INTROSPECTION_PATTERN = re.compile(
    r"不是那种.{0,45}而是|像是.{0,35}(?:又像是|却又像)|"
    r"(?:他|她|我)不知道为什么|(?:他|她|我)?莫名(?:地|其妙|就)?|"
    r"说不清(?:是什么|为什么)|无法形容(?:的|这种)"
)
FORMULAIC_CONTRAST_PATTERN = re.compile(
    r"(?:不只是|不仅仅是|不是)[^。！？!?\n]{1,80}?[，,；;]?\s*(?:而|却|更)?是|"
    r"(?:算是|更像是|是)[^。！？!?\n]{1,80}?[，,；;]\s*(?:而)?不是",
    re.IGNORECASE,
)
COMPARISON_NONMARKER_PREFIXES = ("同比", "环比", "占比", "配比", "可比", "性价比")
COMPARISON_NONMARKER_SUFFIXES = (
    "比如",
    "比例",
    "比赛",
    "比较",
    "比方",
    "比喻",
    "比重",
    "比值",
    "比率",
    "比分",
    "比特",
    "比肩",
    "比邻",
)
INFLATED_CLUSTER_PATTERN = re.compile(
    r"赋能|助力|深耕|打造|构建|全方位|多维度|新篇章|新征程|持续推进|"
    r"\b(?:delve|delving|tapestry|vibrant|crucial|robust|seamless|transformative|"
    r"multifaceted|pivotal|showcasing|underscores?|testament|evolving landscape|"
    r"beacon|foster|unleash|nuanced|intertwined|bolster)\b",
    re.IGNORECASE,
)
DOUBLE_EDGED_PATTERN = re.compile(
    r"双刃剑|双面刃|\bdouble[- ]edged sword\b|\barme [àa] double tranchant\b|"
    r"\barma de doble filo\b|\bfaca de dois gumes\b",
    re.IGNORECASE,
)
TIERED_CONNECTOR_PATTERN = re.compile(
    r"不仅如此|更重要的是|毋庸置疑(?:的是)?|不可否认(?:的是)?|进一步(?:地)?说|"
    r"\b(?:not only that|more importantly|it is undeniable that|needless to say|"
    r"furthermore|what is more)\b|\b(?:no solo eso|m[aá]s importante|sin duda)\b|"
    r"\b(?:n[aã]o s[oó] isso|mais importante|sem d[uú]vida)\b|"
    r"\b(?:non seulement|plus important|il est ind[eé]niable)\b",
    re.IGNORECASE,
)
FAKE_FINALITY_PATTERN = re.compile(
    r"(?:但|可是).{0,18}(?:已经|早已|终究).{0,12}(?:不再重要|无关紧要)|"
    r"有些事情.{0,24}(?:终究|到底).{0,12}(?:无需|不必|说不清)|"
    r"\b(?:but (?:that|it) (?:no longer|didn't) matter|some things,? (?:after all|in the end)|"
    r"none of it mattered now)\b",
    re.IGNORECASE,
)
ALIAS_CYCLING_GROUPS = (
    re.compile(r"主人公|主角|中心人物|核心人物|男主|女主"),
    re.compile(r"\b(?:protagonist|main character|central figure|hero|heroine)\b", re.IGNORECASE),
)
INLINE_HEADER_PATTERN = re.compile(
    r"(?m)^\s*[-*+]\s+(?:\*\*[^*\n]{1,47}[:：]\*\*|\*\*[^*\n]{1,48}\*\*\s*[:：])"
)
DECORATIVE_EMOJI_PATTERN = re.compile(
    "[\U0001F300-\U0001FAFF\u2600-\u27BF]",
    re.UNICODE,
)
TITLE_CASE_HEADING_PATTERN = re.compile(r"(?m)^#{1,6}\s+([A-Z][A-Za-z0-9'-]*(?:\s+[A-Z][A-Za-z0-9'-]*){2,})\s*$")
NARRATIVE_AFFECT_NOUNS = (
    r"(?:感觉|情绪|意味|不安|忐忑|焦虑|心动|悲凉|失落|恐惧|惊讶|嫉妒|"
    r"疲惫|紧张|愤怒|悲伤|羞涩|苦涩|冷意|暖意|凉意|笑意|寒意|杀意|"
    r"怒意|酸楚|惆怅|心绪|心事)"
)
VAGUE_NARRATIVE_MARKER_PATTERN = re.compile(
    rf"说不清|说不上来|道不明|莫名(?:地|其妙)?|不知为何|不知道为什么|"
    rf"难以形容|无法形容|隐约|某种(?:的)?{NARRATIVE_AFFECT_NOUNS}|"
    rf"(?:那点|这点|一丝|一股)(?:的)?{NARRATIVE_AFFECT_NOUNS}|"
    r"仿佛|像是|似乎",
    re.IGNORECASE,
)
INTERPRETIVE_NARRATION_PATTERN = re.compile(
    r"(?:他|她|我|他们|她们|这人|那人).{0,12}(?:知道|明白|发现|意识到|心里清楚|看在眼里|"
    r"心里一(?:跳|紧|沉|酸)|一时不知道|终于懂得)|"
    r"\b(?:he|she|they|i)\s+(?:knew|realized|understood|could see|felt sure|"
    r"could not help but think)\b",
    re.IGNORECASE,
)
ACTION_CHOREOGRAPHY_FRAME_PATTERN = re.compile(
    r"一边[^。！？!?\n]{1,64}(?:一边|又)|"
    r"(?:先|一会儿)[^。！？!?\n]{1,64}(?:再|一会儿)|"
    r"\b(?:while\b[^.!?\n]{1,100}\b(?:and|while)\b|first\b[^.!?\n]{1,100}\bthen\b)"
    r"|\b(?:mientras\b[^.!?\n]{1,100}\by\b|primero\b[^.!?\n]{1,100}\bluego\b)"
    r"|\b(?:pendant que\b[^.!?\n]{1,100}\bet\b|d['’]abord\b[^.!?\n]{1,100}\bpuis\b)",
    re.IGNORECASE,
)
DIALOGUE_QUOTE_PATTERN = re.compile(r"[\“\"](?P<content>[^\”\"\n]{4,240})[\”\"]")
DIALOGUE_PRESSURE_PATTERN = re.compile(
    r"[？?！!]|你|你们|请|别|不要|告诉我|回答|为什么|怎么|必须|不会|不许|"
    r"\b(?:why|how|tell me|answer|don't|do not|must|will not)\b",
    re.IGNORECASE,
)
DIALOGUE_RESPONSE_PATTERN = re.compile(
    r"没有回答|没出声|不作声|沉默|停住|停了下来|转身|抬头|低头|看向|望向|"
    r"避开|握紧|松开|推开|推过|退后|走开|站起|坐下|笑|哭|皱眉|愣住|僵住|"
    r"打断|接过|递给|拉住|抓住|靠近|移开|回头|起身|离开|不动|没动|未答|"
    r"\b(?:silence|paused|turned|looked|avoided|gripped|released|pushed|stepped|"
    r"stood|sat|laughed|cried|frowned|froze|interrupted|took|handed|left)\b",
    re.IGNORECASE,
)
DIALOGUE_TURN_PATTERN = re.compile(
    r"^\s*(?:[\“\"]|(?:他说|她说|他答|她答|他问|她问|回答|答道|回道)\s*[：:]\s*[\“\"]|"
    r"(?:he|she|they)\s+(?:said|answered|replied)\s*:\s*[\"'])",
    re.IGNORECASE,
)
ABSTRACT_PARAGRAPH_ENDING_PATTERN = re.compile(
    rf"(?:仿佛|像是|似乎|说不清|道不明|莫名|某种.{{0,12}}{NARRATIVE_AFFECT_NOUNS}|"
    rf"(?:那点|这点|一丝|一股)(?:的)?{NARRATIVE_AFFECT_NOUNS})"
    r"[^。！？!?\n]{0,80}[。！？!?]?$|"
    r"\b(?:as if|seemed|some kind of|could not explain)\b[^.!?\n]{0,80}[.!?]?$",
    re.IGNORECASE,
)
SCENE_BREAK_PATTERN = re.compile(r"(?:\*\s*\*\s*\*|-{3,}|_{3,}|#{3,})")
TERMINAL_SCENERY_PATTERN = re.compile(
    r"窗外|日头|夕阳|落日|暮色|天色|夜色|灯火|街灯|月光|阳光|车水马龙|雨幕|"
    r"\b(?:outside|window|sunset|sunlight|dusk|nightfall|city lights?|streetlights?|"
    r"rain|traffic|skyline)\b",
    re.IGNORECASE,
)
TERMINAL_TIME_DISSOLVE_PATTERN = re.compile(
    r"一寸一寸|一点一点|一分一秒|慢慢地?|渐渐|逐渐|西移|沉下|暗下|亮起|"
    r"时间.{0,12}(?:过去|流逝|停住|静止)|"
    r"\b(?:inch by inch|little by little|slowly|gradually|faded|slipped away|"
    r"drifted|time (?:passed|stilled|stood still))\b",
    re.IGNORECASE,
)
TERMINAL_STILLNESS_PATTERN = re.compile(
    r"谁也没(?:说话|开口|动)|没有人(?:说话|开口|动)|(?:一言不发|没说话|沉默不语)|"
    r"(?:静静|安静地).{0,18}(?:坐|站|躺|抱|搂|靠|看)|(?:抱|搂|靠).{0,12}(?:更紧|不放)|"
    r"\b(?:neither of them (?:spoke|moved)|no one (?:spoke|moved)|sat in silence|"
    r"stood in silence|held (?:him|her|them) tighter|said nothing)\b",
    re.IGNORECASE,
)
TERMINAL_REFLECTION_PATTERN = re.compile(
    r"不禁.{0,12}(?:想|回想|思考|反思)|(?:他|她|我|他们|她们).{0,12}(?:终于)?(?:明白|意识到|想到)|"
    r"(?:望|看).{0,12}(?:窗外|远处|夜色).{0,30}(?:想|未来|以后)|"
    r"\b(?:reflect(?:ed|ing)?|wondered|realized|thought about|looked back on|"
    r"could not help but think|couldn't help but think)\b",
    re.IGNORECASE,
)
TERMINAL_THEME_PATTERN = re.compile(
    r"仿佛|像是|似乎|意味着|预示着?|见证着?|提醒着?|告诉(?:他|她|我|他们|她们)|"
    r"补回来|弥补回来|新的开始|新篇章|未来还长|来日方长|命运|人生|生活本就|"
    r"这一刻.{0,20}(?:足够|永恒|圆满)|一切.{0,20}(?:值得|值得了|都会好)|"
    r"\b(?:as if|as though|a new beginning|new chapter|whatever came next|"
    r"what the future held|the future still lay ahead|a reminder that|a testament to|"
    r"everything (?:would|was going to) change|life (?:was|is)|love (?:was|is)|"
    r"it was enough|for the first time)\b",
    re.IGNORECASE,
)
STRONG_TERMINAL_REFLECTION_PATTERN = re.compile(
    r"不禁.{0,12}(?:反思|思考).{0,30}(?:人生|生活|未来|命运)|"
    r"(?:他|她|我|他们|她们).{0,10}(?:终于)?(?:明白|意识到).{0,35}(?:人生|生活|未来|命运|一切)|"
    r"\b(?:can(?:not|'t)|could(?: not|n't)) help but reflect\b|"
    r"\bwondered what (?:the )?future held\b|"
    r"\b(?:life|love|hope),?\s+[A-Z]?[a-z]+(?:\s+[A-Z]?[a-z]+)?\s+reflected,?\s+(?:is|was)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class PatternRule:
    rule_id: str
    category: str
    severity: str
    pattern: re.Pattern[str]
    message: str
    excluded_styles: frozenset[str] = frozenset()


@dataclass(frozen=True)
class LintFinding:
    rule_id: str
    category: str
    severity: str
    line: int
    column: int
    start: int
    end: int
    excerpt: str
    message: str


@dataclass(frozen=True)
class LintReport:
    score: int
    label: str
    confidence: str
    style: str
    character_count: int
    word_count: int
    findings: tuple[LintFinding, ...]
    disclaimer: str = (
        "This is a writing-pattern score, not evidence of AI authorship. "
        "Human writing can trigger the same patterns."
    )

    def to_dict(self) -> dict:
        result = asdict(self)
        result["findings"] = [asdict(finding) for finding in self.findings]
        return result


RULES = [
    PatternRule(
        "LEX001",
        "inflated-vocabulary",
        "medium",
        re.compile(
            r"\b(?:delve|delving|tapestry|realm|pivotal|groundbreaking|transformative|"
            r"seamless|game[- ]changer|ever[- ]evolving|testament to|a testament to|"
            r"beacon|foster|unleash|nuanced|intertwined|bolster)\b",
            re.IGNORECASE,
        ),
        "Replace abstract prestige language with a specific fact, action, or consequence.",
    ),
    PatternRule(
        "LEX002",
        "inflated-vocabulary",
        "medium",
        re.compile(r"命运的齿轮(?:已经)?(?:开始)?转动|时代的洪流|历史的车轮|一场风暴即将来临"),
        "Fate inflation announces importance instead of putting an irreversible change on the page.",
    ),
    PatternRule(
        "BODY001",
        "generic-body-cue",
        "medium",
        re.compile(r"嘴角微微(?:上扬|勾起)|眼中闪过一丝|深邃的眼眸|眸光微闪|眉头微皱"),
        "Generic body language should be replaced with character- and situation-specific behavior.",
    ),
    PatternRule(
        "BODY002",
        "melodramatic-reaction",
        "medium",
        re.compile(
            r"倒吸一(?:口|声)凉气|瞳孔(?:骤然|猛地|剧烈)?(?:紧缩|缩小|放大|地震)|"
            r"眼底翻涌着|嘴角勾起一抹(?:玩味|冷笑|嘲弄|弧度)|"
            r"周身散发出.{0,8}?(?:威压|寒意|杀气)|身形(?:猛地|骤然)?一震|"
            r"\b(?:gasp(?:ed)? in disbelief|eyes widened in shock|smirk played on (?:his|her) lips)\b",
            re.IGNORECASE,
        ),
        "Replace stock physiological cliches with concrete physical movement, focal shifts, or tactile reactions.",
        excluded_styles=frozenset({"academic-paper", "formal-document"}),
    ),
    PatternRule(
        "COT001",
        "reasoning-bleed",
        "medium",
        re.compile(
            r"究其原因|归根结底|从本质上(?:说|剖析|看|来讲)|这背后(?:所)?折射出的|"
            r"深层逻辑在于|如果深入探究不难发现|"
            r"\b(?:at its core|fundamentally speaking|the underlying rationale is)\b",
            re.IGNORECASE,
        ),
        "Avoid exposing explicit chain-of-thought analysis; weave insights naturally into observations, scenes, or actions.",
    ),
    PatternRule(
        "PSEUDO001",
        "pseudo-literary-cliche",
        "medium",
        re.compile(
            r"(?:最真实的|时代(?:的)?)底色|写下了?(?:最好的)?注脚|激起微弱的?回响|"
            r"在时间的?褶皱(?:里|中)|构成了?.{0,10}肌理|命运的?锚点|在记忆的?回廊|"
            r"\b(?:tapestry of life|rich tapestry of|etched into the fabric of|echoes of the past)\b",
            re.IGNORECASE,
        ),
        "Replace abstract pseudo-intellectual metaphors with grounded sensory details or factual proof.",
    ),
    PatternRule(
        "MEDIA001",
        "manufactured-hype",
        "medium",
        re.compile(
            r"谁懂啊(?:家人们)?|狠狠(?:共情|住了)|治愈内耗|直接封神|闭眼入|"
            r"答应我，?一定要|不允许还有人不知道|绝绝子|"
            r"\b(?:let that sink in|you won['’]t believe|obsessed with this)\b",
            re.IGNORECASE,
        ),
        "Remove manufactured social-media hype; convey authentic value through honest, grounded experience.",
        excluded_styles=frozenset({"academic-paper", "formal-document", "news-report"}),
    ),
    PatternRule(
        "EMO001",
        "emotion-label",
        "medium",
        re.compile(r"不禁感到一阵|心中涌起(?:一股|一阵)?复杂(?:的)?情绪|百感交集"),
        "Show the emotion through action, perception, contradiction, or consequence.",
    ),
    PatternRule(
        "EMO002",
        "show-then-gloss",
        "medium",
        re.compile(
            r"(?:握紧|攥紧|避开(?:了)?目光|垂下(?:了)?眼|停住(?:了)?脚步|"
            r"手指(?:微微)?发抖|呼吸(?:一滞|急促)).{0,60}?"
            r"(?:这表明|显然|说明|因为|感到|意味着).{0,20}?"
            r"(?:愤怒|紧张|害怕|犹豫|不安|羞愧|嫉妒|悲伤)",
            re.DOTALL,
        ),
        "The action already carries the emotion; remove the gloss unless it complicates or corrects the evidence.",
        excluded_styles=frozenset({"academic-paper", "formal-document", "news-report"}),
    ),
    PatternRule(
        "ATM001",
        "empty-atmosphere",
        "medium",
        re.compile(r"空气仿佛凝固|时间在这一刻静止|气氛(?:顿时|瞬间)?变得凝重"),
        "Replace generic atmosphere with a local sound, object, movement, or social reaction.",
    ),
    PatternRule(
        "STR001",
        "formulaic-contrast",
        "medium",
        re.compile(
            FORMULAIC_CONTRAST_PATTERN.pattern
            + r"|\b(?:it|this) (?:is|isn't|is not) not just .{1,100}?\bbut\b|"
            r"\bnot just .{1,100}?\bbut also\b",
            re.IGNORECASE,
        ),
        "Check whether the contrast is logically necessary; otherwise state the observation or evidence directly.",
    ),
    PatternRule(
        "TRANS001",
        "dead-transition",
        "low",
        re.compile(
            r"(?:值得注意的是|需要指出的是|综上所述|总而言之|与此同时)|"
            r"\b(?:moreover|furthermore|it is important to note|in conclusion|to summarize)\b",
            re.IGNORECASE,
        ),
        "Check whether the transition carries real causality or only announces structure.",
        excluded_styles=frozenset({"academic-paper", "formal-document", "news-report"}),
    ),
    PatternRule(
        "OPEN001",
        "generic-opening",
        "medium",
        re.compile(
            r"在当今(?:快速发展|瞬息万变|日新月异)的|随着.{0,20}的不断发展|"
            r"\bin today['’]s (?:fast-paced|rapidly evolving) world\b|\blet['’]s dive in\b",
            re.IGNORECASE,
        ),
        "Open with the subject, event, conflict, or evidence instead of generic scene-setting.",
    ),
    PatternRule(
        "CLOSE001",
        "generic-conclusion",
        "medium",
        re.compile(
            r"未来可期|让我们拭目以待|相信在不久的将来|"
            r"\b(?:the future looks bright|only time will tell|exciting times lie ahead)\b",
            re.IGNORECASE,
        ),
        "Replace the generic optimistic ending with a specific next action, limit, or unresolved pressure.",
    ),
    PatternRule(
        "CHAT001",
        "chatbot-artifact",
        "high",
        re.compile(
            r"希望这对你有所帮助|如果你愿意，我可以|如有其他问题，请随时|"
            r"\b(?:I hope this helps|let me know if you(?:'d| would) like|feel free to ask)\b",
            re.IGNORECASE,
        ),
        "Remove assistant-style offer-to-continue language from finished prose.",
    ),
    PatternRule(
        "PROMO001",
        "promotional-language",
        "medium",
        re.compile(
            r"令人叹为观止|无缝(?:衔接|体验|集成)|充满活力的|极具创新性的|"
            r"\b(?:breathtaking|cutting-edge|unlock the potential|vibrant ecosystem)\b",
            re.IGNORECASE,
        ),
        "Replace promotional adjectives with observable proof.",
    ),
    PatternRule(
        "SIGN001",
        "significance-inflation",
        "medium",
        re.compile(
            r"标志着.{0,36}(?:重要|关键|崭新|新)(?:时刻|阶段|篇章)|"
            r"(?:彰显|凸显|体现)了?.{0,32}(?:重要性|深远意义|时代价值)|"
            r"为.{0,40}奠定了?(?:坚实)?基础|"
            r"\b(?:marks? a (?:pivotal|historic|significant) moment|serves? as a testament|"
            r"reflects? broader trends?|sets? the stage for)\b",
            re.IGNORECASE,
        ),
        "State the event and evidence first; keep wider significance only when the passage proves it.",
    ),
    PatternRule(
        "ATTR001",
        "vague-attribution",
        "medium",
        re.compile(
            r"(?:有|一些|多位)?(?:专家|业内人士|观察人士|分析人士)(?:普遍)?(?:认为|指出|表示)|"
            r"(?:相关|多项|有)研究(?:普遍)?(?:表明|显示)|(?:相关|多方)数据显示|"
            r"\b(?:experts? (?:believe|argue|say)|observers? (?:note|suggest)|"
            r"industry reports? (?:say|suggest)|studies (?:show|suggest))\b",
            re.IGNORECASE,
        ),
        "Name the source and supported claim, or remove the borrowed authority.",
    ),
    PatternRule(
        "CHALLENGE001",
        "formulaic-challenge-closure",
        "medium",
        re.compile(
            r"尽管.{0,90}(?:挑战|困难|问题).{0,120}(?:仍然|依然|仍|继续).{0,36}(?:发展|前行|繁荣|增长|迈进)|"
            r"\bdespite.{0,100}challenges?.{0,120}(?:continues? to|remains?)\b",
            re.IGNORECASE | re.DOTALL,
        ),
        "Replace the challenge wrapper with the specific constraint, response, and unresolved result.",
    ),
    PatternRule(
        "COPULA001",
        "elaborate-copula",
        "low",
        re.compile(
            r"\b(?:serves? as|stands? as|boasts?|holds? the distinction of being)\b",
            re.IGNORECASE,
        ),
        "Check whether a simple is, has, or direct verb would carry the same meaning more clearly.",
    ),
    PatternRule(
        "ING001",
        "decorative-participle",
        "low",
        re.compile(
            r",\s*(?:highlighting|showcasing|underscoring|reflecting|symbolizing|ensuring)\b",
            re.IGNORECASE,
        ),
        "Verify that the appended analysis adds evidence rather than announcing significance.",
    ),
    PatternRule(
        "RANGE001",
        "range-rhetoric",
        "medium",
        re.compile(
            r"从[^，。！？\n]{1,36}到[^，。！？\n]{1,36}[，,；;]\s*从[^，。！？\n]{1,36}到|"
            r"\bfrom\s+[^,.;]{1,50}\s+to\s+[^,.;]{1,50}[,;]\s*from\s+[^,.;]{1,50}\s+to\b",
            re.IGNORECASE,
        ),
        "Check whether both ranges share a meaningful axis; otherwise list the actual covered items.",
    ),
    PatternRule(
        "HEDGE001",
        "stacked-hedging",
        "medium",
        re.compile(
            r"(?:可能|或许|大概).{0,12}(?:可能|或许|大概)|"
            r"\b(?:could potentially|may perhaps|might possibly)\b",
            re.IGNORECASE,
        ),
        "Keep one calibrated hedge and remove the stack.",
    ),
    PatternRule(
        "PREC001",
        "false-precision",
        "low",
        re.compile(
            r"(?:\d+(?:\.\d+)?|[零一二两三四五六七八九十百千万点]+)\s*"
            r"(?:毫米|厘米|秒|次|mm|cm|seconds?|times?)",
            re.IGNORECASE,
        ),
        "Verify that the narrator or character has a reason to know this exact micro-measurement.",
        excluded_styles=frozenset({"academic-paper", "formal-document", "news-report"}),
    ),
    PatternRule(
        "SYN001",
        "possible-omission",
        "medium",
        re.compile(
            r"(?:把|被|让|使|给|向|往|从|对|对于|跟|与|和|或|但|却|而|"
            r"因为|所以|如果|虽然|不仅|不但|为了|通过|根据|关于|比)"
            r"\s*(?=[。！？!?；;]|$)"
        ),
        "A function word or connector is left without its required constituent; restore the missing slot or confirm an intentional fragment.",
    ),
]

DYNAMIC_RULE_CATALOG = [
    ("REP001", "exact-sentence-recurrence", "medium", "A non-trivial sentence repeats after the scene has moved."),
    ("RHYTHM001", "uniform-rhythm", "medium", "Sentence lengths are unusually uniform for the selected style."),
    ("PUNCT001", "dash-density", "low", "Em-dash use clusters too tightly to read as genuine interruption or turn."),
    ("ARG001", "double-edged-sword-density", "low", "A double-edged-sword metaphor repeats in argumentative prose."),
    ("ARG002", "tiered-connector-density", "low", "Layered logical connectors announce hierarchy more often than they add reasoning."),
    ("END001", "reflective-bookend", "medium", "A narrative exit adds reflective scenery or thematic closure after the last material change."),
    ("END002", "false-finality", "low", "A terminal pseudo-renunciation may simulate depth without changing the scene state."),
    ("NAT001", "repeated-scene-recipe", "medium", "Narrative paragraphs repeat the same scene-entry formula."),
    ("NAT002", "vague-affect-density", "low", "Vague affect markers cluster without concrete evidence."),
    ("NAT003", "abstract-paragraph-closure", "low", "Paragraph exits repeatedly settle on abstraction instead of a changed state."),
    ("NAT004", "orphaned-interaction", "medium", "Pressure-bearing dialogue or action lacks uptake or an explicit deferral."),
    ("NAT005", "interpretive-narration-recurrence", "low", "Narration repeatedly explains what nearby action or dialogue already showed."),
    ("NAT006", "action-choreography-recurrence", "low", "The same multi-action frame recurs at high density."),
    ("STR002", "comparison-ladder", "medium", "A sentence chains multiple comparisons."),
    ("STR003", "contrast-density", "medium", "Formulaic contrast repeats at passage scale."),
    ("STR004", "comparison-ladder-density", "high", "A sentence stacks three or more decorative comparisons."),
    ("LEX003", "inflated-vocabulary-density", "medium", "Prestige vocabulary clusters instead of carrying evidence."),
    ("ALIAS001", "alias-cycling", "low", "Narration rotates labels for the same character without a viewpoint reason."),
    ("FORMAT001", "narrative-mini-heading", "medium", "A narrative mini-heading substitutes for a prose transition."),
    ("FORMAT002", "time-card-heading", "medium", "A standalone time card replaces a natural scene bridge."),
    ("FORMAT003", "title-case-heading", "low", "A decorative title-case heading may fragment narrative flow."),
    ("IMG001", "imagery-density", "low", "Sensory imagery accumulates faster than scene pressure changes."),
    ("INFO001", "detail-inventory", "low", "Description inventories details at equal intensity rather than selecting by viewpoint pressure."),
    ("OPEN002", "cinematic-opening-stack", "low", "A scene opening stacks clock, location, weather, appearance, and generalized feeling."),
    ("EMO003", "body-cue-cluster", "low", "Generic body cues recur as a substitute for situated behavior."),
    ("RESET001", "scenic-chapter-reset", "medium", "A new chapter restarts with scenery before carrying prior pressure forward."),
    ("PARA001", "fragment-run", "medium", "Short paragraphs run together without distinct turns."),
]


def lint_rule_catalog() -> list[dict[str, str]]:
    """Return stable rule metadata for CLI, CI, and editor integrations."""

    items = [
        {"id": rule.rule_id, "category": rule.category, "severity": rule.severity, "message": rule.message}
        for rule in RULES
    ]
    items.extend(
        {"id": rule_id, "category": category, "severity": severity, "message": message}
        for rule_id, category, severity, message in DYNAMIC_RULE_CATALOG
    )
    return sorted(items, key=lambda item: item["id"])


MASK_PATTERNS = [
    re.compile(r"```.*?```", re.DOTALL),
    re.compile(r"`[^`\n]+`"),
    re.compile(r"(?m)^\s*>.*$"),
    re.compile(r"https?://\S+"),
]


def _mask_ignored_regions(text: str) -> str:
    chars = list(text)
    for pattern in MASK_PATTERNS:
        for match in pattern.finditer(text):
            for index in range(match.start(), match.end()):
                if chars[index] not in "\r\n":
                    chars[index] = " "
    return "".join(chars)


def _line_column(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    previous_newline = text.rfind("\n", 0, offset)
    column = offset - previous_newline
    return line, column


def _finding_from_span(
    text: str,
    rule_id: str,
    category: str,
    severity: str,
    start: int,
    end: int,
    message: str,
) -> LintFinding:
    line, column = _line_column(text, start)
    excerpt = text[start:end].replace("\n", " ").strip()
    return LintFinding(rule_id, category, severity, line, column, start, end, excerpt, message)


def _sentence_lengths(text: str) -> list[int]:
    sentences = [part.strip() for part in re.split(r"[。！？.!?]+", text) if part.strip()]
    return [len(re.findall(r"[\u4e00-\u9fff]|\b[\w'-]+\b", sentence)) for sentence in sentences]


def _paragraph_spans(text: str) -> list[tuple[int, int, str]]:
    return [
        (match.start(), match.end(), match.group(0).strip())
        for match in re.finditer(r"\S.*?(?=\n\s*\n|\Z)", text, re.DOTALL)
        if match.group(0).strip()
    ]


def _sentence_spans(text: str) -> list[tuple[int, int, str]]:
    return [
        (match.start(), match.end(), match.group(0))
        for match in re.finditer(r"[^。！？!?\n]+[。！？!?]?", text)
        if match.group(0).strip()
    ]


def _normalized_sentence_for_repetition(sentence: str) -> str:
    """Keep only enough surface form to catch verbatim, non-trivial echoes."""
    return re.sub(r"[^\w\u4e00-\u9fff]+", "", sentence).casefold()


def _exact_sentence_repetition_findings(
    text: str,
    masked: str,
    allowed: set[str],
) -> list[LintFinding]:
    if "REP001" in allowed or "exact-sentence-recurrence" in allowed:
        return []
    seen: dict[str, tuple[int, int]] = {}
    for start, end, sentence in _sentence_spans(masked):
        normalized = _normalized_sentence_for_repetition(sentence)
        if len(normalized) < 18:
            continue
        earlier = seen.get(normalized)
        if earlier is not None and start - earlier[1] >= 24:
            return [
                _finding_from_span(
                    text,
                    "REP001",
                    "exact-sentence-recurrence",
                    "medium",
                    start,
                    end,
                    "A non-trivial sentence repeats verbatim after the scene has moved. Keep it only when the return changes speaker, evidence, consequence, or meaning; otherwise cut, merge, or replace the echo with the next state change.",
                )
            ]
        seen.setdefault(normalized, (start, end))
    return []


def _terminal_paragraphs(masked: str) -> list[tuple[int, int, str]]:
    paragraphs = _paragraph_spans(masked)
    if not paragraphs:
        return []
    indexes = {len(paragraphs) - 1}
    for index, (_, _, paragraph) in enumerate(paragraphs):
        label = paragraph.strip()
        if index > 0 and (
            CHAPTER_HEADING_PATTERN.fullmatch(label)
            or SCENE_BREAK_PATTERN.fullmatch(label)
        ):
            indexes.add(index - 1)
    return [paragraphs[index] for index in sorted(indexes)]


def _reflective_bookend_span(fragment: str) -> tuple[int, int] | None:
    sentences = _sentence_spans(fragment)
    if not sentences:
        return None
    for width in range(1, min(3, len(sentences)) + 1):
        start = sentences[-width][0]
        suffix = fragment[start:].strip()
        leading = len(fragment[start:]) - len(fragment[start:].lstrip())
        span_start = start + leading
        if STRONG_TERMINAL_REFLECTION_PATTERN.search(suffix):
            return span_start, len(fragment)
        patterns = (
            TERMINAL_SCENERY_PATTERN,
            TERMINAL_TIME_DISSOLVE_PATTERN,
            TERMINAL_STILLNESS_PATTERN,
            TERMINAL_REFLECTION_PATTERN,
            TERMINAL_THEME_PATTERN,
        )
        cues = sum(bool(pattern.search(suffix)) for pattern in patterns)
        interpretive = bool(
            TERMINAL_REFLECTION_PATTERN.search(suffix)
            or TERMINAL_THEME_PATTERN.search(suffix)
        )
        if cues >= 3 and interpretive:
            return span_start, len(fragment)
    return None


def _comparative_bi_offsets(sentence: str) -> list[int]:
    offsets: list[int] = []
    for match in re.finditer("比", sentence):
        index = match.start()
        if any(sentence.startswith(term, index) for term in COMPARISON_NONMARKER_SUFFIXES):
            continue
        if any(
            sentence[max(0, index - len(term) + 1) : index + 1] == term
            for term in COMPARISON_NONMARKER_PREFIXES
        ):
            continue
        offsets.append(index)
    return offsets


def _coefficient_of_variation(values: list[int]) -> float:
    if not values:
        return 0.0
    mean = sum(values) / len(values)
    if mean == 0:
        return 0.0
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    return math.sqrt(variance) / mean


def _chapter_opening_spans(text: str, width: int = 700) -> list[tuple[int, int]]:
    return [
        (match.end(), min(len(text), match.end() + width))
        for match in CHAPTER_HEADING_PATTERN.finditer(text)
    ]


def _narrative_heading_findings(
    text: str,
    masked: str,
    allowed: set[str],
) -> list[LintFinding]:
    findings: list[LintFinding] = []
    occupied: list[tuple[int, int]] = []

    def add_finding(start: int, end: int, label: str) -> None:
        if CHAPTER_HEADING_PATTERN.fullmatch(label.strip()):
            return
        is_time_card = bool(TIME_CARD_PATTERN.fullmatch(label.strip()))
        rule_id = "HEAD002" if is_time_card else "HEAD001"
        category = "narrative-time-card" if is_time_card else "narrative-mini-heading"
        if rule_id in allowed or category in allowed:
            return
        message = (
            "This standalone time label substitutes for a narrative transition; carry prior "
            "residue through elapsed time into the first new action, or use an intentional "
            "scene-break marker when a hard cut is the point."
            if is_time_card
            else "This mini-heading segments narrative prose; remove it unless the requested "
            "form requires headings, then bridge scenes through cause, residue, elapsed time, "
            "perception, or changed pressure."
        )
        findings.append(
            _finding_from_span(text, rule_id, category, "high", start, end, message)
        )
        occupied.append((start, end))

    for match in MARKDOWN_HEADING_PATTERN.finditer(masked):
        line = match.group(0).strip()
        if CHAPTER_HEADING_PATTERN.fullmatch(line):
            continue
        if match.start() == len(masked) - len(masked.lstrip()) and match.group("marks") == "#":
            continue
        add_finding(match.start(), match.end(), match.group("label"))

    for match in BOLD_STANDALONE_HEADING_PATTERN.finditer(masked):
        if any(match.start() < end and match.end() > start for start, end in occupied):
            continue
        add_finding(match.start(), match.end(), match.group("label"))

    for match in STANDALONE_PARAGRAPH_PATTERN.finditer(masked):
        if any(match.start() < end and match.end() > start for start, end in occupied):
            continue
        label = match.group("label").strip()
        if TIME_CARD_PATTERN.fullmatch(label):
            add_finding(match.start(), match.end(), label)
    return findings


def _scene_opening_cues(fragment: str) -> set[str]:
    return {
        name
        for name, pattern in SCENE_OPENING_CUE_PATTERNS.items()
        if pattern.search(fragment)
    }


def _narrative_naturalness_findings(
    text: str,
    masked: str,
    style: str,
    allowed: set[str],
) -> list[LintFinding]:
    if style not in NARRATIVE_STYLES:
        return []

    findings: list[LintFinding] = []
    paragraphs = _paragraph_spans(masked)

    def enabled(rule_id: str, category: str) -> bool:
        return rule_id not in allowed and category not in allowed

    # A single cinematic opening can be useful. Repeated fingerprints across a
    # passage are the signal that the writer is reusing a presentation recipe.
    opening_candidates: list[tuple[int, int, tuple[str, ...]]] = []
    for start, end, paragraph in paragraphs:
        fragment = paragraph[:320]
        cues = set(_scene_opening_cues(fragment))
        if re.search(r"清晨|早上|上午|中午|下午|傍晚|晚上|夜里|深夜|黎明|次日", fragment):
            cues.add("time")
        if VAGUE_NARRATIVE_MARKER_PATTERN.search(fragment):
            cues.add("affect")
        if len(cues) >= 4:
            opening_candidates.append((start, end, tuple(sorted(cues))))
    fingerprints: dict[tuple[str, ...], list[tuple[int, int]]] = {}
    for start, end, fingerprint in opening_candidates:
        fingerprints.setdefault(fingerprint, []).append((start, end))
    repeated_fingerprints = [spans for spans in fingerprints.values() if len(spans) >= 3]
    broad_recipe_count = sum(len(cues) >= 4 for _, _, cues in opening_candidates)
    if (
        len(opening_candidates) >= 4
        and (repeated_fingerprints or broad_recipe_count >= 4)
        and enabled("NAT001", "repeated-scene-recipe")
    ):
        start, end, _ = opening_candidates[0]
        findings.append(
            _finding_from_span(
                text,
                "NAT001",
                "repeated-scene-recipe",
                "medium",
                start,
                min(end, start + 180),
                "Several narrative openings reuse the same time/weather, setting, appearance, and feeling bundle; vary the entry point and carry forward scene pressure.",
            )
        )

    vague_markers = list(VAGUE_NARRATIVE_MARKER_PATTERN.finditer(masked))
    if (
        len(vague_markers) >= 6
        and len(vague_markers) * 220 >= max(len(masked), 1)
        and enabled("NAT002", "vague-affect-recurrence")
    ):
        first = vague_markers[0]
        findings.append(
            _finding_from_span(
                text,
                "NAT002",
                "vague-affect-recurrence",
                "medium",
                first.start(),
                first.end(),
                "Vague affect and perception markers recur at high density; keep meaningful uncertainty, but replace repeated labels with owned evidence, action, or consequence.",
            )
        )

    interpretive_matches = list(INTERPRETIVE_NARRATION_PATTERN.finditer(masked))
    interpretive_paragraphs = {
        index
        for index, (start, end, _) in enumerate(paragraphs)
        if any(start <= match.start() < end for match in interpretive_matches)
    }
    if (
        len(interpretive_matches) >= 4
        and len(interpretive_matches) * 1000 >= max(len(masked), 1)
        and len(interpretive_paragraphs) >= 3
        and enabled("NAT005", "interpretive-narration-recurrence")
    ):
        first = interpretive_matches[0]
        findings.append(
            _finding_from_span(
                text,
                "NAT005",
                "interpretive-narration-recurrence",
                "low",
                first.start(),
                first.end(),
                "Narration repeatedly names what nearby dialogue or action can already show. Keep interpretations that add uncertainty, a misreading, or a consequence; otherwise let the evidence carry the beat.",
            )
        )

    choreography_matches = list(ACTION_CHOREOGRAPHY_FRAME_PATTERN.finditer(masked))
    if (
        len(choreography_matches) >= 5
        and len(choreography_matches) * 900 >= max(len(masked), 1)
        and enabled("NAT006", "action-choreography-recurrence")
    ):
        first = choreography_matches[0]
        findings.append(
            _finding_from_span(
                text,
                "NAT006",
                "action-choreography-recurrence",
                "low",
                first.start(),
                first.end(),
                "The same multi-action frame recurs at high density. Keep deliberate rhythm, but vary the next beat through a changed choice, interruption, consequence, or viewpoint-selected detail instead of another inventory.",
            )
        )

    findings.extend(_exact_sentence_repetition_findings(text, masked, allowed))

    if enabled("END001", "reflective-bookend"):
        for start, end, _ in _terminal_paragraphs(masked):
            raw_fragment = masked[start:end]
            fragment = raw_fragment.strip()
            fragment_offset = start + raw_fragment.find(fragment)
            span = _reflective_bookend_span(fragment)
            if span is None:
                continue
            relative_start, relative_end = span
            findings.append(
                _finding_from_span(
                    text,
                    "END001",
                    "reflective-bookend",
                    "medium",
                    fragment_offset + relative_start,
                    fragment_offset + relative_end,
                    "This terminal tail stacks reflection, stillness, scenery, passing time, or thematic explanation after the last concrete change. Test deleting it first; keep or replace it only if it changes choice, knowledge, consequence, document function, or the meaning of a concrete detail.",
                )
            )

    if enabled("END002", "false-finality"):
        for start, end, _ in _terminal_paragraphs(masked):
            fragment = masked[start:end]
            match = FAKE_FINALITY_PATTERN.search(fragment)
            if match is None:
                continue
            findings.append(
                _finding_from_span(
                    text,
                    "END002",
                    "false-finality",
                    "low",
                    start + match.start(),
                    start + match.end(),
                    "A terminal pseudo-renunciation may substitute for a changed consequence. Keep it only when the scene has earned the shift; otherwise end on the concrete choice, object, interruption, or unresolved pressure.",
                )
            )

    abstract_endings = [
        (start, end)
        for start, end, paragraph in paragraphs
        if ABSTRACT_PARAGRAPH_ENDING_PATTERN.search(paragraph)
    ]
    if (
        len(abstract_endings) >= 4
        and len(abstract_endings) * 3 >= max(len(paragraphs), 1)
        and enabled("NAT003", "abstract-paragraph-closure")
    ):
        start, end = abstract_endings[0]
        findings.append(
            _finding_from_span(
                text,
                "NAT003",
                "abstract-paragraph-closure",
                "low",
                start,
                min(end, start + 180),
                "Many paragraphs close on an abstract feeling or polished image; let some exits land on a changed object, action, interruption, or unanswered pressure.",
            )
        )

    # Deterministic lint only reports a cluster. It does not demand a reply to
    # harmless talk and leaves nuanced interaction analysis to the audit module.
    orphaned: list[tuple[int, int]] = []
    for paragraph_index, (p_start, p_end, _) in enumerate(paragraphs):
        for quote in DIALOGUE_QUOTE_PATTERN.finditer(masked[p_start:p_end]):
            absolute_start = p_start + quote.start()
            absolute_end = p_start + quote.end()
            content = quote.group("content")
            if not DIALOGUE_PRESSURE_PATTERN.search(content):
                continue
            tail = masked[absolute_end:p_end]
            has_response = bool(DIALOGUE_RESPONSE_PATTERN.search(tail[:180]))
            if not has_response and paragraph_index + 1 < len(paragraphs):
                next_start, next_end, _ = paragraphs[paragraph_index + 1]
                next_lead = masked[next_start : min(next_end, next_start + 100)]
                has_response = bool(
                    DIALOGUE_RESPONSE_PATTERN.search(next_lead)
                    or DIALOGUE_TURN_PATTERN.search(next_lead)
                )
            if not has_response:
                orphaned.append((absolute_start, absolute_end))
    if len(orphaned) >= 2 and enabled("NAT004", "dialogue-response-orphan"):
        start, end = orphaned[0]
        findings.append(
            _finding_from_span(
                text,
                "NAT004",
                "dialogue-response-orphan",
                "medium",
                start,
                end,
                "Multiple pressure-bearing lines receive no visible reply, action, costly silence, interruption, or carried deferral before the prose moves on.",
            )
        )

    return findings


def _precision_is_earned(text: str, start: int, end: int) -> bool:
    context = text[max(0, start - 60) : min(len(text), end + 60)]
    return bool(
        re.search(
            r"法医|鉴定|伤口|病历|医学|检验|检测|测量|仪器|报告|工程|参数|规格|"
            r"实验|数据|证据|建筑高度|剂量|病例|"
            r"\b(?:forensic|medical|wound|measured|measurement|report|engineering|"
            r"specification|experiment|evidence|dosage)\b",
            context,
            re.IGNORECASE,
        )
    )


def lint_text(
    text: str,
    style: str = "general",
    allow: set[str] | None = None,
) -> LintReport:
    allowed = allow or set()
    masked = _mask_ignored_regions(text)
    findings: list[LintFinding] = []
    for rule in RULES:
        if style in rule.excluded_styles or rule.rule_id in allowed or rule.category in allowed:
            continue
        if rule.rule_id == "PREC001" and style not in NARRATIVE_STYLES:
            continue
        for match in rule.pattern.finditer(masked):
            if rule.rule_id == "PREC001" and _precision_is_earned(
                masked,
                match.start(),
                match.end(),
            ):
                continue
            findings.append(
                _finding_from_span(
                    text,
                    rule.rule_id,
                    rule.category,
                    rule.severity,
                    match.start(),
                    match.end(),
                    rule.message,
                )
            )

    sentence_lengths = _sentence_lengths(masked)
    if len(sentence_lengths) >= 5 and _coefficient_of_variation(sentence_lengths) < 0.16:
        findings.append(
            _finding_from_span(
                text,
                "RHYTHM001",
                "uniform-rhythm",
                "medium",
                0,
                min(len(text), 120),
                "Sentence lengths are unusually uniform; vary cadence where the genre permits.",
            )
        )

    em_dash_count = masked.count("—")
    word_count = len(re.findall(r"[\u4e00-\u9fff]|\b[\w'-]+\b", masked))
    dash_clusters = [
        (start, fragment.find("—"))
        for start, _, fragment in _paragraph_spans(masked)
        if fragment.count("—") >= 3
        and fragment.count("—") * 60 > max(len(re.findall(r"[\u4e00-\u9fff]|\b[\w'-]+\b", fragment)), 1)
    ]
    if em_dash_count >= 3 and (em_dash_count * 500 > max(word_count, 1) or dash_clusters):
        first_dash = dash_clusters[0][0] + dash_clusters[0][1] if dash_clusters else masked.find("—")
        findings.append(
            _finding_from_span(
                text,
                "PUNCT001",
                "dash-density",
                "low",
                first_dash,
                first_dash + 1,
                "Em-dash use clusters tightly; verify that each dash marks a real interruption, withheld clause, or turn rather than decorative depth.",
            )
        )

    if style in FICTION_STYLES:
        findings.extend(_narrative_heading_findings(text, masked, allowed))

    if style not in {"academic-paper", "formal-document", "news-report"}:
        if "STR002" not in allowed and "comparison-ladder" not in allowed:
            for start, end, sentence in _sentence_spans(masked):
                comparison_offsets = _comparative_bi_offsets(sentence)
                if len(comparison_offsets) < 2:
                    continue
                rule_id = "STR004" if len(comparison_offsets) >= 3 else "STR002"
                category = (
                    "comparison-ladder-density" if rule_id == "STR004" else "comparison-ladder"
                )
                if rule_id in allowed or category in allowed:
                    continue
                findings.append(
                    _finding_from_span(
                        text,
                        rule_id,
                        category,
                        "high" if rule_id == "STR004" else "medium",
                        start + comparison_offsets[0],
                        min(end, start + comparison_offsets[-1] + 24),
                        (
                            "This sentence stacks three or more 比-comparisons; rewrite the decorative ladder before delivery while preserving distinct facts."
                            if rule_id == "STR004"
                            else "This sentence chains multiple 比-comparisons; keep one shared criterion, split unlike criteria, or state the observed change directly."
                        ),
                    )
                )

    inflated_matches = list(INFLATED_CLUSTER_PATTERN.finditer(masked))
    if (
        len(inflated_matches) >= 4
        and "LEX003" not in allowed
        and "inflated-vocabulary-density" not in allowed
    ):
        first = inflated_matches[0]
        findings.append(
            _finding_from_span(
                text,
                "LEX003",
                "inflated-vocabulary-density",
                "high" if len(inflated_matches) >= 7 else "medium",
                first.start(),
                inflated_matches[min(len(inflated_matches) - 1, 3)].end(),
                "Inflated or prestige vocabulary clusters in this passage; replace the cluster with claims, actors, and observable proof.",
            )
        )

    if style in ARGUMENTATIVE_STYLES:
        double_edged_matches = list(DOUBLE_EDGED_PATTERN.finditer(masked))
        if (
            len(double_edged_matches) >= 2
            and len(double_edged_matches) * 1400 >= max(len(masked), 1)
            and "ARG001" not in allowed
            and "double-edged-sword-density" not in allowed
        ):
            first = double_edged_matches[0]
            findings.append(
                _finding_from_span(
                    text,
                    "ARG001",
                    "double-edged-sword-density",
                    "low",
                    first.start(),
                    first.end(),
                    "The double-edged-sword metaphor recurs in an argumentative passage. Replace at least one instance with the specific trade-off, affected party, and evidence.",
                )
            )
        tiered_matches = list(TIERED_CONNECTOR_PATTERN.finditer(masked))
        connector_forms = {match.group(0).casefold() for match in tiered_matches}
        if (
            len(tiered_matches) >= 4
            and len(connector_forms) >= 2
            and len(tiered_matches) * 1100 >= max(len(masked), 1)
            and "ARG002" not in allowed
            and "tiered-connector-density" not in allowed
        ):
            first = tiered_matches[0]
            findings.append(
                _finding_from_span(
                    text,
                    "ARG002",
                    "tiered-connector-density",
                    "low",
                    first.start(),
                    first.end(),
                    "Layered connectors repeatedly announce importance without necessarily adding a premise, warrant, or evidence. Keep only the links that identify a real logical relation.",
                )
            )

    if style in NARRATIVE_STYLES:
        for alias_pattern in ALIAS_CYCLING_GROUPS:
            aliases = list(dict.fromkeys(match.group(0).lower() for match in alias_pattern.finditer(masked)))
            if (
                len(aliases) >= 3
                and "ALIAS001" not in allowed
                and "synonym-cycling" not in allowed
            ):
                first = alias_pattern.search(masked)
                if first:
                    findings.append(
                        _finding_from_span(
                            text,
                            "ALIAS001",
                            "synonym-cycling",
                            "medium",
                            first.start(),
                            first.end(),
                            "Several labels rename the same narrative role; repeat the established name or title unless the label changes viewpoint.",
                        )
                    )
                break

    inline_headers = list(INLINE_HEADER_PATTERN.finditer(masked))
    if len(inline_headers) >= 3 and "FORMAT001" not in allowed and "inline-header-density" not in allowed:
        first = inline_headers[0]
        findings.append(
            _finding_from_span(
                text,
                "FORMAT001",
                "inline-header-density",
                "low",
                first.start(),
                first.end(),
                "Repeated bold-label bullets may be template scaffolding; keep them only when the document is genuinely reference-oriented.",
            )
        )

    emoji_matches = list(DECORATIVE_EMOJI_PATTERN.finditer(masked))
    if len(emoji_matches) >= 3 and "FORMAT002" not in allowed and "decorative-emoji-density" not in allowed:
        first = emoji_matches[0]
        findings.append(
            _finding_from_span(
                text,
                "FORMAT002",
                "decorative-emoji-density",
                "low",
                first.start(),
                first.end(),
                "Decorative emoji recur; verify that the channel and audience expect them.",
            )
        )

    title_headings = list(TITLE_CASE_HEADING_PATTERN.finditer(masked))
    if len(title_headings) >= 3 and "FORMAT003" not in allowed and "title-case-heading-density" not in allowed:
        first = title_headings[0]
        findings.append(
            _finding_from_span(
                text,
                "FORMAT003",
                "title-case-heading-density",
                "low",
                first.start(),
                first.end(),
                "English headings repeatedly use title case; confirm the publication's house style instead of normalizing automatically.",
            )
        )

    contrast_matches = list(FORMULAIC_CONTRAST_PATTERN.finditer(masked))
    if (
        len(contrast_matches) >= 3
        and "STR003" not in allowed
        and "formulaic-frame-density" not in allowed
    ):
        first = contrast_matches[0]
        findings.append(
            _finding_from_span(
                text,
                "STR003",
                "formulaic-frame-density",
                "high",
                first.start(),
                first.end(),
                "Not-X/is-Y contrast frames recur across the passage; preserve only distinctions that change fact, logic, or voice and rewrite the rest from evidence.",
            )
        )

    if style in NARRATIVE_STYLES:
        paragraphs = _paragraph_spans(masked)
        imagery_pattern = re.compile(
            r"像|仿佛|如同|宛如|好似|犹如|\blike\b|\bas if\b",
            re.IGNORECASE,
        )
        detail_pattern = re.compile(
            r"(?:[今现]年)?\d{1,3}岁|身高|体重|职业|结婚[了]?\d|任职|毕业于|"
            r"\b(?:aged?|height|weighs?|occupation|married|graduated)\b",
            re.IGNORECASE,
        )
        for start, end, paragraph in paragraphs:
            image_count = len(imagery_pattern.findall(paragraph))
            if (
                image_count >= 4
                and "IMG001" not in allowed
                and "imagery-density" not in allowed
            ):
                findings.append(
                    _finding_from_span(
                        text,
                        "IMG001",
                        "imagery-density",
                        "medium",
                        start,
                        min(end, start + 160),
                        "This paragraph stacks several comparisons; keep the image that changes perception or action.",
                    )
                )
            detail_count = len(detail_pattern.findall(paragraph))
            if (
                detail_count >= 3
                and "INFO001" not in allowed
                and "detail-inventory" not in allowed
            ):
                findings.append(
                    _finding_from_span(
                        text,
                        "INFO001",
                        "detail-inventory",
                        "medium",
                        start,
                        min(end, start + 160),
                        "Several biographical or measured details arrive together; keep what the scene uses and delay the rest.",
                    )
                )

        opening_spans = [(0, min(len(masked), 700)), *_chapter_opening_spans(masked)]
        seen_starts: set[int] = set()
        stacked_openings: list[tuple[int, int, set[str]]] = []
        for start, end in opening_spans:
            if start in seen_starts:
                continue
            seen_starts.add(start)
            cues = _scene_opening_cues(masked[start:end])
            if len(cues) >= 4:
                stacked_openings.append((start, end, cues))
        if "OPEN002" not in allowed and "cinematic-opening-stack" not in allowed:
            for start, end, cues in stacked_openings[:3]:
                findings.append(
                    _finding_from_span(
                        text,
                        "OPEN002",
                        "cinematic-opening-stack",
                        "medium",
                        start,
                        min(end, start + 180),
                        "The opening front-loads "
                        + ", ".join(sorted(cues))
                        + "; keep only details used by the first pressure-bearing action.",
                    )
                )

        introspection_matches = list(FORMULAIC_INTROSPECTION_PATTERN.finditer(masked))
        if (
            len(introspection_matches) >= 3
            and "EMO003" not in allowed
            and "formulaic-introspection" not in allowed
        ):
            first = introspection_matches[0]
            findings.append(
                _finding_from_span(
                    text,
                    "EMO003",
                    "formulaic-introspection",
                    "medium",
                    first.start(),
                    first.end(),
                    "Repeated vague self-interpretation explains feeling without changing action; "
                    "keep only the instance that adds contradiction, choice, or consequence.",
                )
            )

        chapter_openings = _chapter_opening_spans(masked)
        scenic_resets = [
            (start, end)
            for start, end in chapter_openings
            if len(_scene_opening_cues(masked[start:end])) >= 3
        ]
        if (
            len(chapter_openings) >= 3
            and len(scenic_resets) * 5 >= len(chapter_openings) * 3
            and "RESET001" not in allowed
            and "chapter-scenic-reset" not in allowed
        ):
            start, end = scenic_resets[0]
            findings.append(
                _finding_from_span(
                    text,
                    "RESET001",
                    "chapter-scenic-reset",
                    "medium",
                    start,
                    min(end, start + 180),
                    "Most chapters restart with a fresh scenic slate; carry forward a consequence, "
                    "object, question, or relationship pressure before re-establishing atmosphere.",
                )
            )

        run_start = None
        run_count = 0
        for start, end, paragraph in paragraphs:
            if len(paragraph) <= 24:
                if run_start is None:
                    run_start = start
                run_count += 1
                if (
                    run_count == 4
                    and "PARA001" not in allowed
                    and "fragment-run" not in allowed
                ):
                    findings.append(
                        _finding_from_span(
                            text,
                            "PARA001",
                            "fragment-run",
                            "medium",
                            run_start,
                            min(end, run_start + 160),
                            "Four or more short paragraphs run together; verify that each break marks a real turn.",
                        )
                    )
            else:
                run_start = None
                run_count = 0

        findings.extend(_narrative_naturalness_findings(text, masked, style, allowed))

    findings.sort(key=lambda finding: (finding.start, finding.rule_id))
    weighted = sum(SEVERITY_WEIGHT[finding.severity] for finding in findings)
    score = min(100, round(weighted * 500 / max(word_count, 250)))
    label = "minimal"
    if score >= 60:
        label = "heavy"
    elif score >= 35:
        label = "visible"
    elif score >= 15:
        label = "light"
    confidence = "low" if word_count < 80 else "medium" if word_count < 250 else "high"
    return LintReport(
        score=score,
        label=label,
        confidence=confidence,
        style=style,
        character_count=len(text),
        word_count=word_count,
        findings=tuple(findings),
    )


def lint_file(path: str, style: str = "general", allow: set[str] | None = None) -> LintReport:
    return lint_text(Path(path).read_text(encoding="utf-8"), style=style, allow=allow)


def format_lint_report(
    report: LintReport,
    output_format: str = "markdown",
    source_name: str | None = None,
) -> str:
    if output_format == "json":
        return json.dumps(report.to_dict(), ensure_ascii=False, indent=2) + "\n"
    if output_format == "github":
        file_name = (source_name or "draft.md").replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        lines = []
        for finding in report.findings:
            message = f"[{finding.rule_id}] {finding.message}".replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
            lines.append(
                f"::warning file={file_name},line={finding.line},col={finding.column}::{message}"
            )
        return "\n".join(lines) + ("\n" if lines else "")
    lines = [
        "# Writing Pattern Lint",
        "",
        f"- Score: {report.score}/100 ({report.label})",
        f"- Confidence: {report.confidence}",
        f"- Style profile: {report.style}",
        f"- Findings: {len(report.findings)}",
        f"- Disclaimer: {report.disclaimer}",
        "",
        "| Rule | Severity | Location | Evidence | Repair direction |",
        "| --- | --- | --- | --- | --- |",
    ]
    for finding in report.findings:
        evidence = finding.excerpt.replace("|", "\\|")
        message = finding.message.replace("|", "\\|")
        lines.append(
            f"| `{finding.rule_id}` | {finding.severity} | "
            f"L{finding.line}:C{finding.column} | {evidence} | {message} |"
        )
    return "\n".join(lines) + "\n"
