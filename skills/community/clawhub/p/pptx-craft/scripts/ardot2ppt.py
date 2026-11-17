# -*- coding: utf-8 -*-
"""
ardot2ppt.py  —  pptx-craft 画布轴桥接器（治本项 #10：Ardot 画布 → PPT）
==================================================================================
把 Ardot 设计画布导出的节点树（与 ardot-design-core 的节点 schema 对齐：
FRAME / RECTANGLE / ELLIPSE / TEXT / LINE + x/y/width/height/fills/strokes/
cornerRadius/characters/fontSize/fontWeight/textAlignHorizontal）直接映射为
pptx_flex_engine 的渲染原语，复用同一套 L1 几何校验 + QA 闸门。

映射规则（零专属结构、纯几何/属性驱动）：
  · RECTANGLE / FRAME(含 fill) -> deck.rect（支持实色/渐变 fill、圆角、描边）
  · FRAME(无 fill) / GROUP / SECTION -> 仅作容器，递归子节点（子节点用绝对坐标）
  · ELLIPSE  -> deck.ellipse
  · TEXT     -> deck.text（characters / fontSize / fontWeight / 水平对齐 / 颜色）
  · LINE     -> 细分隔条 divider
坐标：每页按 PAGE 的 width/height 等比 letterbox 居中映射到虚拟画布 1440×680。

用法:
  python ardot2ppt.py <canvas.json> [--out out.pptx] [--preview-dir previews] [--qa qa.json]
依赖: python-pptx, pillow
"""
import os, sys, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pptx_flex_engine as eng
from pptx_flex_engine import Box

VW, VH = 1440, 680
FONT_PATH = r"C:/Windows/Fonts/msyh.ttc"


# ---------------------------------------------------------------------------
# 颜色解析（Ardot fills: SOLID / GRADIENT_LINEAR）
# ---------------------------------------------------------------------------
def _clamp(v):
    return max(0, min(255, int(round(v * 255))))

def _rgba_to_hex(c):
    if not c:
        return None
    if "hex" in c and c["hex"]:
        return c["hex"]
    r = _clamp(c.get("r", 0)); g = _clamp(c.get("g", 0)); b = _clamp(c.get("b", 0))
    return f"#{r:02X}{g:02X}{b:02X}"

def _node_fill(node):
    for f in (node.get("fills") or []):
        if f.get("visible", True) is False:
            continue
        t = f.get("type")
        if t == "SOLID":
            return ("solid", _rgba_to_hex(f.get("color")))
        if t in ("GRADIENT_LINEAR", "GRADIENT"):
            stops = f.get("gradientStops") or []
            if len(stops) >= 2:
                return ("gradient", (_rgba_to_hex(stops[0]["color"]),
                                      _rgba_to_hex(stops[-1]["color"])))
    return None

def _node_stroke(node):
    for s in (node.get("strokes") or []):
        if s.get("visible", True) is False:
            continue
        col = _rgba_to_hex(s.get("color"))
        if col:
            return (col, node.get("strokeWeight", 1))
    return None

def _box_of(node):
    bb = node.get("absoluteBoundingBox")
    if bb:
        return bb.get("x", 0), bb.get("y", 0), bb.get("width", 0), bb.get("height", 0)
    return node.get("x", 0), node.get("y", 0), node.get("width", 0), node.get("height", 0)


# ---------------------------------------------------------------------------
# 递归：节点 -> 引擎原语（绝对坐标）
# ---------------------------------------------------------------------------
def _walk(deck, node, ox, oy, scale):
    if node.get("removed") or node.get("visible", True) is False:
        return
    t = node.get("type")
    x, y, w, h = _box_of(node)
    X, Y, W, H = ox + x * scale, oy + y * scale, w * scale, h * scale
    if t in ("RECTANGLE", "FRAME", "GROUP", "SECTION", "COMPONENT", "INSTANCE", "BOOLEAN_OPERATION"):
        fill = _node_fill(node)
        radius = int((node.get("cornerRadius") or 0) * scale)
        line = _node_stroke(node)
        if fill and fill[0] == "solid":
            deck.rect(Box(X, Y, W, H), fill[1], line=line, radius=radius, group="c")
        elif fill and fill[0] == "gradient":
            deck.rect(Box(X, Y, W, H), fill[1][0], gradient=fill[1], line=line,
                      radius=radius, group="c")
        for ch in node.get("children", []):
            _walk(deck, ch, ox, oy, scale)
    elif t == "ELLIPSE":
        col = _rgba_to_hex((node.get("fills") or [{}])[0].get("color")) or "#0F172A"
        deck.ellipse(Box(X, Y, W, H), col, group="c")
    elif t == "TEXT":
        f = node.get("characters") or ""
        fs = max(8, int((node.get("fontSize") or 14) * scale * 0.75))
        bold = (node.get("fontWeight") or 400) >= 600
        al = {"CENTER": "center", "RIGHT": "right"}.get(node.get("textAlignHorizontal"), "left")
        col = _rgba_to_hex((node.get("fills") or [{}])[0].get("color")) or "#0F172A"
        deck.text(Box(X, Y, W, H), f, fs, col, bold=bold, align=al, group="ct")
    elif t == "LINE":
        col = _rgba_to_hex((node.get("strokes") or [{}])[0].get("color")) or "#E2E8F0"
        deck.rect(Box(X, Y, W, max(2, H)), col, radius=0, group="c")
    # 其它类型（VECTOR/STAR…）暂忽略，不阻断主流程


