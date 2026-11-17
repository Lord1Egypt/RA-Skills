# -*- coding: utf-8 -*-
"""
html2ppt.py  —  pptx-craft 通用 HTML→PPT 管线（治本项 #11 / #8 / #12 / #1）
==================================================================================
把「已浏览器验收过的 HTML 报告」无损转成可编辑 PPT。

设计铁律（与 #11/#12「通用」要求一致）：
  · 解析器**零专属类名**——绝不匹配任何单一 HTML 的自定义 class（如 .rv/.model/.tl
    /.stages/.three/.thing/.pit/.conv/.node 等）。只认【语义标签 + 通用契约 class +
    几何/文本启发式】三层检测。
  · HTML 是一等输入（非模式违背）。结构保真：HTML 章节→对应版式，内容驱动弹性布局，
    绝不空白/截断（#8）。
  · 通用版式库沉淀：本文件即通用解析+渲染器，换一份 HTML 不再重写脚本（#12）。
  · QA Layer2：每页出 SVG + PNG，自动算填充率(<55% 标空白)，几何校验兜底（#1）。

三层检测（保证通用）：
  T1 语义元素直判：h1-h3 / table / ul / ol / figure / img
  T2 通用契约 class（可选增强，作者可加）：.head/.card/.grid/.contain/.timeline/.hero/.text
  T3 几何/文本启发兜底：相似兄弟节点→栅格；边框盒+标题→卡片；日期/编号正则→时间线/编号

用法:
  python html2ppt.py <input.html> [--out out.pptx] [--preview-dir previews] [--qa qa.json]
依赖: beautifulsoup4, lxml, python-pptx, pillow
"""
import os, sys, re, json, argparse, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pptx_flex_engine as eng
from bs4 import BeautifulSoup
from PIL import ImageFont

VW, VH = 1440, 680           # 每页虚拟画布
MARGIN = 48                  # 页面边距（虚拟px）
HEADER_H = 116               # 页眉区高度
FONT_PATH = r"C:/Windows/Fonts/msyh.ttc"   # CJK 字体（PIL 预览用）

# ---------------------------------------------------------------------------
# 通用检测工具（不依赖任何专属 class）
# ---------------------------------------------------------------------------
HEADING_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6")
DATE_RE = re.compile(r"(\d{4}\s*年|\d{1,2}\s*月|\d{1,2}[./]\d{1,2}|\d{4}[.\-/]\d{1,2})")
NUM_RE = re.compile(r"^\s*(\d{1,2}|NO\.?\s*\d+|第\s*\d)")

def txt(el):
    if el is None:
        return ""
    return el.get_text(" ", strip=True)

def direct_children(el):
    return [c for c in el.children if getattr(c, "name", None)]

def is_heading(el):
    return el is not None and el.name in HEADING_TAGS

def card_like(el):
    """通用卡片判定：block 级元素，含小标题(h3-h6/strong)且有正文。"""
    if el is None or el.name not in ("div", "section", "article", "li", "figcaption"):
        return False
    has_title = el.find(["h3", "h4", "h5", "h6"]) is not None or el.find("strong") is not None
    return has_title and len(txt(el)) > 4

def leading_date(el):
    return bool(DATE_RE.search(txt(el)[:16]))

def leading_num(el):
    # 子元素带 no/num 类且以数字开头，或自身文本以数字开头
    for sub in el.descendants:
        if getattr(sub, "name", None) and sub.get("class"):
            cls = " ".join(sub.get("class"))
            if re.search(r"\b(no|num|step)\b", cls, re.I) and NUM_RE.search(txt(sub)):
                return True
    return bool(NUM_RE.search(txt(el)))

def has_table(el):
    return el.find("table") is not None

def is_list(el):
    return el.name in ("ul", "ol") or el.find(["ul", "ol"]) is not None

# ---------------------------------------------------------------------------
# 契约 class 识别（T2，可选增强；缺省走 T1/T3）
# ---------------------------------------------------------------------------
CONTRACT = {
    "head": re.compile(r"\b(head|header|kicker|title)\b", re.I),
    "card": re.compile(r"\b(card|thing|stage|pit|node|conv|item|box)\b", re.I),
    "grid": re.compile(r"\b(grid|contain|container|row|columns|pcat|pgrid|three|stages)\b", re.I),
    "timeline": re.compile(r"\b(timeline|tl|road|history|journey)\b", re.I),
    "hero": re.compile(r"\b(hero|cover|title-page)\b", re.I),
    "text": re.compile(r"\b(text|para|sec-sub|note|callout|pitnote|legend|flow|blocker)\b", re.I),
}

def contract_of(el):
    if el is None:
        return None
    cls = " ".join(el.get("class", []) or [])
    for k, rx in CONTRACT.items():
        if rx.search(cls):
            return k
    return None

# ---------------------------------------------------------------------------
# 语义视觉映射（通用设计系统词汇 → 色/底）
#   这些词(kpi/num/highlight/tag/status/info-card/roi/mod-card)是通用词汇,
#   解析器识别后映射为语义色, 直接回应"字色/底色变化在 PPT 没复刻"的差距(#13/#14)。
# ---------------------------------------------------------------------------
SEM = {
    "green": "#2E7D6F", "gold": "#C9A84C", "blue": "#4A90D9", "red": "#C0392B",
    "amber": "#D97706", "ink": "#25211B", "muted": "#6E6558",
    "greenBg": "#E6F2EE", "blueBg": "#EAF2FB", "goldBg": "#FBF4E3", "redBg": "#FBEAE7",
}
MACCHIATO = dict(SEM)

def _cls(el):
    return " ".join(el.get("class", []) or [])

def _var_color(s):
    if s is None:
        return None
    s = s.strip()
    m = re.search(r"var\(--([a-z]+)\)", s)
    if m:
        return SEM.get(m.group(1))
    if s.startswith("#"):
        return s
    return SEM.get(s.lower())

def _inline_color(el, prop):
    st = el.get("style", "") or ""
    m = re.search(prop + r"\s*:\s*([^;]+)", st, re.I)
    if m:
        return _var_color(m.group(1))
    return None

def _class_color(el, *keys):
    cls = _cls(el).lower()
    for k in keys:
        if re.search(r"\b" + k + r"\b", cls):
            return SEM.get(k)
    return None

def _grid_cols(el):
    """从内联 style 推断列数：grid-template-columns 的 fr/值个数；flex-column → 1。"""
    st = el.get("style", "") or ""
    if "flex-direction:column" in st.replace(" ", ""):
        return 1
    m = re.search(r"grid-template-columns\s*:\s*([^;]+)", st, re.I)
    if m:
        return max(1, len([x for x in m.group(1).split() if x.strip()]))
    return 0

# ---------------------------------------------------------------------------
# 章节切分（T1：语义标签 section / header）
# ---------------------------------------------------------------------------
def parse_pages(soup):
    pages = []
    hero = soup.find("header")
    if hero:
        pages.append(("hero", hero))
    for sec in soup.find_all("section"):
        cls = " ".join(sec.get("class", []) or [])
        # 通用契约 class 也能标 hero（不只认 <header> 标签）
        if re.search(r"\b(hero|cover|title-page)\b", cls, re.I):
            pages.append(("hero", sec))
        else:
            pages.append(("section", sec))
    # 通用分页2：<div class="page">（如 index_v7_3.html 的设计系统；class="page-num" 的页码容器不算页）
    for d in soup.find_all("div", class_=re.compile(r"\bpage\b", re.I)):
        if "page-num" in _cls(d).lower():
            continue
        if d.find(HEADING_TAGS) or d.find(["table", "ul"]):
            pages.append(("section", d))
    return pages

