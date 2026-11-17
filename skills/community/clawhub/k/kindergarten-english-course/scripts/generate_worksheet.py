#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
幼儿园英语全套课程 - 练习页生成器
生成 A4 可打印的 HTML 英语练习页 + JSON 答案。

支持主题 (--topics):
    letter_trace  字母描红      letter_match  大小写配对
    letter_sound  字母发音      phonics_cvc   自然拼读
    word_pic      看图识词      vocab_theme   主题词汇
    fill_letter   补全单词      sight_words   高频词
    sentence      简单句型      dialogue      情景对话

支持语言 (--lang):
    zh  中文指导语（默认，适合中国家庭）
    en  英文指导语（双语 / 全英环境）

题型以插件形式存放在 ./generators/ 目录，新增题型只需往该目录添加 g_*.py。

用法示例:
    python generate_worksheet.py --level L2 --count 8 --seed 7 \
        --out 幼儿英语_L2.html --json 幼儿英语_L2_答案.json
    python generate_worksheet.py --level L3 --topics sentence,sight_words
    python generate_worksheet.py --level L1 --lang en --name Tom --count 6
    python generate_worksheet.py --preset diagnostic
    python generate_worksheet.py --review 旧答案.json --wrong 4,7
"""
import argparse
import json
import os
import random
import sys

import common as C
from generators import load_generators

GENERATORS, PLUGIN_LEVELS = load_generators()

# 合并插件声明的等级（新题型若未内置进 LEVEL_TOPICS 则自动加入对应等级）
LEVEL_TOPICS = {k: list(v) for k, v in C.LEVEL_TOPICS.items()}
for _key, _lv in PLUGIN_LEVELS.items():
    if _key in GENERATORS and _key not in LEVEL_TOPICS:
        _targets = _lv if _lv else list(range(1, 5))
        for _L in _targets:
            LEVEL_TOPICS.setdefault(_L, []).append(_key)

I18N = C.I18N


def level_int(level_str):
    try:
        return int(str(level_str).replace("L", "").strip())
    except Exception:
        return 1


def build_activities(level, plan, rng, lang):
    activities = []
    for idx, topic in enumerate(plan, 1):
        title, instr, html, ans = GENERATORS[topic](level, rng, lang)
        activities.append({
            "id": idx, "topic": topic, "title": title,
            "instruction": instr, "html": html, "answer": ans,
        })
    return activities


def render_html(name, level, activities, columns, with_answers, lang, score=False):
    T = I18N[lang]
    html_lang = "en" if lang == "en" else "zh"
    cols_class = "grid3" if columns == 3 else "grid2"
    cards = ""
    for a in activities:
        cards += (
            f'<div class="card"><div class="t">{a["id"]}. {a["title"]}</div>'
            f'<div class="i">{a["instruction"]}</div>{a["html"]}</div>'
        )
    body = f'<div class="{cols_class}">{cards}</div>'
    ans_block = ""
    if with_answers:
        li = "".join(f"<li><b>{a['id']}. {a['title']}：</b>{a['answer']}</li>" for a in activities)
        ans_block = f'<div class="ans"><h2>{T["answer_title"]}</h2><ol>{li}</ol></div>'
    n = len(activities)
    name_html = f'<span class="fill">{name}</span>' if name else '<span class="fill">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>'
    meta = T["name_label_prefix"] + name_html + T["name_label_suffix"].format(n=n)
    score_block = ""
    if score:
        score_block = (
            f'<div class="score"><div class="t2">{T["score_title"]}</div>'
            f'<div class="row2">'
            f'<span>{T["score_points"]}<span class="fill sm">&nbsp;&nbsp;&nbsp;&nbsp;</span></span>'
            f'<span>{T["score_correct"]}<span class="fill sm">&nbsp;&nbsp;&nbsp;&nbsp;</span>{T["score_total_suffix"].format(n=n)}</span>'
            f'</div>'
            f'<div>{T["score_comment"]}<span class="fill">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></div></div>'
        )
    lvl_name = C.LEVEL_NAME.get(level, f"L{level}")
    return (
        f"<!DOCTYPE html><html lang=\"{html_lang}\"><head><meta charset=\"utf-8\"><title>{T['page_title'].format(level=lvl_name)}</title><style>{C.CSS}</style></head><body>"
        f'<div class="no-print"><button onclick="window.print()">🖨 打印 / 另存为 PDF</button>'
        f'　<span style="font-size:12px;color:#888">{T["hint_print"]}</span></div>'
        f'<div class="sheet"><div class="head"><h1>{T["head_title"].format(level=lvl_name)}</h1>'
        f'<div class="meta">{meta}</div></div>'
        f"{body}{ans_block}{score_block}</div></body></html>"
    )


def main():
    ap = argparse.ArgumentParser(description="幼儿园英语练习页生成器")
    ap.add_argument("--level", default="L1", help="等级 L1-L4")
    ap.add_argument("--count", type=int, default=0, help="题目数量（0=按等级默认）")
    ap.add_argument("--topics", default="", help="指定题型，逗号分隔")
    ap.add_argument("--seed", type=int, default=0, help="随机种子（0 随机）")
    ap.add_argument("--name", default="", help="孩子姓名（页眉）")
    ap.add_argument("--lang", default="zh", choices=["zh", "en"], help="指导语语言 zh/en")
    ap.add_argument("--columns", type=int, default=2, help="排版列数 2 或 3")
    ap.add_argument("--no-answers", action="store_true", help="不输出答案（口头作答）")
    ap.add_argument("--score", action="store_true", help="页尾显示评价栏（默认不显示）")
    ap.add_argument("--out", required=True, help="HTML 输出路径")
    ap.add_argument("--json", required=True, help="答案 JSON 输出路径")
    ap.add_argument("--preset", default="", help="diagnostic=生成诊断卷")
    ap.add_argument("--review", default="", help="旧答案 JSON，用于错题重练")
    ap.add_argument("--wrong", default="", help="错题 id 列表，逗号分隔")
    args = ap.parse_args()

    lang = args.lang
    level = level_int(args.level)
    level = max(1, min(4, level))
    rng = random.Random(args.seed if args.seed else C.rid())

    defaults = C.DEFAULT_COUNTS
    count = args.count if args.count > 0 else (10 if args.preset == "diagnostic" else defaults[level])

    if args.review:
        with open(args.review, "r", encoding="utf-8") as f:
            old = json.load(f)
        level = old.get("level", level)
        lang = old.get("lang", lang)
        wrong_ids = [int(x) for x in args.wrong.split(",") if x.strip()] if args.wrong else []
        if wrong_ids:
            wrong_topics = [a["topic"] for a in old["activities"] if a["id"] in wrong_ids]
        else:
            wrong_topics = list({a["topic"] for a in old["activities"]})
        plan = []
        for t in wrong_topics:
            plan += [t, t]  # 每个错题配 2 道同型新题
        activities = build_activities(level, plan, rng, lang)
    else:
        if args.topics:
            topics = [t.strip() for t in args.topics.split(",") if t.strip() in GENERATORS]
        else:
            topics = LEVEL_TOPICS[level]
        if args.preset == "diagnostic":
            base = list(GENERATORS.keys())
            plan = (base * ((count // len(base)) + 1))[:count]
        else:
            plan = [rng.choice(topics) for _ in range(count)]
        activities = build_activities(level, plan, rng, lang)

    html = render_html(args.name, level, activities, args.columns, not args.no_answers, lang, args.score)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)
    with open(args.json, "w", encoding="utf-8") as f:
        json.dump({
            "level": level, "name": args.name, "lang": lang, "count": len(activities),
            "score": args.score, "seed": rng.randint(1, 10 ** 6),
            "topics": sorted({a["topic"] for a in activities}),
            "activities": activities,
        }, f, ensure_ascii=False, indent=2)
    print(f"已生成: {args.out}")
    print(f"答案(JSON): {args.json}")
    print(f"等级 L{level} | 语言 {lang} | 题型: {', '.join(sorted({a['topic'] for a in activities}))} | 题量 {len(activities)}")


if __name__ == "__main__":
    main()
