#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
幼儿园数学练习页生成器（识数 / 加减法体系课程）

按等级（L1-L5）与题型生成自包含的 A4 可打印 HTML 练习页，
可附带答案页，并可输出 JSON 题面数据供批改使用。

用法示例：
  python generate_worksheet.py --level L4 --count 20 --out 练习.html --json 答案.json
  python generate_worksheet.py --preset diagnostic --out 诊断卷.html
  python generate_worksheet.py --level L1 --topics count_objects,write_number --count 10 --no-answers
"""

import argparse
import json
import random
import sys
from datetime import datetime
from pathlib import Path

EMOJIS = ["🍎", "🍓", "🍌", "🍇", "🐟", "🐣", "🌸", "⭐", "🚗", "🐻", "🎈", "🍬", "🦋", "🐞", "🌰", "🐳"]

LEVEL_TOPICS = {
    "L1": ["count_objects", "write_number", "circle_number", "ordinal", "color_by_number"],
    "L2": ["count_objects", "next_number", "circle_number", "write_number", "color_by_number", "ordinal"],
    "L3": ["compare", "compose", "count_objects", "next_number", "picture_equation"],
    "L4": ["add", "sub", "missing_addend", "word_problem", "picture_equation"],
    "L5": ["add_carry", "sub_borrow", "mixed_20", "word_problem", "vertical"],
}

LEVEL_NAME = {
    "L1": "识数 1-5",
    "L2": "识数 6-10",
    "L3": "比大小与分解组成",
    "L4": "10 以内加减法",
    "L5": "20 以内进退位",
}

PER_PAGE = {"L1": 10, "L2": 10, "L3": 12, "L4": 16, "L5": 16}

BLANK = '<span class="blank"></span>'


def blank(width_em=None):
    if width_em:
        return f'<span class="blank" style="min-width:{width_em}em"></span>'
    return BLANK


# ---------------------------------------------------------------- 题目生成器
def q_count_objects(rng, level):
    lo, hi = (1, 5) if level == "L1" else (3, 10)
    n = rng.randint(lo, hi)
    e = rng.choice(EMOJIS)
    prompt = f'<div class="objs">{e * n}</div><div>一共有（{blank()}）个</div>'
    return {"topic": "count_objects", "level": level, "prompt": prompt, "answer": str(n)}


def q_write_number(rng, level):
    pool = list("12345") if level == "L1" else list("67890")
    n = rng.choice(pool)
    ghost = f'<span class="ghost">{n}</span>'
    cells = "".join(
        '<svg class="tian" viewBox="0 0 40 40" width="20mm" height="20mm">'
        '<rect x="0.75" y="0.75" width="38.5" height="38.5" fill="none" stroke="#555" stroke-width="1.5"/>'
        '<line x1="0" y1="20" x2="40" y2="20" stroke="#555" stroke-width="1" stroke-dasharray="3 2"/>'
        '<line x1="20" y1="0" x2="20" y2="40" stroke="#555" stroke-width="1" stroke-dasharray="3 2"/>'
        '</svg>' for _ in range(4)
    )
    prompt = (
        f'<div class="trace-lead">'
        f'<svg class="tian first" viewBox="0 0 40 40" width="20mm" height="20mm" data-n="{n}">'
        f'<rect x="0.75" y="0.75" width="38.5" height="38.5" fill="none" stroke="#c0392b" stroke-width="1.5"/>'
        f'<line x1="0" y1="20" x2="40" y2="20" stroke="#c0392b" stroke-width="1" stroke-dasharray="3 2"/>'
        f'<line x1="20" y1="0" x2="20" y2="40" stroke="#c0392b" stroke-width="1" stroke-dasharray="3 2"/>'
        f'</svg></div>'
        f'<div class="trace-row">照样子再写 4 个：</div>'
        f'<div class="trace-row">{cells}</div>'
    )
    return {
        "topic": "write_number",
        "level": level,
        "prompt": prompt,
        "answer": "书写题：看笔顺与占格",
    }


def q_circle_number(rng, level):
    hi = 5 if level == "L1" else 10
    target = rng.randint(1, hi)
    others = [rng.randint(0, hi) for _ in range(6)]
    pool = others + [target] * 3
    rng.shuffle(pool)
    row = "".join(f"<b>{d}</b>" for d in pool)
    prompt = f'<div>把数字 <b class="hl">{target}</b> 圈出来</div><div class="numrow">{row}</div>'
    return {"topic": "circle_number", "level": level, "prompt": prompt, "answer": f"圈出 3 个 {target}"}


def q_next_number(rng, level):
    reverse = level == "L3" and rng.random() < 0.35
    start = rng.randint(2, 7)
    seq = [start, start + 1, start + 2, start + 3]
    if reverse:
        seq = seq[::-1]
    hole = rng.randint(0, 3)
    parts = []
    for i, v in enumerate(seq):
        parts.append(blank() if i == hole else f"<b>{v}</b>")
    label = "倒着数，填一填" if reverse else "按顺序填数"
    prompt = f'<div>{label}：{", ".join(parts)}</div>'
    return {"topic": "next_number", "level": level, "prompt": prompt, "answer": str(seq[hole])}


def q_compare(rng, level):
    hi = 10 if level in ("L3", "L4") else 5
    a, b = rng.randint(1, hi), rng.randint(1, hi)
    ans = ">" if a > b else ("<" if a < b else "=")
    prompt = f'<div class="cmp"><b>{a}</b>{blank(2.4)}<b>{b}</b></div><div class="tip">填 &gt; 、&lt; 或 =</div>'
    return {"topic": "compare", "level": level, "prompt": prompt, "answer": ans}


def q_compose(rng, level):
    total = rng.randint(3, 5) if level == "L3" else rng.randint(6, 10)
    part = rng.randint(1, total - 1)
    other = total - part
    left_first = rng.random() < 0.5
    left = f"<b>{part}</b>" if left_first else blank(2.4)
    right = blank(2.4) if left_first else f"<b>{part}</b>"
    prompt = (
        f'<div class="tree">'
        f'<div class="tree-top"><b>{total}</b></div>'
        f'<div class="tree-mid">╱&nbsp;&nbsp;╲</div>'
        f'<div class="tree-bot"><span>{left}</span><span>{right}</span></div>'
        f"</div><div class=\"tip\">{total} 可以分成几和几</div>"
    )
    return {"topic": "compose", "level": level, "prompt": prompt, "answer": str(other)}


def q_add(rng, level):
    a = rng.randint(1, 8)
    b = rng.randint(1, 10 - a)
    prompt = f'<div class="calc"><b>{a}</b> + <b>{b}</b> = {blank()}</div>'
    return {"topic": "add", "level": level, "prompt": prompt, "answer": str(a + b)}


def q_sub(rng, level):
    a = rng.randint(2, 10)
    b = rng.randint(1, a)
    prompt = f'<div class="calc"><b>{a}</b> - <b>{b}</b> = {blank()}</div>'
    return {"topic": "sub", "level": level, "prompt": prompt, "answer": str(a - b)}


def q_missing_addend(rng, level):
    if level == "L5" or rng.random() < 0.5:
        a = rng.randint(2, 8)
        c = rng.randint(a + 1, min(10, a + 5))
        prompt = f'<div class="calc"><b>{a}</b> + {blank()} = <b>{c}</b></div>'
        return {"topic": "missing_addend", "level": level, "prompt": prompt, "answer": str(c - a)}
    c = rng.randint(3, 10)
    b = rng.randint(1, c - 1)
    prompt = f'<div class="calc"><b>{c}</b> - {blank()} = <b>{c - b}</b></div>'
    return {"topic": "missing_addend", "level": level, "prompt": prompt, "answer": str(b)}


def q_add_carry(rng, level):
    a = rng.randint(2, 9)
    b = rng.randint(10 - a + 1, min(9, 18 - a))
    prompt = f'<div class="calc"><b>{a}</b> + <b>{b}</b> = {blank()}</div><div class="tip">凑十法：{a} 和几凑成 10？</div>'
    return {"topic": "add_carry", "level": level, "prompt": prompt, "answer": str(a + b)}


def q_sub_borrow(rng, level):
    total = rng.randint(11, 18)
    ones = total % 10
    b = rng.randint(ones + 1, 9)
    prompt = f'<div class="calc"><b>{total}</b> - <b>{b}</b> = {blank()}</div><div class="tip">破十法：先算 10 - {b}</div>'
    return {"topic": "sub_borrow", "level": level, "prompt": prompt, "answer": str(total - b)}


def q_mixed_20(rng, level):
    return q_add_carry(rng, level) if rng.random() < 0.5 else q_sub_borrow(rng, level)


def q_ordinal(rng, level):
    """序数：从左（或从右）数第 N 个是哪一个。"""
    n = rng.randint(4, 6)
    pool = rng.sample(EMOJIS, n)
    pos = rng.randint(1, n)
    from_right = rng.random() < 0.3
    idx = n - pos + 1 if from_right else pos
    side = "右" if from_right else "左"
    row = "".join(f"<span>{e}</span>" for e in pool)
    prompt = (
        f'<div class="objs">{row}</div>'
        f'<div>从<b>{side}</b>数第 <b>{pos}</b> 个是哪一个？把它圈出来</div>'
    )
    return {
        "topic": "ordinal",
        "level": level,
        "prompt": prompt,
        "answer": f"第 {idx} 个 {pool[idx - 1]}",
    }


def q_color_by_number(rng, level):
    """按数取物：按要求给 N 个图形涂色。"""
    hi = 5 if level == "L1" else 10
    n = rng.randint(1, hi)
    total = n + rng.randint(1, 3)
    cells = "".join('<span class="cbox"></span>' for _ in range(total))
    prompt = f'<div>给 <b>{n}</b> 个 ○ 涂上颜色</div><div class="crow">{cells}</div>'
    return {"topic": "color_by_number", "level": level, "prompt": prompt, "answer": f"涂 {n} 个"}


def q_picture_equation(rng, level):
    """看图列式：根据图画写出完整算式。"""
    e = rng.choice(EMOJIS)
    minus = rng.random() < 0.35
    if level == "L5":
        a = rng.randint(6, 9)
        b = rng.randint(10 - a + 1, min(9, 18 - a))
        minus = False
    else:
        a = rng.randint(2, 8)
        b = rng.randint(1, a - 1) if minus else rng.randint(1, 10 - a)
    if minus:
        op, ans = "-", a - b
        pic = f'{e * (a - b)}<span class="del">{e * b}</span>'
        prompt = (
            f'<div class="pe"><span class="objs">{pic}</span></div>'
            f'<div class="calc">{blank(1.8)} - {blank(1.8)} = {blank(1.8)}</div>'
        )
    else:
        op, ans = "+", a + b
        prompt = (
            f'<div class="pe"><span class="objs">{e * a}</span>'
            f'<span class="peop">+</span><span class="objs">{e * b}</span></div>'
            f'<div class="calc">{blank(1.8)} + {blank(1.8)} = {blank(1.8)}</div>'
        )
    return {
        "topic": "picture_equation",
        "level": level,
        "prompt": prompt,
        "answer": f"{a} {op} {b} = {ans}",
    }


def q_vertical(rng, level):
    """竖式：20 以内进位加 / 退位减的竖式书写与计算。"""
    if rng.random() < 0.5:
        a = rng.randint(2, 9)
        b = rng.randint(10 - a + 1, min(9, 18 - a))
        op, ans = "+", a + b
    else:
        a = rng.randint(11, 18)
        b = rng.randint(a % 10 + 1, 9)
        op, ans = "-", a - b
    prompt = (
        '<div class="vert">'
        f'<div class="vrow"><span class="vph"></span><span>{a}</span></div>'
        f'<div class="vrow"><span class="vop">{op}</span><span>{b}</span></div>'
        '<div class="vline"></div>'
        f'<div class="vrow"><span class="vph"></span>{blank(1.8)}</div>'
        "</div>"
        '<div class="tip">先算个位：满十进一 / 不够减向十位借一</div>'
    )
    return {"topic": "vertical", "level": level, "prompt": prompt, "answer": str(ans)}


def q_word_problem(rng, level):
    if level == "L5":
        if rng.random() < 0.5:
            a = rng.randint(5, 9)
            b = rng.randint(10 - a + 1, min(9, 18 - a))
            text = f"小红有 {a} 支 ✏️，小刚有 {b} 支 ✏️，两人一共有几支？"
            ans, ask = a + b, "一共"
        else:
            total = rng.randint(11, 18)
            b = rng.randint(total % 10 + 1, 9)
            text = f"图书角有 {total} 本 📚，借出 {b} 本，还剩几本？"
            ans, ask = total - b, "还剩"
    else:
        kind = rng.choice(["add", "sub_left", "sub_diff"])
        if kind == "add":
            a = rng.randint(1, 7)
            b = rng.randint(1, 10 - a)
            text = f"盘子里有 {a} 个 🍎，妈妈又放进来 {b} 个 🍎，现在一共有几个？"
            ans, ask = a + b, "一共"
        elif kind == "sub_left":
            c = rng.randint(3, 10)
            b = rng.randint(1, c - 1)
            text = f"一共有 {c} 颗 🍬，小明吃了 {b} 颗，还剩几颗？"
            ans, ask = c - b, "还剩"
        else:
            a = rng.randint(3, 9)
            b = rng.randint(1, a - 1)
            text = f"哥哥折了 {a} 颗 ⭐，弟弟折了 {b} 颗 ⭐，哥哥比弟弟多几颗？"
            ans, ask = a - b, "多"
    prompt = f'<div class="wp">{text}</div><div class="wp-ans">算式：{blank(3.2)}　　答：{blank(2.2)}</div>'
    return {"topic": "word_problem", "level": level, "prompt": prompt, "answer": str(ans), "note": ask}


GENERATORS = {
    "count_objects": q_count_objects,
    "write_number": q_write_number,
    "circle_number": q_circle_number,
    "next_number": q_next_number,
    "compare": q_compare,
    "compose": q_compose,
    "add": q_add,
    "sub": q_sub,
    "missing_addend": q_missing_addend,
    "word_problem": q_word_problem,
    "add_carry": q_add_carry,
    "sub_borrow": q_sub_borrow,
    "mixed_20": q_mixed_20,
    "ordinal": q_ordinal,
    "color_by_number": q_color_by_number,
    "picture_equation": q_picture_equation,
    "vertical": q_vertical,
}

TOPIC_LABEL = {
    "count_objects": "数一数",
    "write_number": "数字书写",
    "circle_number": "认数字",
    "next_number": "数的顺序",
    "compare": "比大小",
    "compose": "分解组成",
    "add": "加法",
    "sub": "减法",
    "missing_addend": "填未知数",
    "word_problem": "应用题",
    "add_carry": "进位加",
    "sub_borrow": "退位减",
    "mixed_20": "20以内混合",
    "ordinal": "序数",
    "color_by_number": "按数涂色",
    "picture_equation": "看图列式",
    "vertical": "竖式计算",
}


# ---------------------------------------------------------------- 组卷
def build_questions(level, topics, count, rng):
    """组卷：同一份卷内不出现重复题面；题型取值空间耗尽时允许重复，避免死循环。"""
    qs = []
    seen = set()
    for i in range(count):
        topic = topics[i % len(topics)]
        q = GENERATORS[topic](rng, level)
        for _ in range(40):
            if q["prompt"] not in seen:
                break
            q = GENERATORS[topic](rng, level)
        seen.add(q["prompt"])
        q["no"] = i + 1
        qs.append(q)
    return qs


def build_diagnostic(rng):
    plan = [
        ("L1", "count_objects"),
        ("L1", "circle_number"),
        ("L2", "count_objects"),
        ("L2", "next_number"),
        ("L3", "compare"),
        ("L3", "compose"),
        ("L4", "add"),
        ("L4", "sub"),
        ("L5", "add_carry"),
        ("L5", "sub_borrow"),
    ]
    qs = []
    for i, (lv, topic) in enumerate(plan):
        q = GENERATORS[topic](rng, lv)
        q["no"] = i + 1
        q["level"] = lv
        qs.append(q)
    return qs


def build_review(args, rng):
    """错题重练：读取上次练习的 JSON，按错题所属题型生成同型新题。"""
    data = json.loads(Path(args.review).read_text(encoding="utf-8"))
    prev = {q["no"]: q for q in data.get("questions", [])}
    if not args.wrong:
        sys.exit("--review 需要配合 --wrong 指定错题号，例如 --wrong 3,7,12")
    wrong_nos = [
        int(t.strip())
        for t in args.wrong.replace("，", ",").split(",")
        if t.strip().isdigit()
    ]
    hit = [n for n in wrong_nos if n in prev]
    if not hit:
        sys.exit(f"未在 {args.review} 中找到题号：{args.wrong}")
    topics = [prev[n]["topic"] for n in hit]
    levels = [prev[n]["level"] for n in hit]
    level = max(set(levels), key=levels.count)
    if level not in LEVEL_TOPICS:
        level = args.level
    qs = build_questions(level, topics, len(topics) * 2, rng)
    labels = "、".join(dict.fromkeys(TOPIC_LABEL[t] for t in topics))
    title = args.title or f"错题重练 · {level} {LEVEL_NAME[level]}"
    subtitle = f"针对上次第 {args.wrong} 题 · 题型：{labels} · 同型新题 {len(qs)} 题"
    per_page = args.per_page or PER_PAGE[level]
    return level, qs, title, subtitle, per_page


# ---------------------------------------------------------------- 渲染
CSS = """
:root{--ink:#1a1a1a;--line:#333;--muted:#888;}
*{box-sizing:border-box;}
body{margin:0;background:#f2f2f0;color:var(--ink);
  font-family:"Kaiti SC","STKaiti","KaiTi","楷体","Microsoft YaHei",sans-serif;}
.no-print{text-align:center;padding:10px;background:#fff;position:sticky;top:0;z-index:9;
  border-bottom:1px solid #ddd;font-family:"Microsoft YaHei",sans-serif;}
.no-print button{padding:8px 22px;font-size:14px;cursor:pointer;}
.sheet{width:190mm;min-height:273mm;margin:8mm auto;padding:8mm 9mm;background:#fff;
  box-shadow:0 1px 6px rgba(0,0,0,.15);page-break-after:always;position:relative;
  display:flex;flex-direction:column;}
.sheet:last-child{page-break-after:auto;}
.head{border-bottom:2px solid var(--ink);padding-bottom:3mm;margin-bottom:5mm;}
.title{font-size:19pt;font-weight:700;letter-spacing:1px;}
.sub{font-size:11pt;color:#555;margin-top:1mm;}
.meta{display:flex;gap:6mm;font-size:11pt;margin-top:2mm;flex-wrap:wrap;}
.meta span{border-bottom:1px solid var(--line);min-width:26mm;display:inline-block;}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:6mm 9mm;flex:1;align-content:start;}
.q{font-size:16pt;line-height:1.5;break-inside:avoid;}
.q .no{font-weight:700;margin-right:2mm;}
.q .lvtag{font-size:9pt;color:#a00;border:1px solid #a00;border-radius:3px;
  padding:0 3px;margin-left:2mm;vertical-align:2px;font-family:"Microsoft YaHei",sans-serif;}
.blank{display:inline-block;min-width:2.2em;height:1.5em;border-bottom:2px solid var(--line);
  vertical-align:middle;margin:0 2mm;}
.objs{font-size:23pt;letter-spacing:2mm;line-height:1.3;margin-bottom:1mm;}
.numrow{font-size:17pt;letter-spacing:4mm;margin-top:1mm;}
.calc{font-size:19pt;letter-spacing:1px;}
.cmp{font-size:19pt;}
.tip{font-size:10pt;color:#777;margin-top:1mm;font-family:"Microsoft YaHei",sans-serif;}
.hl{color:#c0392b;}
.tree{text-align:center;font-size:17pt;line-height:1.25;}
.tree-mid{font-size:14pt;letter-spacing:6mm;color:#555;}
.tree-bot{display:flex;justify-content:center;gap:12mm;margin-top:-1mm;}
.wp{font-size:13.5pt;line-height:1.55;font-family:"Microsoft YaHei",sans-serif;}
.wp-ans{margin-top:2mm;font-size:14pt;}
.trace-lead{display:flex;align-items:center;gap:4mm;}
/* 数字描红：浅灰大字，便于孩子对照 */
.ghost{font-size:34pt;color:#888;font-weight:600;}
/* 田字格用 inline SVG 绘制（外框 + 十字中线全部矢量，PDF 打印完美）
   这里只控制布局，不画线 */
.tian{vertical-align:top;margin:0 1mm;display:inline-block;}
.trace-row{margin-top:2mm;display:flex;gap:4mm;align-items:center;flex-wrap:wrap;font-size:12pt;}
.foot{margin-top:auto;padding-top:4mm;font-size:10pt;color:#999;display:flex;justify-content:space-between;}
.answers .alist{display:grid;grid-template-columns:1fr 1fr;gap:3mm 9mm;font-size:13pt;}
.answers .alist div{border-bottom:1px dotted #ccc;padding-bottom:1mm;}
.atopic{color:#a0a0a0;font-size:10pt;margin-left:3mm;}
.note{font-size:11pt;color:#666;margin-top:3mm;line-height:1.6;
  font-family:"Microsoft YaHei",sans-serif;}
.pe{display:flex;align-items:center;gap:5mm;flex-wrap:wrap;margin-bottom:2mm;}
.peop{font-size:22pt;color:#666;padding:0 3mm;font-weight:700;}
.del{text-decoration:line-through;color:#bbb;font-size:23pt;letter-spacing:2mm;}
.vert{font-family:"Times New Roman",serif;font-size:22pt;display:inline-block;
  border-bottom:2px solid var(--ink);padding:0 4mm 1mm 6mm;margin:1mm 0;}
.vert .vrow{display:flex;justify-content:flex-end;gap:3mm;line-height:1.3;}
.vert .vline{border-top:2px solid var(--ink);margin:0 -4mm 0 -6mm;}
.vert .vop{width:2.5em;text-align:center;}
.vert .vph{display:inline-block;width:1.5em;}
.crow{display:flex;flex-wrap:wrap;gap:3mm;margin-top:2mm;}
.cbox{display:inline-block;width:8mm;height:8mm;border:1.5px solid var(--line);border-radius:50%;}
@media print{
  body{background:#fff;}
  .no-print{display:none;}
  .sheet{box-shadow:none;margin:0;width:auto;min-height:0;height:265mm;}
  @page{size:A4 portrait;margin:10mm;}
}
"""


def render_html(qs, title, subtitle, per_page, with_answers, cols=2, name=""):
    pages = [qs[i:i + per_page] for i in range(0, len(qs), per_page)] or [[]]
    total_pages = len(pages) + (1 if with_answers else 0)
    out = []
    for pi, page in enumerate(pages):
        cells = []
        for q in page:
            lvtag = f'<span class="lvtag">{q["level"]}</span>' if len({x["level"] for x in qs}) > 1 else ""
            cells.append(f'<div class="q"><span class="no">{q["no"]}.</span>{lvtag}{q["prompt"]}</div>')
        out.append(
            f'<section class="sheet">'
            f'<div class="head"><div class="title">{title}</div>'
            f'<div class="sub">{subtitle}</div>'
            f'<div class="meta">姓名：<span>{name}</span>日期：<span></span>用时：<span></span>'
            f'做对：<span style="min-width:16mm"></span>题</div></div>'
            f'<div class="grid" style="grid-template-columns:repeat({cols},1fr)">{"".join(cells)}</div>'
            f'<div class="foot"><span>幼儿园数学练习 · {title}</span>'
            f"<span>第 {pi + 1} 页 / 共 {total_pages} 页</span></div>"
            f"</section>"
        )
    if with_answers:
        items = "".join(
            f'<div>{q["no"]}. {q["answer"]}'
            f'<span class="atopic">{TOPIC_LABEL.get(q["topic"], "")}</span></div>'
            for q in qs
        )
        out.append(
            '<section class="sheet answers">'
            '<div class="head"><div class="title">参考答案（家长用）</div>'
            f'<div class="sub">{title} · 共 {len(qs)} 题</div></div>'
            f'<div class="alist">{items}</div>'
            '<div class="note">建议孩子全部完成后再对照。'
            '错题请先让孩子说"你是怎么想的"，再针对性讲一个点，不要当场连讲三遍。'
            '书写题看笔顺与占格，不追求工整。</div>'
            f'<div class="foot"><span>参考答案</span><span>第 {total_pages} 页 / 共 {total_pages} 页</span></div>'
            "</section>"
        )
    html = (
        '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">'
        f"<title>{title}</title><style>{CSS}</style></head><body>"
        '<div class="no-print"><button onclick="window.print()">🖨 打印 / 另存为 PDF</button>'
        "　<span style=\"font-size:12px;color:#888\">打印设置：A4 纵向、边距默认、勾选「背景图形」</span></div>"
        + "".join(out)
        + "</body></html>"
    )
    return html


# ---------------------------------------------------------------- 主流程
def main():
    ap = argparse.ArgumentParser(description="幼儿园数学练习页生成器")
    ap.add_argument("--level", choices=["L1", "L2", "L3", "L4", "L5"], default="L4")
    ap.add_argument("--preset", choices=["diagnostic"], help="预设卷种：diagnostic=10 题诊断卷")
    ap.add_argument("--topics", help="逗号分隔的题型，默认按等级自动配置")
    ap.add_argument("--count", type=int, default=20, help="题目数量，默认 20")
    ap.add_argument("--per-page", type=int, help="每页题数，默认按等级自动配置")
    ap.add_argument("--columns", type=int, default=2, choices=[1, 2, 3], help="每页列数，默认 2")
    ap.add_argument("--seed", type=int, help="随机种子，相同种子生成相同题目")
    ap.add_argument("--title", help="练习页标题")
    ap.add_argument("--name", default="", help="页眉预填的孩子姓名")
    ap.add_argument("--review", help="错题重练：上次练习的 JSON 路径")
    ap.add_argument("--wrong", help="错题题号，逗号分隔（如 3,7,12），配合 --review 使用")
    ap.add_argument("--no-answers", action="store_true", help="不生成答案页")
    ap.add_argument("--out", required=True, help="输出 HTML 路径")
    ap.add_argument("--json", dest="json_out", help="同时输出题目与答案的 JSON，供批改使用")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    seed = args.seed if args.seed is not None else random.randint(1, 10**6)
    rng = random.Random(seed)

    if args.preset == "diagnostic":
        qs = build_diagnostic(rng)
        level = "诊断"
        title = args.title or "幼儿数学能力诊断卷"
        subtitle = "L1-L5 各 2 题，共 10 题 · 从最低未掌握等级开始练"
        per_page = args.per_page or 10
    elif args.review:
        level, qs, title, subtitle, per_page = build_review(args, rng)
    else:
        level = args.level
        topics = [t.strip() for t in args.topics.split(",")] if args.topics else LEVEL_TOPICS[level]
        bad = [t for t in topics if t not in GENERATORS]
        if bad:
            sys.exit(f"未知题型: {bad}；可用题型: {list(GENERATORS)}")
        qs = build_questions(level, topics, args.count, rng)
        title = args.title or f"幼儿园数学练习 · {level} {LEVEL_NAME[level]}"
        labels = "、".join(TOPIC_LABEL[t] for t in topics)
        subtitle = f"{LEVEL_NAME[level]} · 题型：{labels} · 共 {len(qs)} 题 · 建议 10-15 分钟"
        per_page = args.per_page or PER_PAGE[level]

    html = render_html(
        qs, title, subtitle, per_page, not args.no_answers, args.columns, args.name
    )
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

    if args.json_out:
        Path(args.json_out).write_text(
            json.dumps(
                {
                    "seed": seed,
                    "level": level,
                    "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "questions": [
                        {"no": q["no"], "topic": q["topic"], "level": q["level"], "answer": q["answer"]}
                        for q in qs
                    ],
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    print(f"已生成：{out_path.resolve()}")
    print(f"等级：{level}　题数：{len(qs)}　种子：{seed}　答案页：{'否' if args.no_answers else '是'}")
    if args.json_out:
        print(f"题目数据：{Path(args.json_out).resolve()}")
    print("提示：在浏览器中打开后点击打印，或用 Ctrl+P 另存为 PDF。")


if __name__ == "__main__":
    main()