# ---------------------------------------------------------------------------
# 抽取单页数据（通用，不读专属 class）
# ---------------------------------------------------------------------------
def extract_header(el):
    """kicker + title + sub，通用检测：第一个 h1/h2 及其前后短文本。"""
    h = el.find(HEADING_TAGS)
    if h is None:
        return {"kicker": "", "title": "", "sub": ""}
    title = txt(h)
    kicker, sub = "", ""
    prev = h.find_previous_sibling()
    if prev is not None and prev.name in ("div", "p", "span") and not is_heading(prev) and len(txt(prev)) < 40:
        kicker = txt(prev)
    nxt = h.find_next_sibling()
    if nxt is not None and nxt.name == "p" and len(txt(nxt)) < 200:
        sub = txt(nxt)
    return {"kicker": kicker, "title": title, "sub": sub}

def extract_blocks(container, skip=None):
    """把容器内的直接子节点分类为通用 block 列表。skip=需排除的页眉元素集合。"""
    skip = skip or set()
    blocks = []
    for ch in direct_children(container):
        if ch in skip:
            continue
        if ch.name in ("script", "style", "br"):
            continue
        if is_heading(ch):          # 标题不进正文（已在页眉处理）
            continue
        blocks.append(classify_block(ch))
    return [b for b in blocks if b is not None]

def get_body_container(el, skip):
    """通用定位正文容器：
    1) 忽略页码容器(page-num)，避免与正文并列时干扰下钻判定；
    2) 若正文区仅一个 block 级包裹层(且内部有多个子节点)，下钻取其子节点为正文块
       （避免把整页/整段当一张卡塌缩）。"""
    kids = [c for c in direct_children(el)
            if c not in skip and c.name not in ("script", "style", "br")
            and "page-num" not in _cls(c).lower()]
    if len(kids) == 1 and kids[0].name in ("div", "section", "article") \
            and len([c for c in direct_children(kids[0]) if c.name]) > 1:
        return kids[0]
    return el

def classify_block(el):
    if el is None:
        return None
    if el.name in ("script", "style", "br"):
        return None
    if "page-num" in _cls(el).lower():
        return None
    cls = _cls(el).lower()
    # 表格（含嵌套 table 的容器：保持 HTML 并排结构的行布局优先于整块当表）
    if el.name == "table" or has_table(el):
        # 若同时含其他非表结构子节点，则不整块当表——拆开各子元素分别分类
        non_table_kids = [c for c in direct_children(el) if c.name and c.name != "table"
                          and not has_table(c)]
        if el.name != "table" and len(non_table_kids) > 0:
            # 混合容器：返回一个 row 包含 table + 其他 block
            cells = []
            tbl = el.find("table") if el.name != "table" else el
            if tbl:
                t = parse_table(tbl)
                if t: cells.append(t)
            for c in non_table_kids:
                b = classify_block(c)
                if b: cells.append(b)
            if len(cells) > 1:
                return {"kind": "row", "cols": len(cells), "cells": cells}
            elif cells:
                return cells[0]
        kids_all = [c for c in direct_children(el.parent) if c.name] if el.parent else []
        if el.parent is not None and "grid-template-columns" in (el.parent.get("style", "") or ""):
            return parse_row(el.parent)
        return parse_table(el if el.name == "table" else el.find("table"))
    # 原生列表
    if el.name in ("ul", "ol") or (el.find(["ul", "ol"]) is not None and not card_like(el)):
        return parse_list(el if el.name in ("ul", "ol") else el.find(["ul", "ol"]))
    # 语义组件（通用词汇，非专属 class）
    if "kpi-row" in cls or (len([c for c in direct_children(el) if c.name and "kpi" in _cls(c).lower()]) >= 2):
        return parse_kpirow(el)
    if "kpi" in cls and "kpi-row" not in cls:
        return parse_kpi(el)
    if "highlight" in cls:
        return parse_highlight(el)
    if "roi-compare" in cls or "roi-box" in cls:
        return parse_roi(el)
    # 内联 grid（多列并排）→ 行布局，保留 HTML 的左右结构
    if "grid-template-columns" in (el.get("style", "") or "") and len([c for c in direct_children(el) if c.name]) >= 2:
        return parse_row(el)
    # 容器：内部多个卡片 → 栅格/时间线/编号（须在"单卡"判定之前）
    kids = [c for c in direct_children(el) if card_like(c)]
    if len(kids) >= 2:
        return parse_collection(el, kids)
    # 同类语义卡集合（info-card / mod-card 无 h3/strong，card_like 为 False，需单独识别）
    kids_all = [c for c in direct_children(el) if c.name]
    if len(kids_all) >= 2:
        if all("info-card" in _cls(c).lower() for c in kids_all):
            return parse_collection(el, kids_all)
        if all("mod-card" in _cls(c).lower() for c in kids_all):
            return parse_collection(el, kids_all)
    # 时间线 / 编号（契约 class 或语义 class 直接命中；其条目由 parse_collection 转卡）
    cc = contract_of(el)
    if cc == "timeline" or "timeline" in cls:
        return parse_timeline_phases(el)
    if cc == "numbered":
        return parse_collection(el, [c for c in direct_children(el) if c.name])
    # 单卡片（含 info-card / mod-card，由 parse_card 分支处理）
    if card_like(el) or "info-card" in cls or "mod-card" in cls:
        return parse_card(el)
    # 纯文本段落
    if el.name == "p" or (el.name in ("div", "section") and not direct_children(el)):
        t = txt(el)
        if t:
            return {"kind": "text", "text": t}
    # 文字块（含混合内容，取文本）
    t = txt(el)
    if t and len(t) > 2:
        return {"kind": "text", "text": t}
    return None

def parse_card(el):
    cls = _cls(el).lower()
    if "info-card" in cls:
        return parse_infocard(el)
    if "mod-card" in cls:
        return parse_modcard(el)
    title_el = (el.find(["h3", "h4", "h5", "h6"])
                or el.find("strong")
                or el.find(class_=re.compile(r"\b(ph-title|mod-title|title)\b", re.I)))
    title = txt(title_el) if title_el else ""
    # 正文：去掉标题后的剩余文本，按 <p>/<div> 拆成多行要点
    body_parts = []
    for p in el.find_all(["p", "div", "li"]):
        pt = txt(p)
        if pt and pt != title:
            body_parts.append(pt)
    if not body_parts:
        body_parts = [t for t in re.split(r"\n+", txt(el)) if t and t != title]
    return {"kind": "card", "title": title, "body": body_parts, "raw": el}

def parse_collection(el, kids):
    # 时间线 / 编号 / 普通栅格（T3 启发式，T2 契约可覆盖）
    c = contract_of(el)
    if c == "timeline" or (c is None and all(leading_date(k) for k in kids)):
        return {"kind": "timeline", "items": [parse_card(k) for k in kids]}
    if c == "grid" or (c is None and not all(leading_num(k) for k in kids)):
        cols = _grid_cols(el) or (len(kids) if len(kids) <= 4 else (3 if len(kids) % 3 == 0 else 2))
        return {"kind": "grid", "cols": cols, "cards": [parse_card(k) for k in kids]}
    # 编号序列
    return {"kind": "numbered", "items": [parse_card(k) for k in kids]}

