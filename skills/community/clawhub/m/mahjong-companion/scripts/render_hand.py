#!/usr/bin/env python3
"""麻将手牌牌面渲染：把报牌字符串画成一张牌面图。

纯 HTML/CSS 渲染后截图，不用图像模型 —— 保证每次输出一致、字永远不会错。

用法：
  python3 render_hand.py --hand "123万 56万 东东东 白白白 8条" --out hand.png
  python3 render_hand.py --hand "123万 56万 东东东 白白白" --drawn "8条" --out hand.png
"""
from __future__ import annotations

import argparse
import html
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from parse_hand import parse, sort_key, classify  # noqa: E402

# ---------- 花色视觉定义 ----------

SUIT_META = {
    "万": {"label": "萬", "color": "#b23a2e", "ink": "#b23a2e"},
    "条": {"label": "條", "color": "#2f7a4f", "ink": "#2f7a4f"},
    "筒": {"label": "筒", "color": "#2b5f9e", "ink": "#2b5f9e"},
}

HONOR_LABEL = {
    "东": "東", "南": "南", "西": "西", "北": "北",
    "中": "中", "发": "發", "白": "白",
    "春": "春", "夏": "夏", "秋": "秋", "冬": "冬",
    "梅": "梅", "兰": "蘭", "竹": "竹", "菊": "菊",
}

# 数牌点数用「圆点」排布，接近真牌视觉
# 坐标为「列, 行」，范围大致 1~2（列）/ 0.9~3.4（行），由 CSS 换算成百分比
DOT_LAYOUT = {
    1: [(1.5, 2.0)],
    2: [(1.5, 1.0), (1.5, 3.0)],
    3: [(1.0, 0.9), (1.5, 1.9), (2.0, 2.9)],
    4: [(1.0, 1.0), (2.0, 1.0), (1.0, 2.9), (2.0, 2.9)],
    5: [(1.0, 1.0), (2.0, 1.0), (1.5, 1.95), (1.0, 2.9), (2.0, 2.9)],
    6: [(1.0, 0.9), (2.0, 0.9), (1.0, 1.95), (2.0, 1.95), (1.0, 3.0), (2.0, 3.0)],
    7: [(1.0, 0.55), (1.5, 0.55), (2.0, 0.55), (1.5, 1.75), (1.0, 2.95), (1.5, 2.95), (2.0, 2.95)],
    8: [(1.0, 0.6), (2.0, 0.6), (1.0, 1.4), (2.0, 1.4), (1.0, 2.2), (2.0, 2.2), (1.0, 3.0), (2.0, 3.0)],
    9: [(1.0, 0.6), (2.0, 0.6), (1.0, 1.4), (2.0, 1.4), (1.0, 2.2), (2.0, 2.2), (1.0, 3.0), (2.0, 3.0), (1.5, 1.8)],
}


def tile_face_html(code: str) -> str:
    """返回牌面内部 HTML。"""
    t = classify(code)
    if t.kind == "suited":
        meta = SUIT_META[t.suit]
        if t.suit == "筒":
            # 筒子：画成圆饼。坐标 (col, row)：col 1~2 -> left，row 0.6~3.2 -> top
            dots = DOT_LAYOUT.get(t.rank, [])
            items = []
            for (col, row) in dots:
                left = (col - 0.5) / 2.0 * 100      # col=1 -> 25%, col=2 -> 75%, col=1.5 -> 50%
                top = (row - 0.3) / 3.1 * 100
                items.append(
                    f'<span class="dot" style="left:{left:.1f}%;top:{top:.1f}%"></span>'
                )
            body = '<div class="dots">' + "".join(items) + "</div>"
        elif t.suit == "条":
            # 条子：画成竖条。按「列数」自适应，避免竖条过长被容器裁掉
            n = t.rank
            if n == 1:
                cols, rows = 1, 1
            elif n in (2, 3):
                cols, rows = n, 1
            elif n == 4:
                cols, rows = 2, 2
            elif n == 5:
                cols, rows = 3, 2          # 上 2 下 3
            elif n == 6:
                cols, rows = 3, 2
            elif n == 7:
                cols, rows = 3, 3          # 上 3 中 1 下 3
            elif n == 8:
                cols, rows = 2, 4
            else:                          # 9
                cols, rows = 3, 3

            # 每张牌的竖条布局表：给出 (col_ratio, row_ratio) 列表
            if n == 5:
                pos = [(0.17, 0.28), (0.50, 0.28), (0.83, 0.28),
                       (0.33, 0.72), (0.67, 0.72)]
            elif n == 7:
                pos = [(0.17, 0.18), (0.50, 0.18), (0.83, 0.18),
                       (0.50, 0.50),
                       (0.17, 0.82), (0.50, 0.82), (0.83, 0.82)]
            else:
                pos = []
                for r in range(rows):
                    for c in range(cols):
                        if len(pos) >= n:
                            break
                        cx = (c + 0.5) / cols
                        cy = (r + 0.5) / rows
                        pos.append((cx, cy))
            bar_h = 100.0 / rows * 0.62       # 竖条高度占比，留出间距
            bars = []
            for (cx, cy) in pos[:n]:
                bars.append(
                    f'<span class="bar" style="left:{cx*100:.1f}%;top:{cy*100:.1f}%;'
                    f'height:{bar_h:.1f}%"></span>'
                )
            body = '<div class="bars">' + "".join(bars) + "</div>"
        else:
            # 万子：上面数字，下面「萬」
            body = (f'<div class="wan-num">{t.rank}</div>'
                    f'<div class="wan-char">{SUIT_META["万"]["label"]}</div>')
        return f'<div class="face face-{t.suit}">{body}</div>'

    # 字牌 / 花牌
    label = HONOR_LABEL.get(code, code)
    cls = "honor"
    if code in ("中",):
        cls += " honor-red"
    elif code in ("发",):
        cls += " honor-green"
    elif code in ("白",):
        cls += " honor-white"
    elif code in ("春", "夏", "秋", "冬", "梅", "兰", "竹", "菊"):
        cls += " honor-flower"
    return f'<div class="face {cls}"><span class="honor-char">{label}</span></div>'


CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  background: #1f6b46;
  padding: 26px 22px 30px;
  display: inline-block;
}
.title {
  color: rgba(255,255,255,.92); font-size: 15px; letter-spacing: .08em;
  margin-bottom: 14px; font-weight: 600;
}
.row { display: flex; gap: 8px; align-items: flex-end; flex-wrap: nowrap; }
.tile {
  position: relative;
  width: 62px; height: 86px;
  background: linear-gradient(#fffdf7, #f3ecdc);
  border-radius: 7px;
  box-shadow: 0 2px 0 #d8cfbb, 0 5px 10px rgba(0,0,0,.28);
  border: 1px solid #e2d9c6;
  overflow: hidden;
}
.tile.drawn { margin-left: 16px; }
.tile.gap { margin-left: 10px; }
.face { width: 100%; height: 100%; position: relative; }
/* 筒 */
.dots { position: absolute; inset: 9% 12%; }
.dot {
  position: absolute; width: 21%; aspect-ratio: 1; border-radius: 50%;
  transform: translate(-50%, -50%);
  background: radial-gradient(circle at 32% 30%, #7fb0e0, #2b5f9e 65%, #1d4373);
  box-shadow: inset 0 0 2px rgba(0,0,0,.25);
}
/* 条 */
.bars { position: absolute; inset: 10% 12%; }
.bar {
  position: absolute; width: 13%; border-radius: 3px;
  transform: translate(-50%, -50%);
  background: linear-gradient(90deg, #3d9a67, #276b45 60%, #1c5234);
  box-shadow: inset 0 0 2px rgba(0,0,0,.3);
  min-height: 12%;
}
/* 万 */
.wan-num {
  position: absolute; top: 4%; left: 0; right: 0; text-align: center;
  font-size: 26px; font-weight: 700; color: #b23a2e; line-height: 1.1;
  font-family: Georgia, "Times New Roman", serif;
}
.wan-char {
  position: absolute; bottom: 6%; left: 0; right: 0; text-align: center;
  font-size: 28px; font-weight: 700; color: #b23a2e;
  font-family: "Songti SC", "STSong", serif;
}
/* 字牌 */
.honor { display: flex; align-items: center; justify-content: center; }
.honor-char {
  font-size: 34px; font-weight: 700; color: #2a2a2a;
  font-family: "Songti SC", "STSong", "PingFang SC", serif;
}
.honor-red .honor-char { color: #b23a2e; }
.honor-green .honor-char { color: #1f7a4a; }
.honor-white .honor-char {
  color: transparent;
  border: 2px solid #9aa7b5; border-radius: 3px;
  width: 56%; height: 56%; display: block;
}
.honor-flower .honor-char { color: #6b5a3e; font-size: 28px; }
.legend {
  margin-top: 14px; color: rgba(255,255,255,.62); font-size: 12px; letter-spacing: .04em;
}
"""


def build_html(tiles: list, drawn: list | None = None, title: str = "你的手牌") -> str:
    drawn = drawn or []
    parts = []
    prev = None
    for t in tiles:
        gap = ""
        p = classify(t.code)
        if prev is not None:
            c = classify(t.code)
            # 花色变化处留个缝，方便看
            if (p.suit or p.kind) != (c.suit or c.kind):
                gap = " gap"
        parts.append(f'<div class="tile{gap}">{tile_face_html(t.code)}</div>')
        prev = t

    drawn_html = ""
    for t in drawn:
        drawn_html += f'<div class="tile drawn">{tile_face_html(t.code)}</div>'

    total = len(tiles) + len(drawn)
    legend = f"{title} · 共 {total} 张"
    if drawn:
        legend += "（最右一张是新摸的）"

    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body>
<div class="title">{html.escape(title)}</div>
<div class="row">{''.join(parts)}{drawn_html}</div>
<div class="legend">{html.escape(legend)}</div>
</body></html>"""


def find_chrome() -> str | None:
    cands = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
    ]
    for c in cands:
        if os.path.exists(c):
            return c
    for name in ("google-chrome", "chromium", "chrome", "msedge"):
        p = shutil.which(name)
        if p:
            return p
    return None


def measure_geometry(tiles: list, drawn: list) -> tuple[int, int]:
    """按牌数算出需要的画布尺寸，避免右侧被裁。"""
    TILE_W, GAP, GAP_FAR, PAD_X = 62, 8, 10, 22
    total = len(tiles) + len(drawn)
    if total == 0:
        return 320, 200
    # 花色切换会插入额外间隔，最坏情况每张都切
    width = PAD_X * 2 + total * TILE_W + (total - 1) * GAP + total * GAP_FAR
    if drawn:
        width += 16
    # 用实际的分隔数校准
    actual_gaps = 0
    prev = None
    for t in tiles:
        c = classify(t.code)
        if prev is not None:
            p = classify(prev.code)
            actual_gaps += GAP_FAR if (p.suit or p.kind) != (c.suit or c.kind) else 0
        prev = t
    width = PAD_X * 2 + total * TILE_W + (total - 1) * GAP + actual_gaps + (16 if drawn else 0)
    height = 26 + 16 + 14 + 86 + 14 + 40 + 26   # padding + title + gap + tile + legend + 余量
    return width + 8, height


def render(hand: str, drawn: str | None, out: Path, title: str) -> dict:
    tiles = sorted(parse(hand), key=sort_key)
    drawn_tiles = sorted(parse(drawn), key=sort_key) if drawn else []

    doc = build_html(tiles, drawn_tiles, title)
    html_path = out.with_suffix(".html")
    html_path.write_text(doc, encoding="utf-8")

    chrome = find_chrome()
    if not chrome:
        return {
            "ok": False,
            "html": str(html_path),
            "png": None,
            "error": "没找到 Chrome/Chromium/Edge，只生成了 HTML；可用浏览器打开后截图。",
        }

    w, h = measure_geometry(tiles, drawn_tiles)
    tmp_profile = tempfile.mkdtemp(prefix="mjshot-")
    # file:// URL 必须做百分号编码，否则中文路径 / 全角字符会让 Chrome 报 ERR_INVALID_URL
    file_url = html_path.resolve().as_uri()
    cmd = [
        chrome, "--headless", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--force-device-scale-factor=2",
        f"--user-data-dir={tmp_profile}",
        f"--screenshot={out.resolve()}", f"--window-size={w},{h}",
        file_url,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    shutil.rmtree(tmp_profile, ignore_errors=True)

    if not out.exists():
        return {"ok": False, "html": str(html_path), "png": None,
                "error": (r.stderr or "截图失败")[-400:]}
    return {"ok": True, "html": str(html_path), "png": str(out),
            "count": len(tiles) + len(drawn_tiles)}


def main():
    ap = argparse.ArgumentParser(description="把手牌画成牌面图（纯 HTML/CSS 渲染）")
    ap.add_argument("--hand", required=True, help='手牌，如 "123万 56万 东东东 白白白 8条"')
    ap.add_argument("--drawn", default=None, help="刚摸到的那张，会单独隔开显示")
    ap.add_argument("--out", default="hand.png", help="输出 PNG 路径")
    ap.add_argument("--title", default="你的手牌", help="图片顶部标题")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出结果")
    a = ap.parse_args()

    out = Path(a.out)
    try:
        res = render(a.hand, a.drawn, out, a.title)
    except ValueError as e:
        msg = str(e)
        print(f"⚠️ 没认出牌：{msg}", file=sys.stderr)
        print("   试试这些写法：\"123万 56万 东东东 白白白 8条\" / \"一二三万 五六万 东风\" / \"幺鸡 二饼\"",
              file=sys.stderr)
        if a.json:
            print(json.dumps({"ok": False, "error": msg}, ensure_ascii=False))
        sys.exit(1)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        if res["ok"]:
            print(f"✅ 牌面已生成：{res['png']}（{res['count']} 张）")
            print(f"   可编辑源文件：{res['html']}")
        else:
            print(f"⚠️ {res['error']}", file=sys.stderr)
            print(json.dumps(res, ensure_ascii=False))
            sys.exit(1)


if __name__ == "__main__":
    main()
