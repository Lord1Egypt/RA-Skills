#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
幼儿园思维课程体系 - 练习页生成器
生成 A4 可打印的 HTML 思维训练页 + JSON 答案。

支持主题 (--topics):
    classify  分类      match    配对/对应
    same      找相同    diff     找不同
    order     排序      pattern  规律/模式
    shape     图形      position 方位/空间
    compare   比较      maze     迷宫      swap    等量代换

支持语言 (--lang):
    zh  中文界面（默认）
    en  英文界面

题型以插件形式存放在 ./generators/ 目录，新增题型只需往该目录添加 g_*.py，
无需改动本文件。所有素材与文案见 ./common.py（含 I18N 中英文词典）。

用法示例:
    python generate_worksheet.py --level L2 --count 8 --seed 7 \
        --out 幼儿思维_L2.html --json 幼儿思维_L2_答案.json
    python generate_worksheet.py --level L3 --topics pattern,shape,position
    python generate_worksheet.py --level L1 --lang en --name Tom --count 6
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

# 合并插件声明的等级：仅补充「尚未被任何等级收录」的新题型。
# 注意：必须按"是否已出现在任意等级"判断，否则已收录题型会被重复追加（权重翻倍），
# 且新题型会被塞进全部等级（导致 L1 出现等量代换等超纲题）。
LEVEL_TOPICS = {k: list(v) for k, v in C.LEVEL_TOPICS.items()}
_covered = {t for v in LEVEL_TOPICS.values() for t in v}
for _key, _lv in PLUGIN_LEVELS.items():
    if _key in GENERATORS and _key not in _covered:
        _targets = _lv if _lv else list(range(1, 5))
        for _L in _targets:
            LEVEL_TOPICS.setdefault(_L, []).append(_key)
        _covered.add(_key)

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


def balance_plan(plan, topics, rng):
    """观察/专注类题型（迷宫/找不同/找相同）单张不超过 MAX_OBSERVE 题。

    超出部分替换为本等级的其它题型；若本等级没有其它题型可用则原样返回。
    """
    others = [t for t in topics if t not in C.OBSERVE_TOPICS]
    if not others:
        return plan
    out, n_obs = [], 0
    for t in plan:
        if t in C.OBSERVE_TOPICS:
            if n_obs < C.MAX_OBSERVE:
                out.append(t)
                n_obs += 1
            else:
                out.append(rng.choice(others))
        else:
            out.append(t)
    return out


def render_html(name, level, activities, columns, with_answers, lang, score=False, no_name=False):
    T = I18N[lang]
    html_lang = "en" if lang == "en" else "zh"
    cols_class = {1: "grid1", 3: "grid3"}.get(columns, "grid2")
    cards = ""
    for a in activities:
        qcheck = f'<div class="qcheck">{T["qcheck"]}</div>' if score else ""
        cards += (
            f'<div class="card"><div class="t">{a["id"]}. {a["title"]}</div>'
            f'<div class="i">{a["instruction"]}</div>{a["html"]}{qcheck}</div>'
        )
    body = f'<div class="{cols_class}">{cards}</div>'
    ans_block = ""
    if with_answers:
        li = "".join(f"<li><b>{a['id']}. {a['title']}：</b>{a['answer']}</li>" for a in activities)
        ans_block = f'<div class="ans"><h2>{T["answer_title"]}</h2><ol>{li}</ol></div>'
    n = len(activities)
    # 姓名栏：始终是可手填的下划线框；
    #   - 默认（不传 --name 且无 --no-name）→ 空白框
    #   - --name <str> → 预填
    #   - --no-name → 强制空白（覆盖来自 JSON / CLI 的任何预填）
    if no_name or not name:
        name_html = '<span class="fill">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>'
    else:
        # 转义避免 HTML 注入
        safe = name.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        name_html = f'<span class="fill">{safe}</span>'
    meta = T["name_label_prefix"] + name_html + T["name_label_suffix"].format(n=n)
    # 评分栏：可选，默认不出现
    score_block = ""
    if score:
        score_block = (
            f'<div class="score"><div class="t2">{T["score_title"]}</div>'
            f'<div class="row2">'
            f'<span>{T["score_points"]}<span class="fill sm">&nbsp;&nbsp;&nbsp;&nbsp;</span></span>'
            f'<span>{T["score_correct"]}<span class="fill sm">&nbsp;&nbsp;&nbsp;&nbsp;</span>{T["score_total_suffix"].format(n=n)}</span>'
            f'<span>{T["score_date"]}<span class="fill sm">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></span>'
            f'</div>'
            f'<div>{T["score_comment"]}<span class="fill">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></div></div>'
        )
    return (
        f"<!DOCTYPE html><html lang=\"{html_lang}\"><head><meta charset=\"utf-8\">{C.CSS}"
        f"<title>{T['page_title'].format(level=level)}</title></head><body>"
        f'<div class="sheet l{level}">'
        f'<div class="head"><h1>{T["head_title"].format(level=level)}</h1>'
        f'<div class="meta">{meta}</div></div>'
        f"{body}{ans_block}{score_block}"
        f'<div class="brand">{T["brand"]}</div>'
        f"</div></body></html>"
    )