def parse_table(table):
    if table is None:
        return None
    rows = []
    for tr in table.find_all("tr"):
        cells = [txt(td) for td in tr.find_all(["td", "th"])]
        if cells:
            rows.append(cells)
    if not rows:
        return None
    return {"kind": "table", "rows": rows}

def parse_list(ul):
    items = [txt(li) for li in ul.find_all("li")]
    if not items:
        return None
    return {"kind": "list", "items": items}

def parse_timeline_phases(el):
    """结构化解析 timeline：提取每个 phase 的 title / date / tags，而非泛化 card。"""
    phases = []
    for ph in el.find_all("div", class_="tl-phase"):
        title_el = (ph.find(class_=re.compile(r"\b(ph-title|phase-title)\b", re.I))
                    or ph.find(["h4", "h5", "h6", "strong"]))
        title = txt(title_el).strip() if title_el else ""
        date_el = ph.find(class_=re.compile(r"\b(tl-ph-time|date|badge)\b", re.I))
        date = txt(date_el).strip() if date_el else ""
        tags_el = ph.find(class_=re.compile(r"\b(tl-ph-tags|tags)\b", re.I))
        if tags_el:
            tags = [txt(sp).strip() for sp in tags_el.find_all(["span", "li"]) if txt(sp).strip()]
        else:
            # fallback: find any span/li directly under phase
            tags = [txt(sp).strip() for sp in ph.find_all(["span", "li"])
                    if txt(sp).strip() and sp.parent == ph or (sp.parent and 'tag' in _cls(sp.parent).lower())]
        phases.append({"title": title, "date": date, "tags": tags})
    # fallback: if no tl-phase children, treat direct kids as cards
    if not phases:
        kids = [c for c in direct_children(el) if c.name]
        return {"kind": "timeline", "items": [parse_card(k) for k in kids], "phases": []}
    return {"kind": "timeline", "phases": phases, "items": []}

# ---------------------------------------------------------------------------
# 语义组件解析（通用词汇）
# ---------------------------------------------------------------------------
def parse_kpirow(el):
    items = [parse_kpi(c) for c in direct_children(el) if c.name and "kpi" in _cls(c).lower()]
    if not items:
        items = [parse_kpi(c) for c in direct_children(el) if c.name]
    return {"kind": "kpirow", "items": items}

def parse_kpi(el):
    num_el = el.find(class_=re.compile(r"\bnum\b", re.I)) or el.find("div")
    num_txt = txt(num_el) if num_el else ""
    span = num_el.find("span") if num_el else None
    unit = txt(span) if span else ""
    num = num_txt.replace(unit, "").strip() if unit else num_txt.strip()
    lab = txt(el.find(class_=re.compile(r"\blab\b", re.I))) or ""
    color = _class_color(num_el, "green", "gold", "blue", "red") or _class_color(el, "green", "gold", "blue", "red")
    return {"kind": "kpi", "num": num, "unit": unit, "lab": lab, "color": color}

def parse_highlight(el):
    cls = _cls(el).lower()
    tone = "gold" if "light" in cls else "blue"
    return {"kind": "highlight", "tone": tone, "text": txt(el)}

def parse_infocard(el):
    title = txt(el.find(class_=re.compile(r"\btitle\b", re.I))) or ""
    items = [txt(it) for it in el.find_all(class_=re.compile(r"\bitem\b", re.I))]
    if not items:
        items = [t for t in re.split(r"\n+", txt(el)) if t and t != title]
    accent = _inline_color(el, "border-left") or _inline_color(el, "border") or _class_color(el, "red", "blue", "green")
    title_color = _inline_color(el, "color")
    return {"kind": "infocard", "title": title, "items": items, "accent": accent, "title_color": title_color}

def parse_roi(el):
    boxes = []
    for b in el.find_all(class_=re.compile(r"\broi-box\b", re.I)):
        cls = _cls(b).lower()
        tone = "red" if "red" in cls else ("green" if "green" in cls else "gold")
        title = txt(b.find(class_=re.compile(r"\broi-t\b", re.I))) or ""
        items = []
        for ri in b.find_all(class_=re.compile(r"\broi-item\b", re.I)):
            rl = txt(ri.find(class_=re.compile(r"\bri-l\b", re.I))) or ""
            rr = txt(ri.find(class_=re.compile(r"\bri-r\b", re.I))) or ""
            items.append((rl, rr))
        boxes.append({"tone": tone, "title": title, "items": items})
    if not boxes:
        boxes = [{"tone": "gold", "title": "", "items": []}]
    return {"kind": "roi", "boxes": boxes}

def parse_modcard(el):
    icon = txt(el.find(class_=re.compile(r"\bmod-icon\b", re.I))) or ""
    title = txt(el.find(class_=re.compile(r"\bmod-title\b", re.I))) or ""
    desc = txt(el.find(class_=re.compile(r"\bmod-desc\b", re.I))) or ""
    status = txt(el.find(class_=re.compile(r"\bmod-status\b", re.I))) or ""
    return {"kind": "modcard", "icon": icon, "title": title, "desc": desc, "status": status}

def parse_row(el):
    cells = []
    for c in direct_children(el):
        if c.name:
            b = classify_block(c)
            if b is not None:
                cells.append(b)
    cols = _grid_cols(el) or len(cells)
    return {"kind": "row", "cols": cols, "cells": cells}

# ---------------------------------------------------------------------------
# 渲染：把 page 数据 → Deck（调用纯原语库）
# ---------------------------------------------------------------------------
def C():
    return eng.TOK()["color"]

def build_header(deck, box, header):
    C_ = C()
    items = []
    if header["kicker"]:
        items.append({"content": header["kicker"], "fs": 13, "min_fs": 10, "color": C_["gold"], "bold": True})
    if header["title"]:
        items.append({"content": header["title"], "fs": 30, "min_fs": 20, "color": C_["ink"], "bold": True})
    if header["sub"]:
        items.append({"content": header["sub"], "fs": 13, "min_fs": 10, "color": C_["muted"]})
    eng.layout_texts(deck, items, box, pad=0, breath=eng.sp("sm"), align="left", group="head")
    eng.divider(deck, box.x, box.y + box.h, box.w, C_["gold"], thickness=3, group="head_div")  # #9 页眉分隔线

def _card_items(card):
    items = []
    if card.get("title"):
        items.append({"content": card["title"], "fs": 16, "min_fs": 12, "color": C()["ink"], "bold": True})
    for line in card.get("body", []):
        items.append({"content": line, "fs": 12, "min_fs": 9, "color": C()["muted"]})
    return items

def build_card(deck, box, card, group="body"):
    k = card.get("kind")
    if k == "infocard":
        return build_infocard(deck, box, card, group=group)
    if k == "modcard":
        return build_modcard(deck, box, card, group=group)
    C_ = C()
    deck.rect(box, C_["card"], line=(C_["border"], 1), radius=eng.TOK()["radius"]["lg"], group=group)
    eng.layout_texts(deck, _card_items(card), box, pad=eng.PAD_CARD_LG(), breath=eng.sp("sm"),
                     align="left", group=group)

