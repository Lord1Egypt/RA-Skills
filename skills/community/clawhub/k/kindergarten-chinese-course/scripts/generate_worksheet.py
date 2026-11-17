#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
幼儿园识字与诗歌练习生成器 (kindergarten-chinese-course)
生成 A4 可打印 HTML 练习页 + 答案 JSON。

TRACE-E 合规（skillhub 评估红线，与 kindergarten-thinking-course 对齐）：
  T (Trusted/零外网)   仅用 Python 标准库；无 requests/urllib/socket/http 调用
  R (Restricted/零凭证) 不读 ~/.ssh / .env / AppData / token / 浏览器缓存 / 系统目录
  A (Anti-inject/零注入) 姓名等不信任输入统一 html.escape
  C (Contained/最小权限) 文件写入仅在 --out / --json 指定路径内
  E (Evidence/可审计)    所有随机由 seed 控制，JSON 写入 seed，--regen 字节级复现
发布前自检：python scripts/preflight.py

用法见 references/activity-spec.md
"""
import argparse
import html
import json
import random
import sys

# ---------------------------------------------------------------------------
# 数据：汉字（按难度排序，等级从前往后截取）
# 每项: (汉字, emoji, 词义标签)
# ---------------------------------------------------------------------------
CHARS = [
    ("日", "☀️", "太阳"), ("月", "🌙", "月亮"), ("水", "💧", "水"),
    ("火", "🔥", "火苗"), ("山", "⛰️", "高山"), ("石", "🪨", "石头"),
    ("田", "🌾", "田地"), ("土", "🌱", "泥土"), ("人", "🧍", "小人"),
    ("口", "👄", "嘴巴"), ("手", "✋", "小手"), ("目", "👀", "眼睛"),
    ("木", "🌳", "大树"), ("花", "🌸", "花朵"), ("鸟", "🐦", "小鸟"),
    ("鱼", "🐟", "小鱼"), ("牛", "🐮", "黄牛"), ("羊", "🐑", "绵羊"),
    ("马", "🐴", "马儿"), ("车", "🚗", "汽车"), ("上", "⬆️", "上面"),
    ("下", "⬇️", "下面"), ("大", "🔺", "大"), ("小", "🔻", "小"),
    ("出", "🚪", "出去"), ("入", "↘️", "进入"), ("来", "➡️", "过来"),
    ("去", "⬅️", "走去"), ("风", "🌬️", "风"), ("云", "☁️", "云"),
    ("雨", "🌧️", "雨"), ("雪", "❄️", "雪"), ("天", "🌌", "天空"),
    ("地", "🌍", "大地"), ("中", "🎯", "中间"), ("心", "❤️", "心"),
    ("书", "📖", "书"), ("笔", "🖊️", "笔"), ("明", "💡", "明亮"),
    ("亮", "✨", "亮"), ("红", "🌹", "红色"), ("绿", "🍀", "绿色"),
]

# 各等级截取的汉字数量（累计）
LEVEL_CHARS = {"L1": 12, "L2": 24, "L3": 36, "L4": len(CHARS)}

# 各等级默认汉字题量
DEFAULT_COUNT = {"L1": 8, "L2": 10, "L3": 12, "L4": 12}

# ---------------------------------------------------------------------------
# 数据：诗歌（按等级分组，已带拼音）
# 结构: {"title","author","dynasty","lines":[(原文, 拼音), ...]}
# ---------------------------------------------------------------------------
POEMS = {
    "L1": [
        {"title": "两只老虎", "author": "民间儿歌", "dynasty": "",
         "lines": [("两只老虎，两只老虎，", "liǎng zhī lǎo hǔ liǎng zhī lǎo hǔ"),
                   ("跑得快，跑得快，", "pǎo de kuài pǎo de kuài"),
                   ("一只没有耳朵，", "yī zhī méi yǒu ěr duǒ"),
                   ("一只没有尾巴，", "yī zhī méi yǒu wěi ba"),
                   ("真奇怪，真奇怪。", "zhēn qí guài zhēn qí guài")]},
        {"title": "找朋友", "author": "民间儿歌", "dynasty": "",
         "lines": [("找呀找呀找朋友，", "zhǎo ya zhǎo ya zhǎo péng yǒu"),
                   ("找到一个好朋友，", "zhǎo dào yī gè hǎo péng yǒu"),
                   ("敬个礼，握握手，", "jìng gè lǐ wò wò shǒu"),
                   ("你是我的好朋友。", "nǐ shì wǒ de hǎo péng yǒu")]},
        {"title": "小星星", "author": "中文儿歌", "dynasty": "",
         "lines": [("一闪一闪亮晶晶，", "yī shǎn yī shǎn liàng jīng jīng"),
                   ("满天都是小星星。", "mǎn tiān dōu shì xiǎo xīng xīng"),
                   ("挂在天上放光明，", "guà zài tiān shàng fàng guāng míng"),
                   ("好像许多小眼睛。", "hǎo xiàng xǔ duō xiǎo yǎn jīng")]},
    ],
    "L2": [
        {"title": "咏鹅", "author": "骆宾王", "dynasty": "唐",
         "lines": [("鹅，鹅，鹅，", "é é é"),
                   ("曲项向天歌。", "qū xiàng xiàng tiān gē"),
                   ("白毛浮绿水，", "bái máo fú lǜ shuǐ"),
                   ("红掌拨清波。", "hóng zhǎng bō qīng bō")]},
        {"title": "静夜思", "author": "李白", "dynasty": "唐",
         "lines": [("床前明月光，", "chuáng qián míng yuè guāng"),
                   ("疑是地上霜。", "yí shì dì shàng shuāng"),
                   ("举头望明月，", "jǔ tóu wàng míng yuè"),
                   ("低头思故乡。", "dī tóu sī gù xiāng")]},
        {"title": "春晓", "author": "孟浩然", "dynasty": "唐",
         "lines": [("春眠不觉晓，", "chūn mián bù jué xiǎo"),
                   ("处处闻啼鸟。", "chù chù wén tí niǎo"),
                   ("夜来风雨声，", "yè lái fēng yǔ shēng"),
                   ("花落知多少。", "huā luò zhī duō shǎo")]},
        {"title": "悯农", "author": "李绅", "dynasty": "唐",
         "lines": [("锄禾日当午，", "chú hé rì dāng wǔ"),
                   ("汗滴禾下土。", "hàn dī hé xià tǔ"),
                   ("谁知盘中餐，", "shéi zhī pán zhōng cān"),
                   ("粒粒皆辛苦。", "lì lì jiē xīn kǔ")]},
        {"title": "登鹳雀楼", "author": "王之涣", "dynasty": "唐",
         "lines": [("白日依山尽，", "bái rì yī shān jìn"),
                   ("黄河入海流。", "huáng hé rù hǎi liú"),
                   ("欲穷千里目，", "yù qióng qiān lǐ mù"),
                   ("更上一层楼。", "gèng shàng yī céng lóu")]},
    ],
    "L3": [
        {"title": "绝句", "author": "杜甫", "dynasty": "唐",
         "lines": [("两个黄鹂鸣翠柳，", "liǎng gè huáng lí míng cuì liǔ"),
                   ("一行白鹭上青天。", "yī háng bái lù shàng qīng tiān"),
                   ("窗含西岭千秋雪，", "chuāng hán xī lǐng qiān qiū xuě"),
                   ("门泊东吴万里船。", "mén bó dōng wú wàn lǐ chuán")]},
        {"title": "望庐山瀑布", "author": "李白", "dynasty": "唐",
         "lines": [("日照香炉生紫烟，", "rì zhào xiāng lú shēng zǐ yān"),
                   ("遥看瀑布挂前川。", "yáo kàn pú bù guà qián chuān"),
                   ("飞流直下三千尺，", "fēi liú zhí xià sān qiān chǐ"),
                   ("疑是银河落九天。", "yí shì yín hé luò jiǔ tiān")]},
        {"title": "早发白帝城", "author": "李白", "dynasty": "唐",
         "lines": [("朝辞白帝彩云间，", "zhāo cí bái dì cǎi yún jiān"),
                   ("千里江陵一日还。", "qiān lǐ jiāng líng yī rì huán"),
                   ("两岸猿声啼不住，", "liǎng àn yuán shēng tí bú zhù"),
                   ("轻舟已过万重山。", "qīng zhōu yǐ guò wàn chóng shān")]},
    ],
    "L4": [
        {"title": "山行", "author": "杜牧", "dynasty": "唐",
         "lines": [("远上寒山石径斜，", "yuǎn shàng hán shān shí jìng xié"),
                   ("白云生处有人家。", "bái yún shēng chù yǒu rén jiā"),
                   ("停车坐爱枫林晚，", "tíng chē zuò ài fēng lín wǎn"),
                   ("霜叶红于二月花。", "shuāng yè hóng yú èr yuè huā")]},
        {"title": "咏柳", "author": "贺知章", "dynasty": "唐",
         "lines": [("碧玉妆成一树高，", "bì yù zhuāng chéng yī shù gāo"),
                   ("万条垂下绿丝绦。", "wàn tiáo chuí xià lǜ sī tāo"),
                   ("不知细叶谁裁出，", "bù zhī xì yè shéi cái chū"),
                   ("二月春风似剪刀。", "èr yuè chūn fēng sì jiǎn dāo")]},
    ],
}

# 等级 → 适用题型
LEVEL_TOPICS = {
    "L1": ["recognize", "trace", "poem"],
    "L2": ["recognize", "trace", "poem"],
    "L3": ["recognize", "trace", "poem", "word"],
    "L4": ["recognize", "trace", "poem", "word", "fill"],
}
ALL_TOPICS = ["recognize", "trace", "poem", "word", "fill"]
TOPIC_CN = {
    "recognize": "看图认字", "trace": "描红", "poem": "古诗/儿歌",
    "word": "组词", "fill": "古诗填空",
}
TOPIC_EN = {
    "recognize": "Recognize", "trace": "Trace", "poem": "Poem",
    "word": "Word", "fill": "Fill-in",
}

LEVEL_AGE = {
    "L1": "小班 3-4 岁", "L2": "中班 4-5 岁", "L3": "大班 5-6 岁",
    "L4": "幼小衔接 6-7 岁",
}

# ---------------------------------------------------------------------------
# 提示文案
# ---------------------------------------------------------------------------
TIPS = {
    "zh": {
        "recognize": "先指图说名字，再点汉字念出来，把「图画」和「汉字」连起来，不要求会写。",
        "trace": "握笔姿势比写对更重要，沿灰色字轻轻描，写完夸一句「这一笔真稳」。",
        "poem": "跟着拼音读两遍，再拍手打节奏念；会背就打勾，别急着默写。",
        "word": "引导用这个字组一个词（如「日」→ 日月），写不出的字可用拼音代替。",
        "fill": "先熟读全诗，再遮住空格凭记忆填，填完对照答案页改一改。",
    },
    "en": {
        "recognize": "Point to the picture and say its name, then read the character aloud. Link picture to character; no writing needed.",
        "trace": "Pencil grip matters more than correctness. Trace the light-gray character; praise steady strokes.",
        "poem": "Read with pinyin twice, then clap the rhythm. Tick when recited; no dictation yet.",
        "word": "Help form a word with the character (e.g. 日→日月). Pinyin is fine if a字 is hard to write.",
        "fill": "Recite the poem first, then fill blanks from memory; check against the answer page.",
    },
}


# ---------------------------------------------------------------------------
# 构建各版块 HTML
# ---------------------------------------------------------------------------
def esc(s):
    return html.escape(str(s), quote=True)


def build_recognize(chars, lang, columns):
    title = "一、看图认汉字" if lang == "zh" else "1. Look & Read"
    cells = []
    for ch, em, label in chars:
        cells.append(
            f'<div class="cell"><div class="emoji">{em}</div>'
            f'<div class="name">{esc(label)}</div>'
            f'<div class="hanzi">{esc(ch)}</div></div>'
        )
    return (f'<h2>{title}</h2>'
            f'<div class="grid" style="grid-template-columns:repeat({columns},1fr)">'
            + "".join(cells) + '</div>')


def build_trace(chars, lang, columns):
    title = "二、我会描一描（沿着灰色字写一写）" if lang == "zh" else "2. Trace the Characters"
    cells = []
    for ch, _em, _label in chars:
        cells.append(
            f'<div class="trace"><span class="corner">{esc(ch)}</span>'
            f'<span class="t">{esc(ch)}</span></div>'
        )
    return (f'<h2>{title}</h2>'
            f'<div class="trace-grid" style="grid-template-columns:repeat({columns},1fr)">'
            + "".join(cells) + '</div>')


def build_word(chars, lang, columns):
    title = "三、我会组词（用这个字说/写一个词）" if lang == "zh" else "3. Make a Word"
    rows = []
    for ch, _em, _label in chars:
        rows.append(
            f'<div class="word-row"><span class="wchar">{esc(ch)}</span>'
            f'<span class="wline">{"＿"*8}</span>'
            f'<span class="whint">{"（写一写）" if lang=="zh" else "(write)"}</span></div>'
        )
    return f'<h2>{title}</h2><div class="word-list">' + "".join(rows) + '</div>'


def build_poem(poem, lang, fill=False):
    head = "学古诗" if lang == "zh" else "Poem"
    dynasty = f"（{poem['dynasty']}）" if poem["dynasty"] else ""
    author = f"{poem['author']}" if poem["author"] else ""
    sub = f"{head}《{esc(poem['title'])}》　{dynasty}{esc(author)}" if lang == "zh" \
        else f"{head}: {esc(poem['title'])} — {esc(author)} {dynasty}"
    lines_html = []
    for i, (text, py) in enumerate(poem["lines"]):
        if fill:
            display = blank_line(text)
            lines_html.append(
                f'<div class="line"><span class="py">{esc(py)}</span>{esc(display)}</div>')
        else:
            lines_html.append(
                f'<div class="line"><span class="py">{esc(py)}</span>{esc(text)}</div>')
    recite = ('读给爸爸妈妈听一听：<span class="box"></span> 我会背啦！'
              if lang == "zh" else
              'Recite to parents: <span class="box"></span> I can recite it!')
    return (f'<div class="poem"><div class="title">{sub}</div>'
            + "".join(lines_html)
            + f'</div><div class="recite">{recite}</div>')


def blank_line(text):
    """填空：每行保留首尾，挖掉一个非标点汉字。"""
    chars = list(text)
    cand = [i for i, c in enumerate(chars)
            if c not in "，。、！？；：" and 0 < i < len(chars) - 1]
    if cand:
        idx = cand[len(cand) // 2]
        chars[idx] = "＿＿"
    return "".join(chars)


def build_tips(topics, lang):
    title = "家长小提示" if lang == "zh" else "Tips for Parents"
    items = []
    for t in topics:
        tip = TIPS[lang].get(t, "")
        if tip:
            label = TOPIC_CN.get(t, t) if lang == "zh" else TOPIC_EN.get(t, t)
            items.append(f"<b>{esc(label)}：</b>{esc(tip)}")
    body = "<br>".join(items) if items else "陪伴完成，多鼓励，不计时。"
    return f'<h2>{title}</h2><div class="tips">{body}</div>'


def build_answer_section(level, lang, topics, chars, poems):
    """内嵌答案页（与题目同一份 HTML，打印时另起一页）。"""
    parts = []
    head = "参考答案" if lang == "zh" else "Answer Key"
    if set(topics) & {"recognize", "trace", "word"}:
        cells = []
        for ch, em, label in chars:
            cells.append(f'<div class="cell"><div class="emoji">{em}</div>'
                         f'<div class="name">{esc(label)}</div>'
                         f'<div class="hanzi">{esc(ch)}</div></div>')
        parts.append(f'<h2>{"汉字" if lang=="zh" else "Characters"}</h2>'
                     f'<div class="grid" style="grid-template-columns:repeat(4,1fr)">'
                     + "".join(cells) + '</div>')
    if "word" in topics:
        rows = []
        for ch, _em, _label in chars:
            rows.append(f'<div class="word-row"><span class="wchar">{esc(ch)}</span>'
                        f'<span class="whint">{esc(ch)}{esc(ch)}（示例）</span></div>')
        parts.append(f'<h2>{"组词参考" if lang=="zh" else "Word hints"}</h2>'
                     f'<div class="word-list">{"".join(rows)}</div>')
    if set(topics) & {"poem", "fill"}:
        plines = []
        for p in poems:
            lines = "".join(f'<div class="line">{esc(t)}</div>' for t, _ in p["lines"])
            dynasty = f"（{p['dynasty']}）" if p["dynasty"] else ""
            plines.append(f'<div class="poem"><div class="title">'
                          f'《{esc(p["title"])}》{dynasty}{esc(p["author"])}</div>{lines}</div>')
        parts.append(f'<h2>{"古诗全文" if lang=="zh" else "Poems"}</h2>' + "".join(plines))
    if not parts:
        return ""
    return f'<div class="ans"><h1 class="ans-h">{head}</h1>' + "".join(parts) + '</div>'


# ---------------------------------------------------------------------------
# 渲染整页
# ---------------------------------------------------------------------------
CSS = """
:root{--ink:#2b2b2b;--soft:#dcdcdc;--line:#cfd8dc;--brand:#ff8fab;--blue:#cfe8ff;}
*{box-sizing:border-box;}
body{font-family:"Microsoft YaHei","PingFang SC","Hiragino Sans GB",sans-serif;color:var(--ink);margin:0;padding:72px 24px 24px;background:#fff;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
.sheet{max-width:780px;margin:0 auto;}
header{border-bottom:4px solid var(--brand);padding-bottom:10px;margin-bottom:18px;}
h1{font-size:26px;margin:0 0 6px;color:var(--brand);letter-spacing:2px;}
.meta{font-size:15px;color:#555;}
.meta .line{display:inline-block;min-width:150px;margin-right:24px;border-bottom:1px solid var(--line);padding:2px 4px;}
h2{font-size:20px;margin:26px 0 12px;color:#3a6ea5;display:flex;align-items:center;gap:8px;}
h2::before{content:"";width:14px;height:14px;border-radius:50%;background:var(--brand);display:inline-block;}
.grid{display:grid;gap:12px;}
.cell{border:2px dashed var(--line);border-radius:14px;background:#fff;text-align:center;padding:10px 4px;break-inside:avoid;}
.cell .emoji{font-size:30px;line-height:1;}
.cell .name{font-size:13px;color:#888;margin-top:2px;}
.cell .hanzi{font-size:46px;line-height:1.1;margin-top:2px;font-weight:700;}
.trace-grid{display:grid;gap:10px;margin-top:6px;}
.trace{border:2px solid var(--line);border-radius:12px;background:#fff;height:120px;display:flex;align-items:center;justify-content:center;position:relative;break-inside:avoid;}
.trace .t{font-size:72px;color:var(--soft);font-weight:700;user-select:none;}
.trace .corner{position:absolute;top:4px;left:6px;font-size:12px;color:#bbb;}
.word-list{margin-top:6px;}
.word-row{display:flex;align-items:center;gap:14px;padding:10px 4px;border-bottom:1px dashed var(--line);break-inside:avoid;}
.wchar{font-size:40px;font-weight:700;min-width:48px;text-align:center;}
.wline{font-size:28px;color:#bbb;letter-spacing:2px;flex:1;}
.whint{font-size:14px;color:#999;}
.poem{border:2px solid var(--blue);border-radius:16px;background:#f7fbff;padding:18px 22px;line-height:2.1;font-size:24px;text-align:center;break-inside:avoid;}
.poem .line{margin:6px 0;}
.poem .py{font-size:14px;color:#7aa7d6;display:block;letter-spacing:1px;}
.poem .title{font-size:18px;color:#3a6ea5;margin-bottom:10px;font-weight:700;}
.recite{margin-top:14px;font-size:16px;color:#555;}
.recite .box{display:inline-block;width:18px;height:18px;border:2px solid #999;border-radius:4px;vertical-align:-3px;margin:0 4px;}
.tips{border-left:5px solid #fff3c4;background:#fffdf3;padding:12px 16px;border-radius:0 12px 12px 0;font-size:14px;color:#666;line-height:1.9;}
.tips b{color:#b8860b;}
.score{border:2px solid var(--line);border-radius:12px;padding:12px 16px;margin-top:20px;font-size:15px;color:#555;display:flex;gap:24px;flex-wrap:wrap;}
.score .sline{min-width:120px;border-bottom:1px solid var(--line);}
.footer{margin-top:22px;text-align:center;color:#aaa;font-size:12px;}
.ans{page-break-before:always;margin-top:10px;}
.ans-h{font-size:24px;color:var(--brand);margin:0 0 12px;}
.print-bar{position:fixed;top:0;left:0;right:0;z-index:1000;background:#f8f9fa;border-bottom:1px solid #ddd;padding:8px 16px;display:flex;align-items:center;justify-content:center;gap:16px;box-shadow:0 2px 6px rgba(0,0,0,.08);}
.print-bar button{background:#3a6ea5;color:#fff;border:0;border-radius:8px;padding:8px 16px;font-size:15px;cursor:pointer;display:flex;align-items:center;gap:6px;}
.print-bar button:hover{background:#2e5980;}
.print-bar .hint{font-size:13px;color:#666;}
.print-bar .hint b{color:#333;}
@media print{body{padding:0;}.sheet{max-width:100%;}.cell,.trace,.poem,.word-row{page-break-inside:avoid;}.ans{page-break-before:always;}.print-bar{display:none;}}
@page{size:A4;margin:14mm;}
"""

PAGE = """<!DOCTYPE html>
<html lang="{lang}">
<head><meta charset="UTF-8"><title>{title}</title><style>{css}</style></head>
<body>
<div class="print-bar no-print">
  <button type="button" onclick="window.print()">🖨️ {print_btn}</button>
  <span class="hint">{print_hint}</span>
</div>
<div class="sheet">
<header><h1>{h1}</h1>
<div class="meta"><span class="line">{name_label}{name}</span><span class="line">{date_label}__________</span></div>
</header>
{body}
{answer}
{score}
<div class="footer">{footer}</div>
</div></body></html>"""


def render(level, lang, name, topics, chars, poems, columns, with_score, with_answers, seed):
    h1 = "🌟 幼儿识字与诗歌练习" if lang == "zh" else "🌟 Chinese Characters & Poems"
    body_parts = []
    order = ["recognize", "trace", "word", "poem", "fill"]
    for t in order:
        if t not in topics:
            continue
        if t == "recognize":
            body_parts.append(build_recognize(chars, lang, columns))
        elif t == "trace":
            body_parts.append(build_trace(chars, lang, columns))
        elif t == "word":
            body_parts.append(build_word(chars, lang, columns))
        elif t == "poem":
            for p in poems:
                body_parts.append(build_poem(p, lang, fill=False))
        elif t == "fill":
            for p in poems:
                body_parts.append(build_poem(p, lang, fill=True))
    body_parts.append(build_tips(topics, lang))
    body = "".join(body_parts)
    answer_html = build_answer_section(level, lang, topics, chars, poems) if with_answers else ""
    score_html = ""
    if with_score:
        score_html = ('<div class="score"><span class="sline">得分：______</span>'
                      '<span class="sline">正确数：______</span>'
                      '<span class="sline">日期：______</span>'
                      '<span class="sline">评语：______</span></div>')
    if lang == "zh":
        print_btn = "打印 / 另存为 PDF"
        print_hint = '打印设置：<b>A4 纵向</b>，页边距：<b>无</b>，页眉页脚：<b>无</b>，背景图形：<b>✓</b>'
        name_label, date_label = "姓名：", "日期："
        footer = "快乐识字 · 一天认几个，慢慢来 🌈"
    else:
        print_btn = "Print / Save as PDF"
        print_hint = 'Print settings: <b>A4 portrait</b>, margins <b>none</b>, headers/footers <b>none</b>, background graphics <b>✓</b>'
        name_label, date_label = "Name: ", "Date: "
        footer = "Happy learning · a few characters a day 🌈"
    return PAGE.format(lang=lang, css=CSS, title=h1, h1=h1,
                       print_btn=print_btn, print_hint=print_hint,
                       name_label=name_label, date_label=date_label,
                       name=esc(name), body=body, answer=answer_html,
                       score=score_html, footer=footer)


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
def pick(level, topics, count, rng):
    n_chars = LEVEL_CHARS[level]
    pool = CHARS[:n_chars]
    hanzi_topics = [t for t in topics if t in ("recognize", "trace", "word")]
    poem_topics = [t for t in topics if t in ("poem", "fill")]

    if hanzi_topics:
        k = count if count > 0 else DEFAULT_COUNT[level]
        k = min(k, len(pool))
        chars = pool[:k]  # 保持原顺序更利于教学
    else:
        chars = []

    if poem_topics:
        ppool = POEMS.get(level, [])
        if count > 0 and not hanzi_topics:
            kp = min(count, len(ppool))
        else:
            kp = 1
        poems = rng.sample(ppool, kp) if kp <= len(ppool) and ppool else ppool[:kp]
    else:
        poems = []
    return chars, poems


def main():
    ap = argparse.ArgumentParser(description="幼儿识字与诗歌练习生成器")
    ap.add_argument("--level", default="L1", choices=["L1", "L2", "L3", "L4"])
    ap.add_argument("--count", type=int, default=0, help="汉字题量；仅诗歌时表示诗歌数量(上限3)")
    ap.add_argument("--topics", default="", help="recognize,trace,poem,word,fill")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--name", default="")
    ap.add_argument("--no-name", action="store_true")
    ap.add_argument("--columns", type=int, default=4, choices=[1, 2, 3, 4, 5, 6])
    ap.add_argument("--no-answers", action="store_true", help="不内嵌答案页")
    ap.add_argument("--lang", default="zh", choices=["zh", "en"])
    ap.add_argument("--score", action="store_true")
    ap.add_argument("--out", default="")
    ap.add_argument("--json", default="")
    ap.add_argument("--regen", default=None, help="从旧 JSON 复现原套题")
    ap.add_argument("--list", action="store_true", help="列出题型×等级映射后退出")
    args = ap.parse_args()

    if args.list:
        print("== 可用题型 × 等级 ==")
        print(f"{'topic':10} " + "  ".join(f"{lv:4}" for lv in ["L1", "L2", "L3", "L4"]) + "  简介")
        intro = {"recognize": "看图认字", "trace": "描红", "poem": "古诗/儿歌", "word": "组词", "fill": "古诗填空"}
        for t in ALL_TOPICS:
            row = "".join(f"{'✓' if t in LEVEL_TOPICS[lv] else '·':4}" for lv in ["L1", "L2", "L3", "L4"])
            print(f"{t:10} {row}  {intro[t]}")
        print("\n== 各等级诗歌池 ==")
        for lv in ["L1", "L2", "L3", "L4"]:
            print(f"{lv}: " + "、".join(p["title"] for p in POEMS[lv]))
        return

    if not args.out or not args.json:
        print("错误：--out 与 --json 为必填（--list 除外）", file=sys.stderr)
        sys.exit(2)

    # --regen
    if args.regen:
        with open(args.regen, "r", encoding="utf-8") as f:
            old = json.load(f)
        args.level = old.get("level", args.level)
        args.seed = old.get("seed", args.seed)
        args.lang = old.get("lang", args.lang)
        if not args.no_name:
            args.name = old.get("name", args.name)
        args.topics = ",".join(old.get("topics", [])) or args.topics
        args.count = old.get("count", args.count)
        args.score = old.get("score", args.score)
        args.columns = old.get("columns", args.columns)
        args.no_answers = old.get("no_answers", args.no_answers)

    seed = args.seed if args.seed is not None else random.randint(1, 999999)
    rng = random.Random(seed)

    if args.topics:
        wanted = [t.strip() for t in args.topics.split(",") if t.strip()]
        invalid = [t for t in wanted if t not in ALL_TOPICS]
        if invalid:
            print(f"错误：未知题型 {invalid}；合法值：{ALL_TOPICS}", file=sys.stderr)
            sys.exit(2)
        topics = [t for t in wanted if t in LEVEL_TOPICS[args.level]]
        dropped = [t for t in wanted if t not in LEVEL_TOPICS[args.level]]
        if dropped:
            print(f"提示：{dropped} 不在 {args.level} 适用题型，已忽略", file=sys.stderr)
    else:
        topics = list(LEVEL_TOPICS[args.level])

    chars, poems = pick(args.level, topics, args.count, rng)
    name = "" if args.no_name else args.name

    html_out = render(args.level, args.lang, name, topics, chars, poems,
                      args.columns, args.score, not args.no_answers, seed)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html_out)

    meta = {
        "level": args.level,
        "level_age": LEVEL_AGE[args.level],
        "name": name,
        "lang": args.lang,
        "count": args.count,
        "seed": seed,
        "topics": topics,
        "score": args.score,
        "columns": args.columns,
        "no_answers": args.no_answers,
        "chars": [c[0] for c in chars],
        "poems": [p["title"] for p in poems],
    }
    with open(args.json, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"已生成: {args.out}" + ("（含内嵌答案页）" if not args.no_answers else "（不含答案）"))
    print(f"等级 {args.level} | 语言 {args.lang} | 题型: {','.join(topics)} | 汉字 {len(chars)} | 诗歌 {len(poems)}")
    print(f"种子: {seed}  （--seed {seed} 复现；或 --regen {args.json} 一键复现）")


if __name__ == "__main__":
    main()
