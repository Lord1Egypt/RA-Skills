#!/usr/bin/env python3
"""Generate a LearnWa single-file H5 lesson from natural language input.

退出码约定：
  0 = 成功
  2 = 输入有问题（文件不存在、JSON 格式错、参数不认识、题目不合规），已给出中文修复建议
  3 = 技能自身文件缺失或损坏（模板找不到、模板占位符丢失）
  1 = 未预期的异常（会提示重试方式）
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "learnwa-template.html"
OUT_DIR = Path.cwd() / "docs"  # 未指定 --output 时的默认输出目录（相对当前工作目录，跨平台可移植）

EXIT_INPUT = 2
EXIT_SKILL = 3

THEMES = {
    "vehicle": {
        "themeName": "交通工具",
        "characters": ["小汽车", "小火车", "小飞机"],
        "itemNames": ["能量格", "电量格", "燃料格"],
        "goals": ["过桥", "开到下一站", "飞到目的地"],
        "removeVerb": "用掉",
        "addVerb": "加入",
        "rewardNames": ["过桥小能手", "能量小达人", "小小驾驶员"],
        "css": {"--primary":"#FF6B35","--secondary":"#004E89","--accent":"#FFD700","--bg-scene-top":"#87CEEB","--bg-scene-bottom":"#B0E0E6","--ground-color":"#7B8D6F","--item-color":"#FF6B35","--text-on-item":"#FFFFFF","--card-bg":"#FFF8F0"}
    },
    "card_collection": {
        "themeName": "收集卡片",
        "characters": ["小收藏家", "卡片小达人"],
        "itemNames": ["卡片", "普通卡", "能量卡"],
        "goals": ["兑换稀有卡", "集齐一套卡", "完成卡册"],
        "removeVerb": "交出",
        "addVerb": "加入",
        "rewardNames": ["稀有卡收藏家", "卡片小达人", "凑十收藏家"],
        "css": {"--primary":"#7C3AED","--secondary":"#EC4899","--accent":"#FBBF24","--bg-scene-top":"#F5F3FF","--bg-scene-bottom":"#EDE9FE","--ground-color":"#DDD6FE","--item-color":"#7C3AED","--text-on-item":"#FFFFFF","--card-bg":"#FAFAFE"}
    },
    "dinosaur": {
        "themeName": "恐龙",
        "characters": ["小恐龙", "恐龙宝宝"],
        "itemNames": ["恐龙蛋", "树叶", "小脚印"],
        "goals": ["找到妈妈", "收集树叶", "回到山洞"],
        "removeVerb": "拿走",
        "addVerb": "放入",
        "rewardNames": ["恐龙小勇士", "恐龙探险家", "森林小达人"],
        "css": {"--primary":"#059669","--secondary":"#92400E","--accent":"#F59E0B","--bg-scene-top":"#D1FAE5","--bg-scene-bottom":"#A7F3D0","--ground-color":"#65A30D","--item-color":"#059669","--text-on-item":"#FFFFFF","--card-bg":"#F0FDF4"}
    },
    "animal_bear": {
        "themeName": "小熊",
        "characters": ["小熊", "熊宝宝"],
        "itemNames": ["蜂蜜罐", "浆果", "小饼干"],
        "goals": ["准备野餐", "分蜂蜜", "回到小木屋"],
        "removeVerb": "拿走",
        "addVerb": "放进",
        "rewardNames": ["破十小熊", "森林数学家", "蜂蜜小能手"],
        "css": {"--primary":"#B7791F","--secondary":"#78350F","--accent":"#F6C453","--bg-scene-top":"#FEF3C7","--bg-scene-bottom":"#FDE68A","--ground-color":"#84A98C","--item-color":"#F59E0B","--text-on-item":"#182230","--card-bg":"#FFFBEB"}
    },
    "vegetable_garden": {
        "themeName": "小菜园",
        "characters": ["小农夫", "菜菜小园丁"],
        "itemNames": ["白菜", "萝卜", "番茄"],
        "goals": ["收获蔬菜", "装满菜篮", "送到厨房"],
        "removeVerb": "拔走",
        "addVerb": "种下",
        "rewardNames": ["菜园小能手", "蔬菜小达人", "丰收小农夫"],
        "css": {"--primary":"#16A34A","--secondary":"#713F12","--accent":"#F97316","--bg-scene-top":"#BBF7D0","--bg-scene-bottom":"#DCFCE7","--ground-color":"#86EFAC","--item-color":"#16A34A","--text-on-item":"#FFFFFF","--card-bg":"#F0FDF4"}
    }
}

SKILLS = {
    "break_ten": {"skillName":"破十法","englishName":"Break Ten Method","templateId":"remove_to_ten"},
    "make_ten": {"skillName":"凑十法","englishName":"Make Ten Method","templateId":"fill_to_ten"},
    "level_ten": {"skillName":"平十法","englishName":"Level Ten Method","templateId":"subtract_to_ten_then_continue"},
}

# 信号词只收「够明确」的词，避免随口聊天误触发（例如不要用单独的 “-”“+”“龙”“卡”）
SKILL_KEYWORDS = {
    "make_ten": ["凑十法", "凑十", "凑成10", "凑成十", "凑满10", "凑满十", "满十法", "进位加法", "进位加"],
    "level_ten": ["平十法", "平十", "减到10", "减到十", "退到10", "退到十", "平到十", "先减到整十"],
    "break_ten": ["破十法", "破十", "借十法", "借十", "破开十", "十几减", "退位减法", "退位减"],
}

THEME_KEYWORDS = {
    "card_collection": ["卡片", "集卡", "收藏卡", "卡册", "稀有卡", "兑换卡"],
    "animal_bear": ["小熊", "熊宝宝", "蜂蜜"],
    "dinosaur": ["恐龙", "霸王龙", "三角龙"],
    "vegetable_garden": ["菜园", "蔬菜", "萝卜", "白菜", "番茄", "种菜", "庄稼", "农夫"],
    "vehicle": ["汽车", "火车", "飞机", "开车", "交通工具", "高铁", "卡车", "飞船", "挖土机", "小汽车"],
}

DEFAULT_SKILL = "break_ten"
DEFAULT_THEME = "vehicle"

# ---- 「点名主题」识别 ----------------------------------------------------
# 用户明确说出了某个兴趣时（例如「来个足球的」），即使它不是内置主题，
# 也绝不能静默换成别的主题（例如汽车）—— 那等于把孩子带偏。
# 这组句式只认「明确点名」的写法，避免把随口一句聊天当成主题。
_SKILL_WORD_MARKERS = ("破十", "凑十", "平十", "借十", "退位", "进位", "减到", "退到", "满十")
_MENTION_PREFIX = re.compile(
    r"(?:来个|来一个|要个|要一个|换个|换成|用|做个|做一份|生成一个|生成个|整一个|弄个)"
    r"\s*([\u4e00-\u9fa5A-Za-z0-9]{1,10}?)\s*的"
)
_MENTION_LIKE = re.compile(
    r"(?:喜欢|迷上|爱看|爱玩|超爱|最爱|痴迷|兴趣是)\s*"
    r"([\u4e00-\u9fa5A-Za-z0-9]{1,10}?)"
    r"(?=[，,。、；;！!？?\s]|来个|来一个|讲|学|做个|做一份|生成|换|现在|$)"
)
_MENTION_TOPIC = re.compile(r"([\u4e00-\u9fa5A-Za-z0-9]{1,10}?)\s*主题")
_MENTION_BARE = re.compile(
    r"(?:来个|来一个|换个|换成|整一个|弄个)\s*"
    r"([\u4e00-\u9fa5A-Za-z0-9]{1,8}?)"
    r"(?=[，,。、；;！!？?\s的]|来个|破十法|凑十法|平十法|借十法|$)"
)
_MENTION_LEADING_NOISE = re.compile(
    r"^(?:来个|来一个|要个|要一个|换个|换成|用|做个|做一份|生成一个|生成个|整一个|弄个|的|个性|定制|自定义)+"
)
_THEME_NOISE = {
    "数学", "教具", "页面", "练习", "题", "题目", "这个", "那个", "简单", "难一点",
    "游戏", "动画", "互动", "课", "课程", "版本", "h5", "html", "网页", "例子", "新的",
}

# customTheme 没有给 themeCSS 时的中性兜底色板（绝不再借用汽车配色）
CUSTOM_THEME_FALLBACK_CSS = {
    "--primary": "#475569",
    "--secondary": "#0F172A",
    "--accent": "#F59E0B",
    "--bg-scene-top": "#F1F5F9",
    "--bg-scene-bottom": "#E2E8F0",
    "--ground-color": "#CBD5E1",
    "--item-color": "#64748B",
    "--text-on-item": "#FFFFFF",
    "--card-bg": "#F8FAFC",
}


class LearnWaError(Exception):
    """带中文修复建议的、可展示给用户的错误。"""

    def __init__(self, message: str, code: int = EXIT_INPUT):
        super().__init__(message)
        self.message = message
        self.code = code


def _skill_list_text() -> str:
    return "、".join(f"{k}（{v['skillName']}）" for k, v in SKILLS.items())


def _theme_list_text() -> str:
    return "、".join(f"{k}（{v['themeName']}）" for k, v in THEMES.items())


def detect_skill(text: str) -> str:
    """只按明确的方法名识别；识别不到返回空串，由调用方决定默认值。"""
    if not text:
        return ""
    for skill in ("make_ten", "level_ten", "break_ten"):
        if any(k in text for k in SKILL_KEYWORDS[skill]):
            return skill
    return ""


def detect_theme(text: str) -> str:
    """只按明确的主题词识别；识别不到返回空串，由调用方决定默认值。"""
    if not text:
        return ""
    for theme in ("card_collection", "animal_bear", "dinosaur", "vegetable_garden", "vehicle"):
        if any(k in text for k in THEME_KEYWORDS[theme]):
            return theme
    return ""


def extract_theme_mention(text: str) -> str:
    """抽取「被用户点名的主题」。

    抽得到 → 用户明确想要这个主题，即使不是内置主题也必须用 customTheme 实现；
    抽不到 → 用户没提主题，调用方才允许使用默认主题。
    """
    if not text:
        return ""
    candidates: list[str] = []
    for pattern in (_MENTION_PREFIX, _MENTION_LIKE, _MENTION_TOPIC, _MENTION_BARE):
        for match in pattern.finditer(text):
            candidates.append(match.group(1))
    for raw in candidates:
        cand = _MENTION_LEADING_NOISE.sub("", raw.strip()).strip()
        if len(cand) < 2:
            continue
        if cand.lower() in _THEME_NOISE:
            continue
        if any(marker in cand for marker in _SKILL_WORD_MARKERS):
            continue
        if detect_theme(cand):
            continue
        return cand
    return ""


def _theme_mention_error(mentioned: str) -> str:
    return (
        f"你说到了主题「{mentioned}」，它不是内置主题，脚本不会把它偷偷换成别的主题。\n"
        f"    内置主题只有：{_theme_list_text()}\n"
        f"    修复：在 lesson-block.json 里用 customTheme 现场创建「{mentioned}」主题，例如：\n"
        f'      "customTheme": {{\n'
        f'        "themeId": "custom_theme",\n'
        f'        "themeName": "{mentioned}",\n'
        f'        "character": "主角名",\n'
        f'        "itemName": "{mentioned}相关的物品名",\n'
        f'        "removeVerb": "拿走",\n'
        f'        "addVerb": "放进",\n'
        f'        "goal": "这一步要做什么",\n'
        f'        "themeCSS": {{ "--primary": "#16A34A", "--item-color": "#16A34A", "--text-on-item": "#FFFFFF" }},\n'
        f'        "heroSvg": "<svg viewBox=\\"0 0 120 100\\">…主角造型…</svg>",\n'
        f'        "itemSvg": "<svg viewBox=\\"0 0 40 40\\">…物品造型…</svg>"\n'
        f"      }}\n"
        "    注意：命中不了内置主题时，正确的做法是你**自己画一份内联 SVG**（见 references/lesson-block-format.md），\n"
        "    而不是只写文字、更不是换成默认主题；颜色用 {{primary}}/{{accent}}/{{item}} 占位符。\n"
        "    完整字段见 references/lesson-block-format.md 的「自画主题造型」一节。\n"
        "    如果确实想用默认「交通工具」，请加 --allow-default-theme。"
    )


def _custom_theme_css(custom_theme: dict) -> tuple[dict, bool]:
    """返回 (css, 是否用了兜底色板)。不给 themeCSS 时不再借用汽车配色。"""
    css = custom_theme.get("themeCSS")
    if isinstance(css, dict) and css:
        return {**CUSTOM_THEME_FALLBACK_CSS, **css}, False
    primary = custom_theme.get("primaryColor")
    if isinstance(primary, str) and primary.strip():
        return {
            **CUSTOM_THEME_FALLBACK_CSS,
            "--primary": primary,
            "--item-color": custom_theme.get("itemColor", primary),
        }, False
    return dict(CUSTOM_THEME_FALLBACK_CSS), True


_SVG_STRIP_BLOCKS = re.compile(r"<\s*(script|foreignObject|iframe|style)\b[\s\S]*?<\s*/\s*\1\s*>", re.I)
_SVG_STRIP_EVENTS = re.compile(r"\son\w+\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>]+)", re.I)
_SVG_STRIP_JS = re.compile(r"javascript:", re.I)


def _sanitize_svg(value, field: str) -> str | None:
    """校验并清洗 Bot 自画的 SVG：只留安全的内联 <svg>，剔除脚本与事件。"""
    if value in (None, ""):
        return None
    if not isinstance(value, str):
        raise LearnWaError(
            f"customTheme.{field} 必须是字符串形式的 SVG，当前是 {type(value).__name__}。\n"
            f'    修复：写成 "SVG": "<svg viewBox=\\"0 0 120 100\\">…</svg>"。'
        )
    svg = value.strip()
    if not svg.lower().startswith("<svg"):
        raise LearnWaError(
            f"customTheme.{field} 必须以 <svg 开头。\n"
            '    修复：传一个完整的 <svg viewBox="0 0 120 100">…</svg>，不要只传路径片段。'
        )
    if "</svg>" not in svg.lower():
        raise LearnWaError(f"customTheme.{field} 缺少 </svg> 结束标签，请补全。")
    cleaned = _SVG_STRIP_JS.sub("", _SVG_STRIP_EVENTS.sub("", _SVG_STRIP_BLOCKS.sub("", svg)))
    if cleaned != svg:
        print(
            f"[学习娃] 提示：customTheme.{field} 里有脚本、事件或外链写法，已自动剔除"
            "（教具页只允许纯静态内联 SVG）。",
            file=sys.stderr,
        )
    return cleaned


def _custom_theme_symbols(custom_theme: dict) -> dict | None:
    """Bot 自画主题造型：customTheme.heroSvg / itemSvg，或 symbols.{hero,item}。"""
    raw = custom_theme.get("symbols") if isinstance(custom_theme.get("symbols"), dict) else {}
    hero = _sanitize_svg(custom_theme.get("heroSvg", raw.get("hero")), "heroSvg")
    item = _sanitize_svg(custom_theme.get("itemSvg", raw.get("item")), "itemSvg")
    symbols = {}
    if hero:
        symbols["hero"] = hero
    if item:
        symbols["item"] = item
    return symbols or None


def question_for(skill: str, seed: int | None = None) -> dict:
    rng = random.Random(seed)
    if skill == "make_ten":
        while True:
            a = rng.randint(6, 9)
            b = rng.randint(2, 9)
            if a + b > 10 and b >= 10 - a:
                need = 10 - a
                remain = b - need
                return {"text": f"{a} + {b}", "a": a, "b": b, "needToTen": need, "remain": remain, "answer": a + b}
    while True:
        a = rng.randint(11, 19)
        ones = a - 10
        b = rng.randint(2, 9)
        if b > ones:
            if skill == "break_ten":
                ten_minus = 10 - b
                answer = ones + ten_minus
                return {"text": f"{a} - {b}", "a": a, "b": b, "ones": ones, "tenMinus": ten_minus, "answer": answer}
            remain = b - ones
            answer = 10 - remain
            return {"text": f"{a} - {b}", "a": a, "b": b, "toTen": ones, "remain": remain, "answer": answer}


def story_for(theme: str, skill: str, q: dict, themes: dict | None = None) -> dict:
    themes = themes or THEMES
    t = themes[theme]
    character = t["characters"][0]
    if theme == "vehicle" and skill == "level_ten": character = "小火车"
    if theme == "vehicle" and skill == "make_ten": character = "小飞机"
    return {
        "character": character,
        "itemName": t["itemNames"][0],
        "removeVerb": t["removeVerb"],
        "addVerb": t["addVerb"],
        "goal": t["goals"][0],
        "reward": t["rewardNames"][0],
    }


def title_for(skill: str, theme: str, story: dict) -> str:
    if skill == "break_ten":
        verb = "学破十法"
    elif skill == "make_ten":
        verb = "学凑十法"
    else:
        verb = "学平十法"
    if theme == "card_collection": return f"{story['goal']}{verb}"
    return f"{story['character']}{story['goal']}{verb}"


def build_steps(skill: str, q: dict, s: dict) -> list[dict]:
    item, rv, av, char, goal = s["itemName"], s["removeVerb"], s["addVerb"], s["character"], s["goal"]
    a, b = q["a"], q["b"]
    if skill == "make_ten":
        need, remain, ans = q["needToTen"], q["remain"], q["answer"]
        return [
            {"id":"intro","type":"story","childText":f"{a} + {b}","visualAction":"show_addition_scene","parentGuide":{"say":f"{char}先有{a}{item}，又{av}{b}{item}。一共有多少？今天用凑十法来算。","expected":"可以先猜一猜","wrongHint":"先不急着要答案，我们一步一步看。"}},
            {"id":"ask_need_to_ten","type":"question","childText":f"{a} + ? = 10","visualAction":"show_gap_to_ten","parentGuide":{"say":f"{a}还差几就能凑成10？","expected":str(need),"wrongHint":f"从{a}往后数到10，看看一共数了几个。"}},
            {"id":"split_b","type":"split","childText":f"{b} = {need} + {remain}","visualAction":"split_second_number","parentGuide":{"say":f"我们把{b}分成{need}和几？","expected":str(remain),"wrongHint":f"伸出{b}根手指，先拿出{need}根，还剩几根？"}},
            {"id":"make_ten","type":"add_items","childText":f"{a} + {need} = 10","visualAction":"fill_items_to_ten","parentGuide":{"say":f"先拿{need}{item}过来，把{a}凑成10。","expected":"知道先凑10","wrongHint":"10是很好算的数，所以我们先凑成10。"}},
            {"id":"add_remain","type":"add_items","childText":f"10 + {remain} = {ans}","visualAction":"add_remaining_items","parentGuide":{"say":f"还有{remain}{item}没加，现在10加{remain}等于几？","expected":str(ans),"wrongHint":f"从10往后数{remain}个。"}},
            {"id":"summary","type":"summary","childText":f"{a} + {b} = {ans}","visualAction":"show_success","parentGuide":{"say":f"我们先把{a}凑成10，再加剩下的{remain}，所以{a}加{b}等于{ans}。这就是凑十法。","expected":"孩子能复述过程","wrongHint":"可以再用实物摆一遍。"}},
        ]
    if skill == "break_ten":
        ones, ten_minus, ans = q["ones"], q["tenMinus"], q["answer"]
        return [
            {"id":"intro","type":"story","childText":f"{a} - {b}","visualAction":"show_total_items","parentGuide":{"say":f"{char}有{a}{item}，{goal}要{rv}{b}{item}。还剩多少？","expected":"可以先猜一猜","wrongHint":"没关系，先看画面。"}},
            {"id":"split_to_10","type":"split","childText":f"{a} = {ones} + 10","visualAction":"split_items_ones_and_10","parentGuide":{"say":f"破十法先把{a}拆成{ones}和10。{a}里面有几个单独的？","expected":str(ones),"wrongHint":f"{a}就是10再多{ones}个，所以可以写成{ones}加10。"}},
            {"id":"borrow_from_ten","type":"remove_items","childText":f"10 - {b} = ?","visualAction":"remove_from_ten_group","parentGuide":{"say":f"第一排摆10{item}，第二排摆{ones}{item}。现在第二排不动，只从第一排10个里{rv}{b}{item}。10减{b}等于几？","expected":str(ten_minus),"wrongHint":f"看第一排：10个里面{rv}{b}个，还剩几个？第二排{ones}个先不要动。"}},
            {"id":"add_ones_back","type":"add_items","childText":f"{ten_minus} + {ones} = ?","visualAction":"add_ones_back","parentGuide":{"say":f"第一排还剩{ten_minus}{item}，第二排{ones}{item}一直没动。现在算{ten_minus}加{ones}等于几？","expected":str(ans),"wrongHint":f"先看第一排剩下的{ten_minus}个，再加上第二排没动的{ones}个。"}},
            {"id":"summary","type":"summary","childText":f"{a} - {b} = {ans}","visualAction":"show_success","parentGuide":{"say":f"所以{a}减{b}，先把{a}摆成第一排10个、第二排{ones}个；第一排10个减{b}还剩{ten_minus}个；第二排{ones}个不变；最后{ten_minus}加{ones}等于{ans}。这就是破十法，也就是这里的借十法。","expected":"孩子能复述：第一排10个先减，第二排不动，最后合起来","wrongHint":"可以再用实物摆一遍：第一排10个，第二排几个不要动。"}},
        ]
    to_ten, remain, ans = q["toTen"], q["remain"], q["answer"]
    return [
        {"id":"intro","type":"story","childText":f"{a} - {b}","visualAction":"show_total_items","parentGuide":{"say":f"{char}有{a}{item}，{goal}要{rv}{b}{item}。我们来算算还剩几。","expected":"可以先猜一猜","wrongHint":"先不急着要答案，我们一步一步看。"}},
        {"id":"split_subtrahend","type":"split","childText":f"{b} = {to_ten} + {remain}","visualAction":"split_remove_number","parentGuide":{"say":f"先看要减的{b}。为了把{a}先减到10，要先减{to_ten}，所以把{b}分成{to_ten}和几？","expected":str(remain),"wrongHint":f"第二排有{to_ten}{item}，第三排里先拿出同样多的{to_ten}{item}，剩下就是{remain}。"}},
        {"id":"subtract_to_ten","type":"question","childText":f"{a} - {to_ten} = 10","visualAction":"show_path_to_ten","parentGuide":{"say":f"先从{a}里面{rv}{to_ten}{item}，就正好退到10。{a}减{to_ten}等于几？","expected":"10","wrongHint":f"{a}里面有10和{to_ten}，先把多出来的{to_ten}减掉，就变成10。"}},
        {"id":"continue_subtract","type":"remove_items","childText":f"10 - {remain} = ?","visualAction":"remove_remaining_items","parentGuide":{"say":f"刚才{b}里面还剩{remain}{item}没减。现在从10里面再{rv}{remain}{item}，还剩几？","expected":str(ans),"wrongHint":f"从10往回数{remain}步。"}},
        {"id":"summary","type":"summary","childText":f"{a} - {b} = {ans}","visualAction":"show_success","parentGuide":{"say":f"我们先把要减的{b}分成{to_ten}和{remain}，先减{to_ten}到10，再从10里减{remain}，所以{a}减{b}等于{ans}。这就是平十法。","expected":"孩子能复述：先分，再减到10，再继续减","wrongHint":"可以再用实物摆一遍。"}},
    ]


def practice_for(skill: str, seed: int | None = None) -> list[dict]:
    return [{"text": (q := question_for(skill, (seed or 100) + i))["text"], "answer": q["answer"]} for i in range(3)]


def _explain_numbers_rejected(skill: str, a: int, b: int) -> str:
    """把不合规的题目翻译成家长看得懂的原因和建议。"""
    if skill == "make_ten":
        if not (2 <= b <= 9):
            return f"凑十法的第二个加数要在 2 到 9 之间，当前是 {b}。"
        if not (6 <= a <= 9):
            return f"凑十法的第一个加数要在 6 到 9 之间（个位接近 10 才好凑），当前是 {a}。"
        return (
            f"{a} 加 {b} 等于 {a + b}，没有超过 10，本来就是不用凑十的加法。\n"
            f"    建议：凑十法选和大于 10 的题，例如 8 + 7、9 + 5、7 + 6。"
        )
    if not (11 <= a <= 19):
        return f"退位减法（破十法／平十法）的要减数要在 11 到 19 之间，当前是 {a}。"
    if not (2 <= b <= 9):
        return f"减数要在 2 到 9 之间，当前是 {b}。"
    ones = a - 10
    if b <= ones:
        return (
            f"{a} 的个位是 {ones}，减数 {b} 不比它大，不需要退位，直接 {a} - {b} = {a - b} 就能算出来。\n"
            f"    建议：破十法／平十法请选个位小于减数的题，例如 15 - 8、13 - 7、16 - 9。"
        )
    return f"当前题目 {a} - {b} 不符合本方法的适用范围。"


def _coerce_int(value, label: str) -> int:
    if isinstance(value, bool):
        raise LearnWaError(f"numbers.{label} 必须是整数，当前是布尔值 {value}。\n    修复：写成数字，例如 \"{label}\": 15")
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if value.is_integer():
            return int(value)
        raise LearnWaError(f"numbers.{label} 必须是整数，当前是小数 {value}。\n    修复：写成整数，例如 \"{label}\": 15")
    if isinstance(value, str):
        text = value.strip()
        try:
            return int(text)
        except ValueError:
            raise LearnWaError(
                f"numbers.{label} 必须是整数，当前是文本 \"{value}\"。\n"
                f"    修复：去掉引号或写成纯数字，例如 \"{label}\": 15"
            ) from None
    raise LearnWaError(f"numbers.{label} 必须是整数，当前类型是 {type(value).__name__}。")


def question_from_numbers(skill: str, numbers: dict | None) -> dict | None:
    if not numbers:
        return None
    if not isinstance(numbers, dict):
        raise LearnWaError(
            "lesson-block.json 里的 numbers 必须写成对象，例如 \"numbers\": { \"a\": 15, \"b\": 8 }。"
        )
    a = _coerce_int(numbers.get("a", 0), "a")
    b = _coerce_int(numbers.get("b", 0), "b")
    if skill == "make_ten":
        if not (6 <= a <= 9 and 2 <= b <= 9 and a + b > 10):
            return None
        need = 10 - a
        remain = b - need
        return {"text": f"{a} + {b}", "a": a, "b": b, "needToTen": need, "remain": remain, "answer": a + b}
    if not (11 <= a <= 19 and 2 <= b <= 9):
        return None
    ones = a - 10
    if b <= ones:
        return None
    if skill == "break_ten":
        ten_minus = 10 - b
        answer = ones + ten_minus
        return {"text": f"{a} - {b}", "a": a, "b": b, "ones": ones, "tenMinus": ten_minus, "answer": answer}
    remain = b - ones
    answer = 10 - remain
    return {"text": f"{a} - {b}", "a": a, "b": b, "toTen": ones, "remain": remain, "answer": answer}


def build_config(
    prompt: str,
    skill: str | None,
    theme: str | None,
    seed: int | None,
    story_overrides: dict | None = None,
    copy_overrides: dict | None = None,
    numbers: dict | None = None,
    force_random: bool = False,
    themes: dict | None = None,
    allow_default_theme: bool = False,
) -> dict:
    themes = themes or THEMES
    skill = skill or detect_skill(prompt) or DEFAULT_SKILL
    if theme:
        pass
    else:
        theme = detect_theme(prompt)
        if not theme:
            mentioned = extract_theme_mention(prompt)
            if mentioned and not allow_default_theme:
                raise LearnWaError(_theme_mention_error(mentioned))
            theme = DEFAULT_THEME
    q = question_from_numbers(skill, numbers)
    if q is None and numbers and not force_random:
        a = _coerce_int(numbers.get("a", 0), "a")
        b = _coerce_int(numbers.get("b", 0), "b")
        raise LearnWaError(
            f"你指定的题目 {a} - {b} 不能用于{SKILLS[skill]['skillName']}。\n"
            f"    原因：{_explain_numbers_rejected(skill, a, b)}\n"
            f"    如果确实要换一道题，请修改 numbers，或加参数 --force-random 改用随机题目。"
        )
    q = q or question_for(skill, seed)
    story = story_for(theme, skill, q, themes)
    if story_overrides:
        story.update({k: v for k, v in story_overrides.items() if v})
    meta = SKILLS[skill]
    title = (copy_overrides or {}).get("title") or title_for(skill, theme, story)
    return {
        "lessonId": f"lesson_{skill}_{theme}_{seed or random.randint(100,999)}",
        "suiteId": "learnwa_math_skills",
        "suiteName": "学习娃",
        "suiteEnglishName": "LearnWa",
        "skillId": skill,
        "skillName": meta["skillName"],
        "englishName": meta["englishName"],
        "templateId": meta["templateId"],
        "themeId": theme,
        "title": title,
        "grade": 1,
        "difficulty": (copy_overrides or {}).get("difficulty", "easy"),
        "mode": "parent_controlled",
        "question": q,
        "story": story,
        "steps": build_steps(skill, q, story),
        "practice": practice_for(skill, seed),
        "parentTips": ["每一步先让孩子观察，再提问。", "答错时不要急着纠正，先用实物摆一遍。"],
        "offlineMaterials": ["10到20个瓶盖、积木或小卡片", "一张写着数字10的纸", "一支笔和一张草稿纸", "如果不想让孩子看屏幕，可以把屏幕当家长提示卡，只让孩子摆实物"],
        "themeCSS": themes[theme]["css"],
    }


def _validate_skill_id(value) -> str | None:
    if not value:
        return None
    if value not in SKILLS:
        raise LearnWaError(
            f"lesson-block.json 里的 skillId 不认识：{value}\n"
            f"    可选值：{_skill_list_text()}\n"
            f"    修复：改成上面之一；如果是「借十法」请填 break_ten。"
        )
    return value


def _validate_theme_id(value, custom_theme: dict) -> str | None:
    if not value:
        return None
    if value not in THEMES and not custom_theme:
        raise LearnWaError(
            f"lesson-block.json 里的 themeId 不认识：{value}\n"
            f"    内置主题：{_theme_list_text()}\n"
            f"    修复：改用内置主题，或为孩子的专属兴趣写 customTheme 分块（见 references/lesson-block-format.md）。"
        )
    return value


def build_config_from_block(block: dict, force_random: bool = False, allow_default_theme: bool = False) -> dict:
    if not isinstance(block, dict):
        raise LearnWaError(
            "lesson-block.json 的最外层必须是一个对象（用 { } 包起来），当前不是。\n"
            "    修复：参考 references/lesson-block-format.md 的最小示例。"
        )
    prompt = block.get("input") or block.get("prompt") or "我要一个破十法"
    copy_overrides = block.get("copyOverrides") or {}
    if block.get("difficulty"):
        copy_overrides = {**copy_overrides, "difficulty": block["difficulty"]}
    custom_theme = block.get("customTheme") or {}
    _validate_skill_id(block.get("skillId"))
    theme_id = _validate_theme_id(block.get("themeId") or custom_theme.get("themeId"), custom_theme)
    # 用本进程的局部副本，避免自定义主题污染内置 THEMES 或残留到下一次生成
    themes = {**THEMES}
    if custom_theme:
        theme_id = theme_id or "custom_theme"
        css, used_fallback = _custom_theme_css(custom_theme)
        themes[theme_id] = {
            "themeName": custom_theme.get("themeName", "自定义主题"),
            "characters": [custom_theme.get("character", "小朋友")],
            "itemNames": [custom_theme.get("itemName", "小物品")],
            "goals": [custom_theme.get("goal", "完成任务")],
            "removeVerb": custom_theme.get("removeVerb", "拿走"),
            "addVerb": custom_theme.get("addVerb", "放进"),
            "rewardNames": [custom_theme.get("reward", "数学小达人")],
            "css": css,
        }
        if used_fallback:
            print(
                "[学习娃] 提示：customTheme 没有给 themeCSS（或 primaryColor），"
                "已使用中性配色。孩子看到的主色可能和「"
                f"{custom_theme.get('themeName', '自定义主题')}」不搭，建议补上 themeCSS。",
                file=sys.stderr,
            )
    config = build_config(
        prompt=prompt,
        skill=block.get("skillId"),
        theme=theme_id,
        seed=block.get("seed"),
        story_overrides=block.get("storyOverrides") or custom_theme,
        copy_overrides=copy_overrides,
        numbers=block.get("numbers"),
        force_random=force_random,
        themes=themes,
        allow_default_theme=allow_default_theme,
    )
    if custom_theme:
        config["visualKind"] = custom_theme.get("visualKind", "generic")
        config["themeId"] = theme_id
        config["themeName"] = custom_theme.get("themeName", "自定义主题")
        symbols = _custom_theme_symbols(custom_theme)
        if symbols:
            config["symbols"] = symbols
        else:
            print(
                f"[学习娃] 提示：customTheme「{config['themeName']}」没有 heroSvg/itemSvg，"
                "角色和物品会用通用造型，和主题未必搭。建议自己画一份内联 SVG（方法见 "
                "references/lesson-block-format.md 的「自画主题造型」）。",
                file=sys.stderr,
            )
    return config


def resolve_template() -> Path:
    """模板缺失时给出可执行的修复建议，而不是抛 traceback。"""
    candidates = [
        TEMPLATE,
        ROOT / "assets" / "learnwa-template.html",  # 兼容旧版目录名
        Path.cwd() / "templates" / "learnwa-template.html",
        Path.cwd() / "assets" / "learnwa-template.html",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise LearnWaError(
        "找不到 H5 模板文件 templates/learnwa-template.html，无法生成页面。\n"
        f"    期望位置：{TEMPLATE}\n"
        "    可能原因：技能目录里的 templates 被移动或删除了。\n"
        "    修复：确认 neway-learnwa 技能目录完整（SKILL.md / templates / references / scripts 四个都在），必要时重新安装该技能。",
        code=EXIT_SKILL,
    )


def load_block(path: str) -> dict:
    block_path = Path(path).expanduser()
    if not block_path.is_file():
        raise LearnWaError(
            f"找不到分块文件：{block_path}\n"
            "    可能原因：路径写错、文件被移动，或忘了先写 lesson-block.json。\n"
            "    修复：检查路径；如果不想用分块，可以直接给一句话：\n"
            '      python generate_learnwa.py "我要一个破十法，孩子喜欢飞机"'
        )
    raw = block_path.read_text(encoding="utf-8")
    if not raw.strip():
        raise LearnWaError(
            f"分块文件是空的：{block_path}\n"
            "    修复：至少写上 input 和 skillId，参考 references/lesson-block-format.md 的最小示例。"
        )
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise LearnWaError(
            f"分块 JSON 格式有误：{block_path}\n"
            f"    位置：第 {exc.lineno} 行第 {exc.colno} 列 —— {exc.msg}\n"
            "    常见原因：多写或漏写逗号、用了中文引号“”、键名没加引号、末尾多了逗号。\n"
            "    修复：把该处改好后重跑；也可用 python -m json.tool 先校验。"
        ) from None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="generate_learnwa.py",
        description="学习娃 LearnWa：把一句话或一个 lesson-block.json 合成为单文件 H5 数学教具。",
        epilog=(
            "示例：\n"
            '  python generate_learnwa.py "我要一个破十法，孩子喜欢飞机"\n'
            "  python generate_learnwa.py --block lesson-block.json --output docs/lesson.html\n"
            "  python generate_learnwa.py --list\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("prompt", nargs="?", default=None, help="家长自然语言输入")
    parser.add_argument("--block", default=None, help="个性化 lesson-block.json 路径；提供后 Bot 不需要生成完整 HTML")
    parser.add_argument("--skill", choices=list(SKILLS), default=None, help="指定数学方法")
    parser.add_argument("--theme", choices=list(THEMES), default=None, help="指定内置主题")
    parser.add_argument("--seed", type=int, default=None, help="固定随机种子，用于复现同一道题")
    parser.add_argument("--output", default=None, help="输出 HTML 路径")
    parser.add_argument("--force-random", action="store_true", help="numbers 不合规时改用随机题目，而不是报错")
    parser.add_argument(
        "--allow-default-theme",
        action="store_true",
        help="用户点名了非内置主题时，仍然使用默认「交通工具」（默认会报错并提示改用 customTheme）",
    )
    parser.add_argument("--list", action="store_true", help="列出可用的数学方法与内置主题")
    return parser


def _print_catalog() -> None:
    print("可用的数学方法（skillId）：")
    for key, meta in SKILLS.items():
        print(f"  {key:<12} {meta['skillName']}  {meta['englishName']}")
    print("\n内置主题（themeId）：")
    for key, meta in THEMES.items():
        print(f"  {key:<18} {meta['themeName']}  物品示例：{meta['itemNames'][0]}")
    print("\n孩子的专属兴趣（小猫钓鱼、足球、城堡等）请用 customTheme，不必新增内置主题。")
    print("注意：只要用户点名了主题，脚本就不会静默换成默认主题，而是要求你用 customTheme 实现。")


def main() -> int:
    args = build_parser().parse_args()

    if args.list:
        _print_catalog()
        return 0

    if args.block:
        block = load_block(args.block)
        config = build_config_from_block(
            block, force_random=args.force_random, allow_default_theme=args.allow_default_theme
        )
    else:
        prompt = args.prompt or "我要一个破十法"
        if not detect_skill(prompt):
            print(
                "[学习娃] 提示：这句话里没有明确的方法名，已默认使用「破十法」。"
                "需要其他方法请写明：凑十法 / 平十法。",
                file=sys.stderr,
            )
        mentioned = "" if args.theme else extract_theme_mention(prompt)
        if args.allow_default_theme and mentioned:
            print(
                f"[学习娃] 提示：你点名了主题「{mentioned}」，但加了 --allow-default-theme，"
                "所以这次仍然使用默认「交通工具」。如果这不是你要的，请改用 customTheme 分块。",
                file=sys.stderr,
            )
        config = build_config(
            prompt,
            args.skill,
            args.theme,
            args.seed,
            force_random=args.force_random,
            allow_default_theme=args.allow_default_theme,
        )

    template = resolve_template()
    template_text = template.read_text(encoding="utf-8")
    if "__CONFIG_PLACEHOLDER__" not in template_text:
        raise LearnWaError(
            "模板文件里缺少 __CONFIG_PLACEHOLDER__ 占位符，无法写入配置。\n"
            f"    文件：{template}\n"
            "    可能原因：模板被改坏了。\n"
            "    修复：从技能原始版本恢复 templates/learnwa-template.html。",
            code=EXIT_SKILL,
        )
    html = template_text.replace("__CONFIG_PLACEHOLDER__", json.dumps(config, ensure_ascii=False, indent=2))

    if args.output:
        out = Path(args.output).expanduser()
    else:
        out = OUT_DIR / f"learnwa-{config['skillId']}-{config['themeId']}.html"
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
    except OSError as exc:
        raise LearnWaError(
            f"写文件失败：{out}\n"
            f"    原因：{exc.strerror or exc}\n"
            "    修复：换个可写目录，或先关掉占用了该文件的程序，再用 --output 指定新路径。"
        ) from None

    print(out)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except LearnWaError as err:
        print(f"\n[学习娃] 无法生成教具\n  {err.message}\n", file=sys.stderr)
        sys.exit(err.code)
    except KeyboardInterrupt:
        print("\n[学习娃] 已取消。", file=sys.stderr)
        sys.exit(130)
    except Exception:  # noqa: BLE001 - 兜底，避免给用户看原始 traceback
        print(
            "\n[学习娃] 遇到了未预期的问题，教具没有生成。\n"
            "  修复：先用 --list 确认参数，再重跑一次；如果仍然失败，把下面两行贴给助手排查。\n"
            f"  {traceback.format_exc().strip().splitlines()[-1]}\n"
            f"  脚本位置：{Path(__file__).resolve()}\n",
            file=sys.stderr,
        )
        sys.exit(1)