def build_grid(deck, box, blk):
    cards = blk["cards"]
    cols = blk["cols"]
    rows = (len(cards) + cols - 1) // cols
    gap = eng.sp("lg")
    cw = (box.w - gap * (cols - 1)) / cols
    ch = (box.h - gap * (rows - 1)) / rows
    for i, card in enumerate(cards):
        r, c = divmod(i, cols)
        cb = eng.Box(box.x + c * (cw + gap), box.y + r * (ch + gap), cw, ch)
        build_card(deck, cb, card, group=f"g{i}")

def _weighted_heights(items, avail_h, gap, card_w):
    """按各卡自然高度占比分配 avail_h，且每卡不低于其自然高度权重。
    自然总高 ≤ avail_h 时按比例放大；> avail_h 时按比例压缩（layout_texts 会缩字号兜底）。"""
    nat = [max(MIN_CARD_H, _card_natural(c, card_w)) for c in items]
    usable = avail_h - gap * (len(items) - 1)
    total = sum(nat)
    if total <= 0:
        return [usable / len(items)] * len(items)
    return [h * usable / total for h in nat]

def build_timeline(deck, box, blk):
    """渲染时间线：2-4 个 phase 时横向排列（匹配 HTML 的三阶段卡片布局）；
    更多 phase 时回退到竖向列表。"""
    phases = blk.get("phases", [])
    items = blk.get("items", [])
    C_ = C()

    # 新结构化数据：横向阶段卡片
    if phases and 2 <= len(phases) <= 4:
        n = len(phases)
        gap = eng.sp("md")
        cw = (box.w - gap * (n - 1)) / n
        for i, ph in enumerate(phases):
            cx = box.x + i * (cw + gap)
            cb = eng.Box(cx, box.y, cw, box.h)
            # 阶段标题栏（带彩色顶边）
            tone_colors = ["#2E7D6F", "#1565C0", "#C9A84C", "#C62828"]
            fg = SEM.get(tone_colors[i % len(tone_colors)], tone_colors[i % len(tone_colors)])
            # 标题
            if ph.get("title"):
                deck.rect(eng.Box(cb.x, cb.y, cb.w, 28), "F8F9FB",
                          line=(fg, 0), radius=eng.TOK()["radius"]["sm"], group=f"tl{i}")
                eng.layout_texts(deck, [{"content": ph["title"], "fs": 13, "min_fs": 11,
                                       "color": fg, "bold": True}],
                                 eng.Box(cb.x + 10, cb.y + 2, cb.w - 20, 24),
                                 pad=0, breath=0, align="left", group=f"tl{i}")
            # 日期 badge
            dy = cb.y + (32 if ph.get("title") else 4)
            if ph.get("date"):
                deck.rect(eng.Box(cb.x + 10, dy, len(ph["date"]) * 7 + 12, 20),
                          SEM.get("greenBg", "#E8F5E9"), radius=4, group=f"tl{i}")
                eng.layout_texts(deck, [{"content": ph["date"], "fs": 10, "min_fs": 9,
                                       "color": SEM.get("green", "#2E7D6F"), "bold": True}],
                                 eng.Box(cb.x + 16, dy + 2, cb.w - 20, 18),
                                 pad=0, breath=0, align="left", group=f"tl{i}")
                dy += 24
            # Tags 行
            if ph.get("tags"):
                tag_txt = "  ".join(ph["tags"])
                eng.layout_texts(deck, [{"content": tag_txt, "fs": 9, "min_fs": 8,
                                       "color": C_["muted"]}],
                                 eng.Box(cb.x + 10, dy, cb.w - 20, max(16, box.h - (dy - cb.y) - 8)),
                                 pad=0, breath=2, align="left", group=f"tl{i}")
        return

    # 回退：竖向列表（旧逻辑，兼容 items 格式）
    if not phases and items:
        gap = eng.sp("md")
        hs = _weighted_heights(items, box.h, gap, box.w - 110)
        y = box.y
        for i, card in enumerate(items):
            ch = hs[i]
            date_txt = ""
            m = DATE_RE.search(txt(card.get("raw", ""))[:16])
            if m:
                date_txt = m.group(1)
            marker = eng.Box(box.x, y, 96, min(ch, 24))
            if date_txt:
                deck.text(marker, date_txt, 12, C_["blue"], bold=True, align="left", group="tl")
            cb = eng.Box(box.x + 110, y, box.w - 110, ch)
            build_card(deck, cb, card, group=f"tl{i}")
            y += ch + gap

def build_numbered(deck, box, blk):
    items = blk["items"]
    gap = eng.sp("md")
    hs = _weighted_heights(items, box.h, gap, box.w - 40)
    y = box.y
    for i, card in enumerate(items):
        ch = hs[i]
        cb = eng.Box(box.x + 40, y, box.w - 40, ch)
        # 编号徽标
        deck.text(eng.Box(box.x, y, 32, min(ch, 26)), f"{i+1:02d}", 18, C()["gold"], bold=True, align="left", group="no")
        build_card(deck, cb, card, group=f"no{i}")
        y += ch + gap

def build_table(deck, box, blk):
    rows = blk["rows"]
    n = len(rows)
    gap = eng.sp("xs")
    rh = (box.h - gap * (n - 1)) / n
    C_ = C()
    for ri, row in enumerate(rows):
        y = box.y + ri * (rh + gap)
        is_head = ri == 0
        fill = C_["goldSoft"] if is_head else (C_["card"] if ri % 2 else "F8F9FB")
        # 简单按列均分（最多取最大列数）
        ncol = max(len(r) for r in rows)
        cw = box.w / ncol
        for ci, cell in enumerate(row):
            cb = eng.Box(box.x + ci * cw, y, cw, rh)
            deck.rect(cb, fill, line=(C_["border"], 1), radius=eng.TOK()["radius"]["sm"], group=f"t{ri}")
            color = C_["ink"] if is_head else C_["muted"]
            if not is_head:
                if "✅" in cell:
                    color = SEM["green"]
                elif "⚠" in cell:
                    color = SEM["amber"]
            eng.layout_texts(deck, [{"content": cell, "fs": 11, "min_fs": 9,
                                     "color": color, "bold": is_head}],
                             cb, pad=eng.sp("sm"), breath=0, align="left", group=f"t{ri}")

def build_list(deck, box, blk):
    items = blk["items"]
    n = len(items)
    gap = eng.sp("sm")
    ih = (box.h - gap * (n - 1)) / n
    for i, it in enumerate(items):
        y = box.y + i * (ih + gap)
        cb = eng.Box(box.x, y, box.w, ih)
        deck.rect(cb, C()["card"], line=(C()["border"], 1), radius=eng.TOK()["radius"]["md"], group=f"l{i}")
        eng.layout_texts(deck, [{"content": "• " + it, "fs": 12, "min_fs": 9, "color": C()["muted"]}],
                         cb, pad=eng.PAD_CARD(), breath=0, align="left", group=f"l{i}")

