#!/usr/bin/env python3
"""Generate a LearnWa single-file H5 lesson from natural language input."""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets" / "learnwa-template.html"
OUT_DIR = Path(r"D:\claw\workspace\workbuddy\work\docs")

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
    }
}

SKILLS = {
    "break_ten": {"skillName":"破十法","englishName":"Break Ten Method","templateId":"remove_to_ten"},
    "make_ten": {"skillName":"凑十法","englishName":"Make Ten Method","templateId":"fill_to_ten"},
    "level_ten": {"skillName":"平十法","englishName":"Level Ten Method","templateId":"subtract_to_ten_then_continue"},
}


def detect_skill(text: str) -> str:
    if any(k in text for k in ["凑十", "进位", "加法", "+"]):
        return "make_ten"
    if any(k in text for k in ["平十", "减到10", "减到十", "整十"]):
        return "level_ten"
    if any(k in text for k in ["借十", "破十", "退位", "十几减", "减法", "-"]):
        return "break_ten"
    return "break_ten"


def detect_theme(text: str) -> str:
    if any(k in text for k in ["卡", "收藏", "兑换", "集齐"]):
        return "card_collection"
    if any(k in text for k in ["熊", "小熊", "熊宝宝", "蜂蜜"]):
        return "animal_bear"
    if any(k in text for k in ["恐龙", "龙", "森林"]):
        return "dinosaur"
    if any(k in text for k in ["车", "交通", "火车", "汽车", "飞机"]):
        return "vehicle"
    return "vehicle"


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


def story_for(theme: str, skill: str, q: dict) -> dict:
    t = THEMES[theme]
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


def question_from_numbers(skill: str, numbers: dict | None) -> dict | None:
    if not numbers:
        return None
    a = int(numbers.get("a", 0))
    b = int(numbers.get("b", 0))
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
) -> dict:
    skill = skill or detect_skill(prompt)
    theme = theme or detect_theme(prompt)
    q = question_from_numbers(skill, numbers) or question_for(skill, seed)
    story = story_for(theme, skill, q)
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
        "themeCSS": THEMES[theme]["css"],
    }


def build_config_from_block(block: dict) -> dict:
    prompt = block.get("input") or block.get("prompt") or "我要一个破十法"
    copy_overrides = block.get("copyOverrides") or {}
    if block.get("difficulty"):
        copy_overrides = {**copy_overrides, "difficulty": block["difficulty"]}
    custom_theme = block.get("customTheme") or {}
    theme_id = block.get("themeId") or custom_theme.get("themeId")
    if custom_theme:
        theme_id = theme_id or "custom_theme"
        THEMES[theme_id] = {
            "themeName": custom_theme.get("themeName", "自定义主题"),
            "characters": [custom_theme.get("character", "小朋友")],
            "itemNames": [custom_theme.get("itemName", "小物品")],
            "goals": [custom_theme.get("goal", "完成任务")],
            "removeVerb": custom_theme.get("removeVerb", "拿走"),
            "addVerb": custom_theme.get("addVerb", "放进"),
            "rewardNames": [custom_theme.get("reward", "数学小达人")],
            "css": custom_theme.get("themeCSS", THEMES["vehicle"]["css"]),
        }
    config = build_config(
        prompt=prompt,
        skill=block.get("skillId"),
        theme=theme_id,
        seed=block.get("seed"),
        story_overrides=block.get("storyOverrides") or custom_theme,
        copy_overrides=copy_overrides,
        numbers=block.get("numbers"),
    )
    if custom_theme:
        config["visualKind"] = custom_theme.get("visualKind", "generic")
        config["themeId"] = theme_id
        config["themeName"] = custom_theme.get("themeName", "自定义主题")
    return config


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", nargs="?", default=None, help="家长自然语言输入")
    parser.add_argument("--block", default=None, help="个性化 lesson-block.json 路径；提供后 Bot 不需要生成完整 HTML")
    parser.add_argument("--skill", choices=list(SKILLS), default=None)
    parser.add_argument("--theme", choices=list(THEMES), default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    if args.block:
        block = json.loads(Path(args.block).read_text(encoding="utf-8"))
        config = build_config_from_block(block)
    else:
        config = build_config(args.prompt or "我要一个破十法", args.skill, args.theme, args.seed)
    html = TEMPLATE.read_text(encoding="utf-8").replace("__CONFIG_PLACEHOLDER__", json.dumps(config, ensure_ascii=False, indent=2))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = Path(args.output) if args.output else OUT_DIR / f"learnwa-{config['skillId']}-{config['themeId']}.html"
    out.write_text(html, encoding="utf-8")
    print(out)

if __name__ == "__main__":
    main()