def canvas_to_decks(canvas):
    """画布 JSON -> [(deck, title), ...]，每页一个 deck。"""
    decks = []
    pages = canvas.get("pages") or []
    if not pages and "document" in canvas:
        pages = [p for p in canvas["document"].get("children", []) if p.get("type") == "PAGE"]
    for pg in pages:
        pw = pg.get("width") or pg.get("absoluteBoundingBox", {}).get("width") or VW
        ph = pg.get("height") or pg.get("absoluteBoundingBox", {}).get("height") or VH
        scale = min(VW / pw, VH / ph)
        ox, oy = (VW - pw * scale) / 2, (VH - ph * scale) / 2
        deck = eng.Deck()
        for node in pg.get("children", []):
            _walk(deck, node, ox, oy, scale)
        decks.append((deck, pg.get("name", "Slide")))
    return decks


# ---------------------------------------------------------------------------
# QA：填充率（画布为满幅设计，按整画布计；仅作报告，不触发空白警告）
# ---------------------------------------------------------------------------
def _fill_rate(deck):
    area = VW * VH
    content = sum(r.w * r.h for r in deck.recs if r.kind in ("rect", "text"))
    return min(1.0, content / area) if area else 0.0


def qa_gate(qa):
    n = len(qa["errors"])
    if n:
        return False, f"❌ QA FAIL: {n} 个几何错误, 不可交付"
    return True, f"✅ QA PASS: 0 几何错误, {len(qa['warnings'])} 条警告"


def convert(json_path, out_pptx, preview_dir, qa_path):
    canvas = json.load(open(json_path, encoding="utf-8"))
    decks = canvas_to_decks(canvas)
    prs = eng.new_presentation()
    qa = {"pages": [], "errors": [], "warnings": []}
    os.makedirs(preview_dir, exist_ok=True)
    for i, (deck, title) in enumerate(decks, 1):
        errs, warns = eng.validate(deck.recs)
        eng.add_slide_from_deck(prs, deck)
        slide = f"slide_{i:02d}"
        svg = os.path.join(preview_dir, slide + ".svg")
        png = os.path.join(preview_dir, slide + ".png")
        eng.emit_svg(deck, svg)
        try:
            eng.render_deck_png(deck, png, scale_px=1.4, font_path=FONT_PATH)
        except Exception as e:
            warns.append(f"PNG 渲染失败: {e}")
        fr = _fill_rate(deck)
        qa["pages"].append({"slide": i, "type": "canvas", "title": title,
                            "fill_rate": round(fr, 3), "blank_risk": False,
                            "svg": svg, "png": png})
        qa["errors"].extend([f"[S{i}] {e}" for e in errs])
        qa["warnings"].extend([f"[S{i}] {w}" for w in warns])
    prs.save(out_pptx)
    with open(qa_path, "w", encoding="utf-8") as f:
        json.dump(qa, f, ensure_ascii=False, indent=2)
    return qa


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json")
    ap.add_argument("--out", default="out.pptx")
    ap.add_argument("--preview-dir", default="previews")
    ap.add_argument("--qa", default="qa.json")
    args = ap.parse_args()
    qa = convert(args.json, args.out, args.preview_dir, args.qa)
    print(f"✅ 已写出 {args.out}（{len(qa['pages'])} 页，QA 见 {args.qa}）")
    for p in qa["pages"]:
        print(f"  S{p['slide']:>2} [canvas] {p['title'][:24]:<24} 填充 {p['fill_rate']:.0%}")
    passed, msg = qa_gate(qa)
    print(msg)
    if not passed:
        sys.exit(2)


if __name__ == "__main__":
    main()