def build_text(deck, box, blk):
    # 盒子高度富余时放大字号（陈述式版式），避免少内容页大片空白
    fs = 14
    nat = eng.text_h(blk["text"], fs, max(1, box.w - 2 * eng.sp("md")))
    if box.h > nat * 4 and len(blk["text"]) < 140:
        fs, align = 28, "center"
    elif box.h > nat * 2.2 and len(blk["text"]) < 260:
        fs, align = 20, "left"
    else:
        align = "left"
    eng.layout_texts(deck, [{"content": blk["text"], "fs": fs, "min_fs": 10, "color": C()["ink"]}],
                     box, pad=eng.sp("md"), breath=0, align=align, group="txt")

# ---------------------------------------------------------------------------
# 语义组件渲染（#13 富文本色 / #14 数据凸显）
# ---------------------------------------------------------------------------
def build_kpirow(deck, box, blk):
    items = blk["items"]
    n = len(items)
    if n == 0:
        return
    gap = eng.sp("md")
    cw = (box.w - gap * (n - 1)) / n
    for i, it in enumerate(items):
        cb = eng.Box(box.x + i * (cw + gap), box.y, cw, box.h)
        build_kpi(deck, cb, it, group=f"k{i}")

def build_kpi(deck, box, it, group="kpi"):
    C_ = C()
    # 卡片底（轻描边区分每个 KPI）
    deck.rect(eng.Box(box.x, box.y, box.w, box.h), C_["card"], line=(C_["border"], 1),
              radius=eng.TOK()["radius"]["md"], group=group)
    # 数字暴力美学：锁定 38pt 大字号，不参与二分缩放 (#14)
    col = it.get("color") or C_["ink"]
    num_fs = 38
    num_txt = it["num"] + (it["unit"] or "")
    deck.text(eng.Box(box.x, box.y + 4, box.w, 46), num_txt, num_fs, col, bold=True, align="center", group=group)
    if it["lab"]:
        deck.text(eng.Box(box.x, box.y + 52, box.w, 20), it["lab"], 12, C_["muted"], align="center", group=group)

def build_highlight(deck, box, blk, group="hl"):
    C_ = C()
    tone = blk.get("tone", "blue")
    bg = SEM.get(tone + "Bg", C_["card"])
    fg = SEM.get(tone, C_["blue"])
    deck.rect(eng.Box(box.x, box.y, box.w, box.h), bg, radius=eng.TOK()["radius"]["md"], group=group)
    eng.accent_bar(deck, eng.Box(box.x, box.y, 6, box.h), fg, vertical=True, group=group)
    eng.layout_texts(deck, [{"content": blk["text"], "fs": 13, "min_fs": 10, "color": C_["ink"]}],
                     eng.Box(box.x + 16, box.y, box.w - 24, box.h), pad=eng.sp("sm"), breath=eng.sp("sm"),
                     align="left", group=group)

def build_infocard(deck, box, blk, group="ic"):
    C_ = C()
    accent = blk.get("accent") or C_["blue"]
    deck.rect(eng.Box(box.x, box.y, box.w, box.h), C_["card"], line=(C_["border"], 1),
              radius=eng.TOK()["radius"]["md"], group=group)
    eng.accent_bar(deck, eng.Box(box.x, box.y, 5, box.h), accent, vertical=True, group=group)
    inner = eng.Box(box.x + 14, box.y + 6, box.w - 22, box.h - 12)
    items = []
    if blk.get("title"):
        items.append({"content": blk["title"], "fs": 13, "min_fs": 11,
                      "color": blk.get("title_color") or accent, "bold": True})
    for it in blk.get("items", []):
        items.append({"content": it, "fs": 10, "min_fs": 8, "color": C_["muted"]})
    eng.layout_texts(deck, items, inner, pad=eng.PAD_CARD(), breath=eng.sp("xs"), align="left", group=group)

def build_roi(deck, box, blk, group="roi"):
    boxes = blk["boxes"]
    n = len(boxes)
    if n == 0:
        return
    C_ = C()
    gap = eng.sp("lg")
    cw = (box.w - gap * (n - 1)) / n
    for i, b in enumerate(boxes):
        cb = eng.Box(box.x + i * (cw + gap), box.y, cw, box.h)
        tone = b.get("tone", "gold")
        fg = SEM.get(tone, C_["gold"])
        deck.rect(eng.Box(cb.x, cb.y, cb.w, cb.h), C_["card"], line=(C_["border"], 1),
                  radius=eng.TOK()["radius"]["md"], group=group)
        eng.accent_bar(deck, eng.Box(cb.x, cb.y, cb.w, 6), fg, vertical=False, group=group)  # 顶部色带
        inner = eng.Box(cb.x + 12, cb.y + 14, cb.w - 24, cb.h - 22)
        items = []
        if b.get("title"):
            items.append({"content": b["title"], "fs": 13, "min_fs": 11, "color": fg, "bold": True})
        for rl, rr in b.get("items", []):
            line = (rl + "：" + rr) if rl else rr
            items.append({"content": line, "fs": 10, "min_fs": 8, "color": C_["muted"]})
        eng.layout_texts(deck, items, inner, pad=eng.sp("sm"), breath=eng.sp("xs"), align="left", group=group)

def build_modcard(deck, box, blk, group="mc"):
    C_ = C()
    accent = SEM.get("blue", "#1565C0")
    deck.rect(eng.Box(box.x, box.y, box.w, box.h), C_["card"], line=(C_["border"], 1),
              radius=eng.TOK()["radius"]["md"], group=group)
    eng.accent_bar(deck, eng.Box(box.x, box.y, 5, box.h), accent, vertical=True, group=group)
    icon = blk.get("icon") or ""
    if icon:
        deck.rect(eng.Box(box.x + 10, box.y + 8, 28, 28), SEM.get("blueBg", "#E3F2FD"),
                  radius=eng.TOK()["radius"]["sm"], group=group)
        deck.text(eng.Box(box.x + 10, box.y + 10, 28, 24), icon, 16,
                  C_["ink"], align="center", group=group)
    inner_x = box.x + (46 if icon else 12)
    inner_w = box.w - (56 if icon else 24)
    inner = eng.Box(inner_x, box.y + 6, inner_w, box.h - 12)
    items = []
    title = blk.get("title") or ""
    if title:
        items.append({"content": title, "fs": 14, "min_fs": 12,
                      "color": C_["ink"], "bold": True})
    desc = blk.get("desc") or ""
    if desc:
        items.append({"content": desc, "fs": 10, "min_fs": 8, "color": C_["muted"]})
    status = blk.get("status") or ""
    if status:
        sc = SEM["green"] if ("✅" in status or "上线" in status) else (
             SEM["amber"] if "⚠" in status else C_["muted"])
        items.append({"content": status, "fs": 10, "min_fs": 8, "color": sc, "bold": True})
    eng.layout_texts(deck, items, inner, pad=eng.PAD_CARD(), breath=eng.sp("xs"), align="left", group=group)

def build_row(deck, box, blk):
    cells = blk["cells"]
    n = len(cells)
    if n == 0:
        return
    cols = min(blk.get("cols", n) or n, n)
    gap = eng.sp("lg")
    cw = (box.w - gap * (cols - 1)) / cols
    # 若单列（纵向 flex），按可用高度均分；否则按列宽铺
    if cols == 1:
        ch = (box.h - gap * (n - 1)) / n
        for i, c in enumerate(cells):
            cb = eng.Box(box.x, box.y + i * (ch + gap), box.w, ch)
            _build_cell(deck, cb, c)
    else:
        for i, c in enumerate(cells):
            cb = eng.Box(box.x + i * (cw + gap), box.y, cw, box.h)
            _build_cell(deck, cb, c)