def main():
    ap = argparse.ArgumentParser(description="幼儿园思维课程体系练习页生成器")
    ap.add_argument("--level", default="L1", help="等级 L1-L4")
    ap.add_argument("--count", type=int, default=0, help="题目数量（0=按等级默认；上限 {}）".format(C.MAX_COUNT))
    ap.add_argument("--topics", default="", help="指定题型，逗号分隔（拼错会列出合法值）")
    ap.add_argument("--seed", type=int, default=None, help="随机种子；不指定则每次随机（指定 0 也可复现）")
    ap.add_argument("--name", default="", help="孩子姓名（页眉）")
    ap.add_argument("--lang", default="zh", choices=["zh", "en"], help="界面语言 zh/en")
    ap.add_argument("--columns", type=int, default=2, choices=[1, 2, 3], help="排版列数 1/2/3")
    ap.add_argument("--no-answers", action="store_true", help="不输出答案（口头作答）")
    ap.add_argument("--score", action="store_true", help="页尾显示得分/评分栏（打印后手填，默认不显示）")
    ap.add_argument("--out", default="", help="HTML 输出路径（非 --list 时必填）")
    ap.add_argument("--json", default="", help="答案 JSON 输出路径（非 --list 时必填）")
    ap.add_argument("--preset", default="", help="diagnostic=生成诊断卷")
    ap.add_argument("--review", default="", help="旧答案 JSON，用于错题重练")
    ap.add_argument("--wrong", default="", help="错题 id 列表，逗号分隔")
    ap.add_argument("--regen", default="", help="从旧答案 JSON 复现原套题（用其 seed）")
    ap.add_argument("--no-name", action="store_true", help="强制姓名栏空白（即使 JSON 里有也忽略，覆盖 --name）")
    ap.add_argument("--list", action="store_true", help="列出可用题型与等级映射后退出，不生成练习页")
    args = ap.parse_args()

    if args.list:
        # 输出当前等级↔题型映射矩阵，便于快速浏览
        all_topics = sorted(set(GENERATORS.keys()) | {t for v in LEVEL_TOPICS.values() for t in v})
        print("== 可用题型 × 等级 ==")
        header = "topic".ljust(12) + " ".join(f"L{i}".rjust(4) for i in range(1, 5)) + "  简介"
        print(header)
        title_zh = C.I18N["zh"]
        brief = {k.split("_", 1)[1]: v for k, v in title_zh.items() if k.startswith("title_")}
        for t in all_topics:
            row = t.ljust(12)
            for L in range(1, 5):
                row += ("  ✓ " if t in LEVEL_TOPICS.get(L, []) else "  · ").rjust(4)
            row += "  " + brief.get(t, "?")
            print(row)
        print("\n共 {} 题型；当前等级池：L1={} 个, L2={} 个, L3={} 个, L4={} 个".format(
            len(all_topics), *(len(LEVEL_TOPICS.get(L, [])) for L in range(1, 5))))
        return

    if not args.out or not args.json:
        ap.error("--out and --json required (or use --list to only inspect)")

    lang = args.lang
    level = level_int(args.level)
    level = max(1, min(4, level))
    seed = args.seed if args.seed is not None else C.rid()
    rng = random.Random(seed)

    defaults = C.DEFAULT_COUNTS
    count = args.count if args.count > 0 else (10 if args.preset == "diagnostic" else defaults[level])
    count = max(1, min(C.MAX_COUNT, count))  # 硬规则：单次不超过 30 题

    if args.regen:
        # 从旧答案 JSON 复现原套题：用其存储的 seed、level、name、lang、score、count、topics
        with open(args.regen, "r", encoding="utf-8") as f:
            old = json.load(f)
        if "seed" not in old:
            ap.error("该 JSON 不含 seed 字段（旧版本生成），无法复现")
        # 全字段覆盖 CLI 默认值；CLI 显式传入的非默认参数仍优先
        seed = old["seed"]
        level = old.get("level", level)
        lang = old.get("lang", lang)
        if not args.name:
            args.name = old.get("name", args.name)
        if not args.score:
            args.score = bool(old.get("score", False))
        count = old.get("count", count)
        count = max(1, min(C.MAX_COUNT, count))
        rng = random.Random(seed)
        topics = LEVEL_TOPICS[level]
        plan = [rng.choice(topics) for _ in range(count)]
        plan = balance_plan(plan, topics, rng)
        activities = build_activities(level, plan, rng, lang)
    elif args.review:
        with open(args.review, "r", encoding="utf-8") as f:
            old = json.load(f)
        level = old.get("level", level)        # 错题重练沿用原等级
        lang = old.get("lang", lang)           # 错题重练沿用原语言
        wrong_ids = [int(x) for x in args.wrong.split(",") if x.strip()] if args.wrong else []
        if wrong_ids:
            wrong_topics = [a["topic"] for a in old["activities"] if a["id"] in wrong_ids]
        else:
            wrong_topics = list({a["topic"] for a in old["activities"]})
        # 每个错题配 2 道同型新题；并按"该等级可用题型"过滤掉任何超纲误传
        topics_pool = LEVEL_TOPICS[level]
        wrong_topics = [t for t in wrong_topics if t in topics_pool] or topics_pool
        plan = []
        for t in wrong_topics:
            plan += [t, t]
        # 错题重练也要遵守观察类题型上限（避免家长连续送一堆迷宫）
        plan = balance_plan(plan, topics_pool, rng)
        activities = build_activities(level, plan, rng, lang)
    else:
        if args.topics:
            wanted = [t.strip() for t in args.topics.split(",") if t.strip()]
            bad = [t for t in wanted if t not in GENERATORS]
            if bad:
                ap.error("未知题型: {}；可用题型: {}".format(
                    ", ".join(bad), ", ".join(sorted(GENERATORS))))
            # 限定到本等级可用题型，避免使用者把高等级题塞给小班
            topics = [t for t in wanted if t in LEVEL_TOPICS[level]] or LEVEL_TOPICS[level]
        else:
            topics = LEVEL_TOPICS[level]
        if args.preset == "diagnostic":
            # 诊断卷必须覆盖全部题型；若指定 count 不足则自动扩到题型数
            base = list(GENERATORS.keys())
            count = max(count, len(base))
            plan = (base * ((count // len(base)) + 1))[:count]
            plan = balance_plan(plan, list(GENERATORS.keys()), rng)
        else:
            plan = [rng.choice(topics) for _ in range(count)]
            plan = balance_plan(plan, topics, rng)
        activities = build_activities(level, plan, rng, lang)

    html = render_html(args.name, level, activities, args.columns, not args.no_answers, lang, args.score, args.no_name)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)
    with open(args.json, "w", encoding="utf-8") as f:
        json.dump({
            "level": level, "name": args.name, "lang": lang, "count": len(activities),
            "score": args.score, "seed": seed,
            "topics": sorted({a["topic"] for a in activities}),
            "activities": activities,
        }, f, ensure_ascii=False, indent=2)
    print(f"已生成: {args.out}")
    print(f"答案(JSON): {args.json}")
    print(f"等级 L{level} | 语言 {lang} | 题型: {', '.join(sorted({a['topic'] for a in activities}))} | 题量 {len(activities)}")
    if seed is not None:
        print(f"种子: {seed}  （可加 --seed {seed} 复现本套题；或 --regen {args.json} 一键复现）")


if __name__ == "__main__":
    main()
