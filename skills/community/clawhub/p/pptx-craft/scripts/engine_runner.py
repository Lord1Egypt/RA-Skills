# -*- coding: utf-8 -*-
"""
engine_runner.py — pptx-craft 声明式驱动层 (M1/M2/M3/M4 合一)
================================================================
把"数据模型 + 版式策略 + 主题规范"三个 JSON 文件 → 渲染成可编辑 PPTX。
这是通用引擎 pptx_flex_engine.py（纯原语库）之上的"调用方/调度层"：

  - M1 纯函数化 : render_model(data, layout, theme) 无副作用、可重入；只写文件是预期输出
  - M2 八坑防御 : direction 必填断言 / 负尺寸硬拦截(引擎层) / layout_index 合法 / 键值对同行 / CJK≥1.0
  - M3 阶段落盘 : data/layout/theme 三文件由专家团各 agent 独立产出落盘，本层只读三文件，
                 支持单阶段重跑（改某阶段只需重跑本脚本，不动其他 agent 产出）
  - M4 输入快照 : 运行前对三输入文件做 sha256，写入 <out>.snapshot.json，打回时精确回退

用法:
  python engine_runner.py --data data.json --layout layout.json --theme theme.json \
                          --out out.pptx [--preview-dir previews]

依赖: pptx_flex_engine.py（同目录）
"""

import json
import hashlib
import os
import sys
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import pptx_flex_engine as E
from pptx.util import Pt
from pptx.enum.text import PP_ALIGN

# ---------------------------------------------------------------------------
# 单位换算（虚拟画布 px ↔ 英寸/磅）
#   引擎内部用"虚拟 px"，FS(px)=px*0.75pt；配置后 PX = 每英寸虚拟 px 数
# ---------------------------------------------------------------------------
PX = 116.2  # 配置后覆盖

def PT(p):
    """磅 → 虚拟 px（引擎 FS 用 px*0.75=pt）"""
    return p / 0.75

def IN(v):
    """英寸 → 虚拟 px"""
    return v * PX