def _build_cell(deck, box, blk):
    """行内单格：按其 kind 分发（table / infocard / card / ...）。"""
    k = blk.get("kind")
    if k == "table":
        build_table(deck, box, blk)
    elif k == "infocard":
        build_infocard(deck, box, blk)
    elif k == "kpirow":
        build_kpirow(deck, box, blk)
    elif k == "row":
        build_row(deck, box, blk)
    elif k == "card":
        build_card(deck, box, blk, group="rc")
    elif k == "numbered":
        build_numbered(deck, box, blk)
    elif k == "list":
        build_list(deck, box, blk)
    elif k == "text":
        build_text(deck, box, blk)
    else:
        build_card(deck, box, blk, group="rc")

# 长竖向序列分页：单页放不下的 timeline/numbered 拆成多页
MIN_CARD_H = 64

def _body_h():
    return VH - (MARGIN + HEADER_H + eng.sp("lg")) - MARGIN

def split_vertical(blk):
    """竖向序列（timeline/numbered）与 grid 按自然高度贪心拆页：
    每个 chunk 的自然总高不超过正文区高度，矮卡可多装、高卡少装，绝不超页压缩。"""
    body_h = _body_h()
    # 新结构化 timeline（横向阶段卡片）不拆页，整体保留
    if blk["kind"] == "timeline" and blk.get("phases"):
        return [blk]
    if blk["kind"] in ("timeline", "numbered") and len(blk.get("items", [])) > 1:
        gap = eng.sp("md")
        indent = 110 if blk["kind"] == "timeline" else 40
        card_w = (VW - 2 * MARGIN) - indent
        out, cur, cur_h = [], [], 0.0
        for c in blk["items"]:
            nh = max(MIN_CARD_H, _card_natural(c, card_w))
            add = nh + (gap if cur else 0)
            if cur and cur_h + add > body_h:
                chunk = dict(blk); chunk["items"] = cur
                out.append(chunk)
                cur, cur_h = [c], nh
            else:
                cur.append(c); cur_h += add
        if cur:
            chunk = dict(blk); chunk["items"] = cur
            out.append(chunk)
        return out
    if blk["kind"] == "grid":
        cols = blk["cols"]
        gap = eng.sp("lg")
        cell_w = ((VW - 2 * MARGIN) - gap * (cols - 1)) / cols
        cards = blk["cards"]
        rows = [cards[i:i + cols] for i in range(0, len(cards), cols)]
        out, cur, cur_h = [], [], 0.0
        for row in rows:
            rh = max(MIN_CARD_H, max(_card_natural(c, cell_w) for c in row))
            add = rh + (gap if cur else 0)
            if cur and cur_h + add > body_h:
                chunk = dict(blk); chunk["cards"] = [c for r in cur for c in r]
                out.append(chunk)
                cur, cur_h = [row], rh
            else:
                cur.append(row); cur_h += add
        if cur:
            chunk = dict(blk); chunk["cards"] = [c for r in cur for c in r]
            out.append(chunk)
        return out
    return [blk]

def _card_natural(card, w):
    """卡片最小高度：与 build_card→layout_texts 的公式严格一致
    （同 pad=PAD_CARD_LG、同 breath=sp("sm")、min 字号 标题12/正文9），
    保证按此高度分配时 layout_texts 缩到 min_fs 后恰好放得下、绝不溢出。"""
    pad = eng.PAD_CARD_LG()
    breath = eng.sp("sm")
    avail = max(1, w - 2 * pad)
    hs = []
    if card.get("title"):
        hs.append(eng.text_h(card["title"], 12, avail))
    for line in card.get("body", []):
        hs.append(eng.text_h(line, 9, avail))
    h = sum(hs) + breath * max(0, len(hs) - 1)
    return max(MIN_CARD_H, h + 2 * pad)

def _block_natural(blk, avail_w):
    if blk["kind"] == "grid":
        cols = blk["cols"]
        cell_w = (avail_w - eng.sp("lg") * (cols - 1)) / cols
        cnh = max(MIN_CARD_H, max(_card_natural(c, cell_w) for c in blk["cards"]))
        rows = (len(blk["cards"]) + cols - 1) // cols
        return rows * cnh + eng.sp("lg") * (rows - 1)
    if blk["kind"] == "card":
        return max(MIN_CARD_H, _card_natural(blk, avail_w))
    if blk["kind"] == "timeline":
        # 新结构化 timeline（横向阶段卡片）：固定高度
        if blk.get("phases"):
            return 90  # 标题28 + 日期24 + tags间距 + padding
        # 旧竖向列表格式
        indent = 110
        hs = [max(MIN_CARD_H, _card_natural(c, avail_w - indent)) for c in blk["items"]]
        return sum(hs) + eng.sp("md") * (len(hs) - 1)
    if blk["kind"] == "numbered":
        indent = 40
        hs = [max(MIN_CARD_H, _card_natural(c, avail_w - indent)) for c in blk["items"]]
        return sum(hs) + eng.sp("md") * (len(hs) - 1)
    if blk["kind"] == "table":
        return len(blk["rows"]) * 30 + eng.sp("xs") * (len(blk["rows"]) - 1)
    if blk["kind"] == "list":
        cnh = max(40, _card_natural({"title": "", "body": blk["items"][:1]}, avail_w))
        return len(blk["items"]) * cnh + eng.sp("sm") * (len(blk["items"]) - 1)
    if blk["kind"] == "text":
        return eng.text_h(blk["text"], 14, avail_w) + eng.sp("md")
    if blk["kind"] == "row":
        # row 的自然高度 = 子元素最大高度（横向排列时）或子元素之和（纵向）
        cells = blk.get("cells", [])
        if not cells:
            return MIN_CARD_H
        cols = blk.get("cols", len(cells))
        gap = eng.sp("lg")
        if cols > 1:
            # 横向：取最高子元素 + gap
            return max(_block_natural(c, avail_w / max(cols, 1)) for c in cells)
        else:
            # 纵向或单列：累加
            return sum(_block_natural(c, avail_w) for c in cells) + gap * max(0, len(cells) - 1)
    return MIN_CARD_H

def _build_deck(header, blocks, heights, ptype="section", with_header=True):
    deck = eng.Deck()
    deck._all_text_blocks = bool(blocks) and all(b["kind"] == "text" for b in blocks)
    # #9 封面渐变面板：纯装饰底，提升封面丰满度；整块含纳正文不触发几何错误，并拉高填充率
    if ptype == "hero" and with_header:
        deck.rect(eng.Box(0, 0, VW, VH), "#EEF2FF", gradient=("#EEF2FF", "#F4F5F8"),
                  group="herob", radius=0)
    if with_header:
        build_header(deck, eng.Box(MARGIN, MARGIN, VW - 2 * MARGIN, HEADER_H), header)
        y = MARGIN + HEADER_H + eng.sp("lg")
        x0, full_w = MARGIN, VW - 2 * MARGIN
    else:
        # 模板模式：模板自带页眉/编号，内容铺满可用区
        y = 0
        x0, full_w = 0, VW
    for b, h in zip(blocks, heights):
        bb = eng.Box(x0, y, full_w, h)
        k = b["kind"]
        if k == "grid":
            build_grid(deck, bb, b)
        elif k == "timeline":
            build_timeline(deck, bb, b)
        elif k == "numbered":
            build_numbered(deck, bb, b)
        elif k == "table":
            build_table(deck, bb, b)
        elif k == "list":
            build_list(deck, bb, b)
        elif k == "card":
            build_card(deck, bb, b, group="g0")
        elif k == "text":
            build_text(deck, bb, b)
        elif k == "kpirow":
            build_kpirow(deck, bb, b)
        elif k == "highlight":
            build_highlight(deck, bb, b)
        elif k == "roi":
            build_roi(deck, bb, b)
        elif k == "infocard":
            build_infocard(deck, bb, b)
        elif k == "modcard":
            build_modcard(deck, bb, b)
        elif k == "row":
            build_row(deck, bb, b)
        else:
            build_card(deck, bb, b, group="g0")
        y += h + eng.sp("lg")
    return deck

def render_slides(header, blocks, ptype="section", with_header=True):
    """把 blocks 排成若干页：内容驱动高度 + 溢出自动分页 + 不足则拉伸填满（#8 结构保真）。"""
    gap = eng.sp("lg")
    # 内容宽度：模板模式(无引擎页眉)内容铺满整张虚拟画布；常规模式左右留 MARGIN
    cw = (VW - 2 * MARGIN) if with_header else VW
    expanded = []
    for b in blocks:
        expanded.extend(split_vertical(b))
    if not expanded:
        return [_build_deck(header, [], [], ptype=ptype, with_header=with_header)]
    if with_header:
        body_top = MARGIN + HEADER_H + gap
        body_h = VH - body_top - MARGIN
    else:
        body_top = 0
        body_h = VH
    # 贪心装页
    slides, cur, y = [], [], body_top
    for b in expanded:
        nh = _block_natural(b, cw)
        if cur and y + nh > VH - MARGIN + 1:
            slides.append(cur); cur, y = [], body_top
        cur.append(b); y += nh + gap
    if cur:
        slides.append(cur)
    # 合并过小页到相邻页（前向或后向），避免孤零零的空白页；合并后必须仍放得下
    def _pg_h(sl):
        return sum(_block_natural(b, cw) for b in sl) + gap * (len(sl) - 1)
    merged = list(slides)
    changed = True
    while changed:
        changed = False
        for i, sl in enumerate(merged):
            if not (_pg_h(sl) < 0.45 * body_h and len(sl) <= 2):
                continue
            # 优先并入上一页，其次并入下一页
            if i > 0 and _pg_h(merged[i - 1]) + gap + _pg_h(sl) <= body_h:
                merged[i - 1].extend(sl); merged.pop(i); changed = True; break
            if i + 1 < len(merged) and _pg_h(sl) + gap + _pg_h(merged[i + 1]) <= body_h:
                merged[i + 1][:0] = sl; merged.pop(i); changed = True; break
    # 逐页渲染（时间线/编号不拉伸，避免内容溢出边界）
    decks, first = [], True
    for sl in merged:
        nhs = [_block_natural(b, cw) for b in sl]
        total = sum(nhs) + gap * (len(sl) - 1)
        if total < body_h:
            extra = body_h - total
            nhs = [(h + extra * (h / total)) if b["kind"] not in ("timeline", "numbered") else h
                   for h, b in zip(nhs, sl)]
        h_used = sum(nhs) + gap * (len(sl) - 1)
        if h_used > body_h:
            nhs = [h * (body_h / h_used) for h in nhs]
        hdr = dict(header)
        if not first:
            hdr["title"] = (header["title"] or "续") + "（续）"
        decks.append(_build_deck(hdr, sl, nhs, ptype="hero" if first and ptype == "hero" else "section",
                                 with_header=with_header))
        first = False
    return decks

# ---------------------------------------------------------------------------
# QA Layer2：填充率（内容面积 / 正文区面积）
# ---------------------------------------------------------------------------
def fill_rate(deck, body_area=None):
    if body_area is None:
        body_area = (VW - 2 * MARGIN) * (VH - (MARGIN + HEADER_H + eng.sp("lg")) - MARGIN)
    content = 0.0
    for r in deck.recs:
        if r.kind in ("rect", "text") and r.group not in ("head",):
            content += r.w * r.h
    return min(1.0, content / body_area) if body_area else 0.0

# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# 数据模型 schema 强校验 (#3)
# 解析后的页面/块若缺关键字段, 报警并写入 QA, 防止"内容静默丢失"。
# ---------------------------------------------------------------------------
def check_blocks_schema(ptype, header, blocks):
    msgs = []
    title = (header.get("title") or "").strip()
    if not title:
        msgs.append("页面缺少标题(header.title) — 封面/章节页至少应有 h1/h2 标题")
    if not blocks:
        msgs.append("页面无正文块 — 该 section 可能仅含标题或未被识别为正文, 请检查 HTML 结构")
        return msgs
    for i, b in enumerate(blocks):
        kind = b.get("kind")
        if kind == "card":
            if not b.get("title") and not b.get("body"):
                msgs.append(f"card#{i} 既无标题也无正文 — 卡片内容可能丢失")
        elif kind in ("timeline", "numbered"):
            items = b.get("items") or []
            if not items:
                msgs.append(f"{kind}#{i} 无条目(items) — 时间线/步骤为空")
            for j, it in enumerate(items):
                if not it.get("title") and not it.get("body"):
                    msgs.append(f"{kind}#{i}.item{j} 既无标题也无正文")
        elif kind == "grid":
            cards = b.get("cards") or b.get("items") or []
            if not cards:
                msgs.append(f"grid#{i} 无子卡 — 栅格容器为空")
            for j, c in enumerate(cards):
                if not c.get("title") and not c.get("body"):
                    msgs.append(f"grid#{i}.card{j} 既无标题也无正文")
        elif kind == "table":
            if not b.get("rows"):
                msgs.append(f"table#{i} 无行数据")
    return msgs


# ---------------------------------------------------------------------------
# QA 几何闸门 (#1) — 几何错误>0 即 FAIL(硬闸门, 不可交付); 空白风险仅警告
# ---------------------------------------------------------------------------
def qa_gate(qa):
    n_err = len(qa["errors"])
    if n_err:
        return False, f"❌ QA FAIL: {n_err} 个几何错误(重叠/越界/拥挤), 不可交付, 请先修复后再转"
    n_warn = len(qa["warnings"])
    return True, f"✅ QA PASS: 0 几何错误, {n_warn} 条警告(含空白风险/内容提示)"


def _render_page(args):
    """#7 子进程工作函数：渲染单页 SVG+PNG 并做 L1 几何校验（与主线同源、可并行）。"""
    deck, svg, png, font_path = args
    errs, warns = eng.validate(deck.recs)
    eng.emit_svg(deck, svg)
    try:
        eng.render_deck_png(deck, png, scale_px=1.4, font_path=font_path)
    except Exception as e:
        warns.append(f"PNG 渲染失败: {e}")
    return errs, warns, svg, png