# ---------------------------------------------------------------------------
# 加载 + 快照（M4）
# ---------------------------------------------------------------------------
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def write_snapshot(inputs, out):
    snap = {
        "out": out,
        "ts": datetime.datetime.now().isoformat(timespec="seconds"),
        "inputs": [{"path": p, "sha256": _sha256(p)} for p in inputs],
    }
    spath = out + ".snapshot.json"
    with open(spath, "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=2)
    return spath

# ---------------------------------------------------------------------------
# M2 防御断言
# ---------------------------------------------------------------------------
def _assert_direction(blk):
    """Pitfall#5: 数据模型每个区块必须带 direction，禁止默认竖排"""
    if "direction" not in blk:
        raise AssertionError(
            f"[Pitfall#5 缺 direction] block type={blk.get('type')} 缺 direction 字段 "
            f"—— 渲染无法判定横排/竖排，已拦截（data-expert 必须固化 direction）")

def _assert_layout_index(prs, idx):
    """Pitfall#2: layout index 必须合法，避免套错空 layout"""
    n = len(prs.slide_layouts)
    if not (0 <= idx < n):
        raise AssertionError(
            f"[Pitfall#2 layout 非法] layout_index={idx} 超出范围 [0,{n-1}] "
            f"—— 套错 layout 会导致背景图/无主题，已拦截")

# ---------------------------------------------------------------------------
# 通用组件（基于引擎原语；内部文本优先，装饰填空）
#   所有坐标用虚拟 px（IN/PT 换算）；颜色从 theme tokens 取
# ---------------------------------------------------------------------------
def comp_highlight(deck, box, blk, T):
    """顶部高亮条：左竖条 + 浅底 + 多色 runs 文本（同行，row）"""
    deck.rect(E.Box(box.x, box.y, IN(0.04), box.h), T["blue"], group="hl")
    deck.rect(E.Box(box.x + IN(0.04), box.y, box.w - IN(0.04), box.h), T["hlBg"], group="hl")
    runs = [{"text": s["text"],
             "color": T[s.get("color", "ink")],
             "bold": s.get("bold", False)} for s in blk["segs"]]
    deck.text(E.Box(box.x + IN(0.12), box.y, box.w - IN(0.22), box.h),
           "", PT(9.5), T["ink"], runs=runs, align="left", group="hl")

def comp_kpi_row(deck, box, blk, T):
    """KPI 并排（row）：N 等分白卡 + 大数字 + 标签"""
    data = blk["data"]
    n = len(data)
    gap = IN(blk.get("gap", 0.05))
    kw = (box.w - gap * (n - 1)) / n
    for i, kpi in enumerate(data):
        kx = box.x + i * (kw + gap)
        kb = E.Box(kx, box.y, kw, box.h)
        deck.rect(kb, T["white"], line=(T["border"], 1),
               radius=E.TOK()["radius"]["lg"], group="kpi")
        deck.text(E.Box(kx, box.y + IN(0.06), kw, IN(0.42)),
               kpi["num"] + kpi.get("unit", ""),
               PT(26), T[kpi["color"]], bold=True, align="center", group="kpi")
        deck.text(E.Box(kx, box.y + box.h - IN(0.26), kw, IN(0.24)),
               kpi["lab"], PT(9), T["gray"], align="center", group="kpi")

def _card_compare(deck, box, o, color_key, T):
    """单张对比卡（优化前/后）：标题 + 竖排 items + note + foot"""
    deck.rect(box, T["white"], line=(T["border"], 1),
           radius=E.TOK()["radius"]["md"], group="cmp")
    deck.rect(E.Box(box.x, box.y, box.w, IN(0.04)), T[color_key], group="cmp")
    cy = box.y + IN(0.10)
    deck.text(E.Box(box.x + IN(0.10), cy, box.w - IN(0.20), IN(0.22)),
           o["title"], PT(11), T[color_key], bold=True, group="cmp")
    cy += IN(0.30)
    reserve = IN(0.30) if o.get("foot") else 0.0
    reserve += IN(0.32) if o.get("note") else 0.0
    items_h = max(box.h - IN(0.30) - reserve, IN(0.1))
    E.layout_texts(
        deck,
        [{"content": it, "fs": PT(8.5), "min_fs": PT(7), "color": T["ink"]}
         for it in o["items"]],
        E.Box(box.x + IN(0.10), cy, box.w - IN(0.20), items_h),
        pad=0, breath=E.sp("xs"), align="left", group="cmp")
    ny = cy + items_h
    if o.get("note"):
        deck.text(E.Box(box.x + IN(0.10), ny, box.w - IN(0.20), IN(0.30)),
               o["note"], PT(8), T["gray"], group="cmp")
    if o.get("foot"):
        deck.text(E.Box(box.x + IN(0.10), box.y + box.h - IN(0.26), box.w - IN(0.20), IN(0.24)),
               o["foot"], PT(10), T[color_key], bold=True, group="cmp")

def comp_compare2(deck, box, blk, T):
    """双列对比 + 中间箭头（row 横排，法则①）"""
    o = blk
    gap = IN(0.18)
    cw = (box.w - gap) / 2
    _card_compare(deck, E.Box(box.x, box.y, cw, box.h), o["left"], "red", T)
    deck.text(E.Box(box.x + cw, box.y, gap, box.h), "→", PT(20), T["green"],
           bold=True, align="center", group="cmp")
    _card_compare(deck, E.Box(box.x + cw + gap, box.y, cw, box.h), o["right"], "green", T)

def _info_kvp(deck, box, o, T):
    """键值对卡：label 左 / value 右 同一行（Pitfall#6 同行，禁止 value 折行）"""
    deck.rect(box, T["white"], line=(T["border"], 1),
           radius=E.TOK()["radius"]["md"], group="info")
    deck.rect(E.Box(box.x, box.y, box.w, IN(0.04)), T[o.get("border", "gold")], group="info")
    deck.text(E.Box(box.x + IN(0.10), box.y + IN(0.08), box.w - IN(0.20), IN(0.22)),
           o["title"], PT(11), T[o.get("titleColor", "dark")], bold=True, group="info")
    cy = box.y + IN(0.30)
    note_h = IN(0.30) if o.get("note") else 0.0
    line_h = max((box.h - IN(0.30) - note_h) / max(len(o["items"]), 1), IN(0.08))
    for i, kvp in enumerate(o["items"]):
        ly = cy + i * line_h
        deck.text(E.Box(box.x + IN(0.10), ly, box.w * 0.50, line_h),
               kvp["l"], PT(8.5), T["gray"], group="info")
        deck.text(E.Box(box.x + IN(0.10) + box.w * 0.50, ly, box.w * 0.40, line_h),
               kvp["r"], PT(8.5), T["ink"], bold=True, align="right", group="info")
    if o.get("note"):
        deck.text(E.Box(box.x + IN(0.10), box.y + box.h - IN(0.30), box.w - IN(0.20), IN(0.28)),
               o["note"], PT(8), T["gray"], group="info")

def _info_list(deck, box, o, T):
    """纯文本列表卡（扩展收益）"""
    deck.rect(box, T["white"], line=(T["border"], 1),
           radius=E.TOK()["radius"]["md"], group="info")
    deck.rect(E.Box(box.x, box.y, box.w, IN(0.04)), T[o.get("border", "green")], group="info")
    deck.text(E.Box(box.x + IN(0.10), box.y + IN(0.08), box.w - IN(0.20), IN(0.22)),
           o["title"], PT(11), T[o.get("titleColor", "dark")], bold=True, group="info")
    cy = box.y + IN(0.30)
    items_h = max(box.h - IN(0.30) - (IN(0.30) if o.get("note") else 0), IN(0.1))
    E.layout_texts(
        deck,
        [{"content": "• " + it, "fs": PT(8.5), "min_fs": PT(7), "color": T["ink"]}
         for it in o["items"]],
        E.Box(box.x + IN(0.10), cy, box.w - IN(0.20), items_h),
        pad=0, breath=E.sp("xs"), align="left", group="info")
    if o.get("note"):
        deck.text(E.Box(box.x + IN(0.10), box.y + box.h - IN(0.30), box.w - IN(0.20), IN(0.28)),
               o["note"], PT(8), T["gray"], group="info")

def comp_info_row(deck, box, blk, T):
    """双卡并排（row）：左 kvp / 右 list"""
    gap = IN(0.16)
    cw = (box.w - gap) / 2
    _info_kvp(deck, E.Box(box.x, box.y, cw, box.h), blk["cards"][0], T)
    _info_list(deck, E.Box(box.x + cw + gap, box.y, cw, box.h), blk["cards"][1], T)

def comp_text(deck, box, blk, T):
    """纯文本块（陈述页）"""
    E.layout_texts(
        deck,
        [{"content": s["text"], "fs": PT(s.get("fs", 10)), "min_fs": PT(8),
          "color": T[s.get("color", "ink")], "bold": s.get("bold", False)}
         for s in blk.get("segs", [{"text": blk.get("text", "")}])],
        box, pad=IN(0.10), breath=E.sp("sm"), align="left", group="txt")

# ---------------------------------------------------------------------------
# 区块分派
# ---------------------------------------------------------------------------
COMPONENTS = {
    "highlight": comp_highlight,
    "kpi_row": comp_kpi_row,
    "compare2": comp_compare2,
    "info_row": comp_info_row,
    "text": comp_text,
}

def dispatch_block(deck, box, blk, T):
    _assert_direction(blk)  # M2 #5
    fn = COMPONENTS.get(blk["type"])
    if fn is None:
        raise AssertionError(f"[未知区块类型] type={blk['type']} 引擎无对应组件")
    fn(deck, box, blk, T)

# ---------------------------------------------------------------------------
# 主渲染（M1 纯函数；M3 读三文件；M4 快照在外层）
# ---------------------------------------------------------------------------
def render_model(data, layout, theme, out, preview_dir=None):
    global PX
    tpl = layout.get("template")
    if not tpl:
        raise AssertionError("layout.json 缺 template 路径")
    idx = int(layout.get("layout_index", 1))
    margin_cm = float(layout.get("margin_cm", 0.3))
    gap = float(layout.get("gap", 0.05))
    start_off = float(layout.get("start_y_offset", 0.50))
    type_heights = layout.get("type_heights", {})

    prs = E.load_presentation_safe(tpl)
    _assert_layout_index(prs, idx)            # M2 #2
    E.configure(tokens=theme.get("tokens"))   # 主题令牌覆盖
    E.configure_from_template(prs, idx, margin_cm)  # 设 _tpl_src/_tpl_layout（克隆用）
    if "area" in layout:
        # M3: layout-expert 实测死区已落盘到 layout.json，直接消费，不再重测
        a = layout["area"]
        VW = 1440
        VH = round(a["h"] / a["w"] * 1440)
        E.CFG["vw"], E.CFG["vh"] = VW, VH
        E.CFG["slide_w_emu"] = int(a["w"] * 360000)
        E.CFG["slide_h_emu"] = int(a["h"] * 360000)
        E.CFG["scale"] = a["w"] / VW
        E.CFG["offx"] = int(a["x"] * 360000)
        E.CFG["offy"] = int(a["y"] * 360000)
        PX = VW / a["w"]
    else:
        area = E.compute_available_area(prs, idx, margin_cm)
        PX = E.CFG["vw"] / (area["cw"] / 360000.0)  # 每英寸虚拟 px

    E.delete_all_slides(prs)   # 清空模板自带页，仅保留版式用于克隆
    pages = data.get("pages", [])
    total_errors = []
    for pi, page in enumerate(pages):
        deck = E.Deck()
        cy = IN(start_off)
        for blk in page.get("blocks", []):
            h = IN(type_heights.get(blk["type"], blk.get("h", 0.5)))
            dispatch_block(deck, E.Box(0, cy, E.CFG["vw"], h), blk, theme["tokens"]["color"])
            cy += h + IN(gap)
        # M2 #1/#3: 渲染前几何校验（越界/重叠/负尺寸由引擎拦截）
        errs, warns = E.validate(deck.recs)
        if errs:
            total_errors.append({"page": pi, "errors": errs, "warns": warns})
            continue
        E.add_slide_from_template(prs, deck, title=page.get("title", ""),
                                  badge=page.get("badge", ""))
        if preview_dir:
            os.makedirs(preview_dir, exist_ok=True)
            E.emit_svg(deck, os.path.join(preview_dir, f"page_{pi+1:02d}.svg"))
            try:
                E.render_deck_png(deck, os.path.join(preview_dir, f"page_{pi+1:02d}.png"),
                                  font_path=theme.get("font_path"))
            except Exception:
                pass

    if total_errors:
        msg = "\n".join(f"  P{p['page']}: " + "; ".join(p['errors']) for p in total_errors)
        raise AssertionError(f"[QA L1 FAIL] 几何校验未过，拒绝产出（防崩闸门）:\n{msg}")

    prs.save(out)
    return out

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def cli():
    import argparse
    ap = argparse.ArgumentParser(description="pptx-craft 声明式驱动：三 JSON → PPTX")
    ap.add_argument("--data", required=True)
    ap.add_argument("--layout", required=True)
    ap.add_argument("--theme", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--preview-dir", default=None)
    args = ap.parse_args()

    data = load_json(args.data)
    layout = load_json(args.layout)
    theme = load_json(args.theme)

    out = render_model(data, layout, theme, args.out, preview_dir=args.preview_dir)
    snap = write_snapshot([args.data, args.layout, args.theme], out)  # M4
    print(f"✅ 已生成 (声明式引擎): {out}  [{os.path.getsize(out)} bytes]")
    print(f"📸 输入快照: {snap}")

if __name__ == "__main__":
    cli()