def convert(html_path, out_pptx, preview_dir, qa_path, workers=None,
            template=None, pages=None, tpl_slide=3, margin_cm=0.8):
    """通用 HTML→PPT 主流程。

    template : 给定 PPT 模板路径 → 走【模板克隆模式】(Branch B)：可用区作为尺寸锚点，
               内容铺满可用区、跳过引擎自带页眉、用模板版式承载标题/编号。
    pages    : 1-based 页码列表(对准 HTML 的 <div class="page"> 顺序)，仅渲染指定页。
    """
    global VW, VH
    soup = BeautifulSoup(open(html_path, encoding="utf-8").read(), "lxml")
    all_pages = parse_pages(soup)
    # --pages 过滤（1-based，对准 HTML 的 <div class="page"> 文档顺序）
    if pages:
        sel = set(int(x) for x in pages)
        pages_list = [(pt, el) for i, (pt, el) in enumerate(all_pages, start=1) if i in sel]
    else:
        pages_list = all_pages
    use_tpl = bool(template)
    if use_tpl:
        prs = eng.load_presentation_safe(template)
        area = eng.configure_from_template(prs, tpl_slide, margin_cm)
        eng.delete_all_slides(prs)                      # 清掉模板原始页, 只克隆版式承载内容
        VW, VH = eng.CFG["vw"], eng.CFG["vh"]          # 同步虚拟画布到模板可用区比例
        body_area = VW * VH                            # 模板模式：内容铺满整张虚拟画布
    else:
        prs = eng.new_presentation()
        body_area = None
    qa = {"pages": [], "errors": [], "warnings": [], "_template": template or ""}
    os.makedirs(preview_dir, exist_ok=True)
    # 1) 先构建全部 deck + 收集元数据（顺序，保证页码稳定）
    jobs, idx = [], 0
    for ptype, el in pages_list:
        header = extract_header(el)
        # 页眉元素集合（标题 + 其前后短文本），不进正文，避免重复
        skip = set()
        h = el.find(HEADING_TAGS)
        if h is not None:
            skip.add(h)
            prev = h.find_previous_sibling()
            if prev is not None and prev.name in ("div", "p", "span"):
                skip.add(prev)
            nxt = h.find_next_sibling()
            if nxt is not None and nxt.name == "p":
                skip.add(nxt)
        container = get_body_container(el, skip)
        body_blocks = extract_blocks(container, skip=skip)
        # 若跳过"标题+其后<p>"导致正文为空，则该 <p> 实为页面内容，放回正文
        if not body_blocks:
            h0 = el.find(HEADING_TAGS)
            nxt0 = h0.find_next_sibling() if h0 is not None else None
            if nxt0 is not None and nxt0.name == "p" and nxt0 in skip:
                skip.discard(nxt0)
                container = get_body_container(el, skip)
                body_blocks = extract_blocks(container, skip=skip)
        schema_warns = check_blocks_schema(ptype, header, body_blocks)  # #3 漏字段报警
        with_header = not use_tpl
        decks = render_slides(header, body_blocks, ptype=ptype, with_header=with_header)
        for deck in decks:
            idx += 1
            slide_name = f"slide_{idx:02d}"
            svg = os.path.join(preview_dir, slide_name + ".svg")
            png = os.path.join(preview_dir, slide_name + ".png")
            jobs.append({"deck": deck, "header": header, "ptype": ptype,
                         "schema_warns": schema_warns, "idx": idx, "svg": svg,
                         "png": png, "nblocks": len(body_blocks),
                         "title": header.get("title", ""),
                         "kicker": header.get("kicker", ""),
                         "with_header": with_header})
    # 2) 并行渲染预览（ProcessPool；异常则回退顺序，保证健壮性 #7）
    payload = [(j["deck"], j["svg"], j["png"], FONT_PATH) for j in jobs]
    try:
        import multiprocessing as _mp
        from concurrent.futures import ProcessPoolExecutor
        w = max(1, int(workers)) if workers else min(8, (_mp.cpu_count() or 4))
        with ProcessPoolExecutor(max_workers=w) as ex:
            results = list(ex.map(_render_page, payload))
        mode = f"并行×{w}"
    except Exception:
        results = [_render_page(a) for a in payload]
        mode = "顺序(回退)"
    # 3) 顺序组装 PPTX（prs 单对象不可并行）+ 汇总 QA
    for j, (errs, warns, svg, png) in zip(jobs, results):
        warns = list(warns) + j["schema_warns"]  # #3 schema 告警并入本页
        if use_tpl:
            eng.add_slide_from_template(prs, j["deck"], title=j["title"], badge=j["kicker"])
        else:
            eng.add_slide_from_deck(prs, j["deck"])
        fr = fill_rate(j["deck"], body_area=body_area)
        # hero 与纯文本陈述页属于刻意留白版式，不算空白风险
        statement = getattr(j["deck"], "_all_text_blocks", False)
        cont_flag = fr < 0.55 and j["ptype"] != "hero" and not statement
        if cont_flag:
            warns.append(f"[空白风险] 填充率 {fr:.0%} < 55%")
        qa["pages"].append({
            "slide": j["idx"], "type": j["ptype"], "title": j["title"],
            "blocks": j["nblocks"], "fill_rate": round(fr, 3),
            "blank_risk": cont_flag, "svg": svg, "png": png,
            "with_header": j["with_header"],
        })
        qa["errors"].extend([f"[S{j['idx']}] {e}" for e in errs])
        qa["warnings"].extend([f"[S{j['idx']}] {w_}" for w_ in warns])
    prs.save(out_pptx)
    qa["_mode"] = mode
    qa["_template_used"] = bool(use_tpl)
    with open(qa_path, "w", encoding="utf-8") as f:
        json.dump(qa, f, ensure_ascii=False, indent=2)
    return qa

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--out", default="out.pptx")
    ap.add_argument("--preview-dir", default="previews")
    ap.add_argument("--qa", default="qa.json")
    ap.add_argument("--workers", type=int, default=None, help="并行渲染预览的进程数(默认按 CPU)")
    ap.add_argument("--template", default=None, help="PPT 模板路径 → 走模板克隆模式(内容铺满可用区)")
    ap.add_argument("--pages", default=None, help="只渲染指定页(逗号分隔, 1-based, 对准 <div class=page> 顺序)")
    ap.add_argument("--tpl-slide", type=int, default=3, help="克隆的模板页索引(默认 3=标题和内容 版式)")
    ap.add_argument("--margin", type=float, default=0.8, help="模板可用区边距(cm)")
    args = ap.parse_args()
    pages = [p.strip() for p in args.pages.split(",")] if args.pages else None
    qa = convert(args.html, args.out, args.preview_dir, args.qa, workers=args.workers,
                 template=args.template, pages=pages, tpl_slide=args.tpl_slide, margin_cm=args.margin)
    print(f"✅ 已写出 {args.out}（{len(qa['pages'])} 页，QA 见 {args.qa}，渲染模式：{qa.get('_mode','顺序')}）")
    for p in qa["pages"]:
        flag = " ⚠空白" if p["blank_risk"] else ""
        print(f"  S{p['slide']:>2} [{p['type']}] {p['title'][:24]:<24} 填充 {p['fill_rate']:.0%}{flag}")
    passed, msg = qa_gate(qa)  # #1 几何闸门
    print(msg)
    if not passed:
        sys.exit(2)  # 硬失败：几何错误不可交付

if __name__ == "__main__":
    main()
