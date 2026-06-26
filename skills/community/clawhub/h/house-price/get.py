#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抓取查房价（fangjia.fang.com）城市页的新房 / 二手房参考均价、环比同比，以及近月走势折线数据（站内接口）。
用法: python get.py <slug>   例: python get.py cs
     python get.py --url https://fangjia.fang.com/cs/
     python get.py cs --trend-months 6
     python get.py cs --chart
     python get.py cs --chart out.html
     python get.py cs --spark
     python get.py cs --no-svg-stdout
     python get.py cs --no-trend

依赖: pip install requests beautifulsoup4
请遵守站点服务条款，勿高频请求。
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Tuple

# Windows 控制台尽量 UTF-8 输出
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# 页面展示时间为国内习惯，按月对齐用东八区即可（不依赖 tzdata）
CN_TZ = timezone(timedelta(hours=8))

# 与站内走势图一致：二手房 ajaxtrenddata，新房 ajaxtrenddatanew + dataType=4
TREND_ESF = ("ajaxtrenddata", 1, "default")
TREND_XF = ("ajaxtrenddatanew", 4, "defaultnew")


def fetch_html(url: str, timeout: int = 20) -> str:
    r = requests.get(url, headers={"User-Agent": DEFAULT_UA}, timeout=timeout)
    r.raise_for_status()
    # 该站当前为 UTF-8；若异常则回退
    if r.encoding:
        r.encoding = r.apparent_encoding or r.encoding
    text = r.text
    if "title_num" not in text and "gb2312" in (r.headers.get("Content-Type") or "").lower():
        text = r.content.decode("gb18030", errors="replace")
    return text


def parse_cityshort(html: str, fallback_slug: str) -> str:
    m = re.search(r"cityshort\s*=\s*['\"]([^'\"]+)['\"]", html)
    if m:
        return m.group(1).strip().strip("/")
    return fallback_slug.strip().strip("/")


def parse_trend_pairs(raw: str) -> List[Tuple[int, float]]:
    """解析接口返回的 [[ms, price], ...]，其后可有 &yMax&yMin 或 | 第二序列。"""
    raw = (raw or "").strip()
    if not raw:
        return []
    first = raw.split("|", 1)[0]
    arr_blob = first.split("&", 1)[0].strip()
    if not arr_blob.startswith("["):
        return []
    try:
        data = ast.literal_eval(arr_blob)
    except (ValueError, SyntaxError):
        return []
    out: List[Tuple[int, float]] = []
    for item in data:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            try:
                out.append((int(item[0]), float(item[1])))
            except (TypeError, ValueError):
                continue
    return out


def fetch_trend_pairs(
    city_key: str,
    referer: str,
    endpoint: str,
    data_type: int,
    trend_class: str,
    timeout: int = 20,
) -> List[Tuple[int, float]]:
    url = (
        f"https://fangjia.fang.com/fangjia/common/{endpoint}/"
        f"{city_key}?dataType={data_type}&Class={trend_class}"
    )
    r = requests.get(
        url,
        headers={"User-Agent": DEFAULT_UA, "Referer": referer},
        timeout=timeout,
    )
    r.raise_for_status()
    if r.encoding:
        r.encoding = r.apparent_encoding or r.encoding
    return parse_trend_pairs(r.text)


def trim_trend_months(
    pairs: List[Tuple[int, float]], last_n: int
) -> List[Tuple[int, float]]:
    if last_n <= 0 or len(pairs) <= last_n:
        return pairs
    return pairs[-last_n:]


def print_trend_section(title: str, pairs: List[Tuple[int, float]]) -> None:
    print(title + "（按月，元/㎡；与站内折线图同源接口）：")
    if not pairs:
        print("  无")
        return
    for ms, price in pairs:
        ym = datetime.fromtimestamp(ms / 1000, tz=CN_TZ).strftime("%Y-%m")
        print(f"  {ym}：{int(round(price))}")


_SPARK_BARS = "▁▂▃▄▅▆▇█"


def spark_prices_bar(prices: List[float]) -> str:
    """一字一月，纵向仅为相对高低（Unicode），不写文件。"""
    if not prices:
        return "无"
    lo, hi = min(prices), max(prices)
    span = hi - lo or 1.0
    out: list[str] = []
    for p in prices:
        idx = int((float(p) - lo) / span * 7.999)
        out.append(_SPARK_BARS[max(0, min(7, idx))])
    return "".join(out)


def print_spark_lines(
    esf_pts: List[Tuple[int, float]],
    xf_pts: List[Tuple[int, float]],
) -> None:
    print("走势终端示意（可选，一字一月、仅相对高低；非精确作图）：")
    if not esf_pts:
        print("  二手房：无")
    else:
        pr = [p[1] for p in esf_pts]
        lo, hi = int(round(min(pr))), int(round(max(pr)))
        print(f"  二手房：{spark_prices_bar(pr)}  （约 {lo}～{hi} 元/㎡）")
    if not xf_pts:
        print("  新房：无")
    else:
        pr = [p[1] for p in xf_pts]
        lo, hi = int(round(min(pr))), int(round(max(pr)))
        print(f"  新房：{spark_prices_bar(pr)}  （约 {lo}～{hi} 元/㎡）")


def escape_html(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def fetch_both_trends(
    html: str,
    slug: str,
    page_url: str,
    trend_months: int,
) -> Tuple[List[Tuple[int, float]], List[Tuple[int, float]]]:
    city_key = parse_cityshort(html, slug)
    esf_pts: List[Tuple[int, float]] = []
    xf_pts: List[Tuple[int, float]] = []
    try:
        ep, dt, cl = TREND_ESF
        esf_pts = trim_trend_months(
            fetch_trend_pairs(city_key, page_url, ep, dt, cl), trend_months
        )
    except (requests.RequestException, ValueError):
        pass
    try:
        ep, dt, cl = TREND_XF
        xf_pts = trim_trend_months(
            fetch_trend_pairs(city_key, page_url, ep, dt, cl), trend_months
        )
    except (requests.RequestException, ValueError):
        pass
    return esf_pts, xf_pts


def _svg_line_panel(
    title: str,
    pairs: List[Tuple[int, float]],
    stroke: str,
) -> str:
    """单张折线图：viewBox 内坐标，元/㎡。"""
    vb_w, vb_h = 720, 268
    ml, mr, mt, mb = 58.0, 18.0, 42.0, 52.0
    pw = vb_w - ml - mr
    ph = vb_h - mt - mb
    if not pairs:
        return (
            f'<svg viewBox="0 0 {vb_w} {vb_h}" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" aria-label="{escape_html(title)}">'
            f'<text x="24" y="48" fill="#888" font-size="14">{escape_html(title)}：无数据</text>'
            f"</svg>"
        )
    labels = [
        datetime.fromtimestamp(ms / 1000, tz=CN_TZ).strftime("%Y-%m")
        for ms, _ in pairs
    ]
    prices = [float(p[1]) for p in pairs]
    n = len(prices)
    pmin, pmax = min(prices), max(prices)
    span = pmax - pmin
    if span < 1e-6:
        pmin -= 1.0
        pmax += 1.0
        span = pmax - pmin
    pad = span * 0.08
    y_lo, y_hi = pmin - pad, pmax + pad
    y_span = y_hi - y_lo or 1.0

    coords: List[Tuple[float, float]] = []
    for i, pr in enumerate(prices):
        x = ml + (i / max(n - 1, 1)) * pw
        y = mt + ph * (1.0 - (pr - y_lo) / y_span)
        coords.append((x, y))

    pts_attr = " ".join(f"{x:.1f},{y:.1f}" for x, y in coords)

    grid_lines: list[str] = []
    for j in range(5):
        gy = mt + ph * (1.0 - j / 4.0)
        grid_lines.append(
            f'<line x1="{ml:.1f}" y1="{gy:.1f}" x2="{vb_w - mr:.1f}" y2="{gy:.1f}" '
            f'stroke="#eceff1" stroke-width="1"/>'
        )

    y_labels: list[str] = []
    for j in range(5):
        val = y_lo + (y_hi - y_lo) * (1.0 - j / 4.0)
        gy = mt + ph * (1.0 - j / 4.0)
        y_labels.append(
            f'<text x="{ml - 6:.1f}" y="{gy + 4:.1f}" text-anchor="end" '
            f'font-size="11" fill="#78909c">{int(round(val))}</text>'
        )

    step = 1 if n <= 9 else max(1, (n - 1) // 7)
    x_idx = list(range(0, n, step))
    if n > 1 and (n - 1) not in x_idx:
        x_idx.append(n - 1)
    x_labels: list[str] = []
    for i in x_idx:
        x, _y = coords[i]
        x_labels.append(
            f'<text x="{x:.1f}" y="{vb_h - 18:.1f}" text-anchor="middle" '
            f'font-size="10" fill="#78909c" transform="rotate(-40 {x:.1f} {vb_h - 18:.1f})">'
            f"{escape_html(labels[i])}</text>"
        )

    circles = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#fff" stroke="{stroke}" stroke-width="2"/>'
        for x, y in coords
    )

    return (
        f'<svg viewBox="0 0 {vb_w} {vb_h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="{escape_html(title)}">'
        f'<text x="{ml:.1f}" y="{mt - 12:.1f}" font-size="15" font-weight="600" fill="#37474f">'
        f"{escape_html(title)}</text>"
        f'<text x="{ml:.1f}" y="{mt - 2:.1f}" font-size="11" fill="#90a4ae">元/㎡</text>'
        + "".join(grid_lines)
        + f'<line x1="{ml:.1f}" y1="{mt:.1f}" x2="{ml:.1f}" y2="{mt + ph:.1f}" stroke="#cfd8dc" stroke-width="1"/>'
        f'<line x1="{ml:.1f}" y1="{mt + ph:.1f}" x2="{vb_w - mr:.1f}" y2="{mt + ph:.1f}" stroke="#cfd8dc" stroke-width="1"/>'
        + "".join(y_labels)
        + f'<polyline fill="none" stroke="{stroke}" stroke-width="2.5" stroke-linecap="round" '
        f'stroke-linejoin="round" points="{pts_attr}"/>'
        + circles
        + "".join(x_labels)
        + "</svg>"
    )


def build_trend_chart_html(
    city: str,
    slug: str,
    page_url: str,
    esf_pts: List[Tuple[int, float]],
    xf_pts: List[Tuple[int, float]],
) -> str:
    esf_svg = _svg_line_panel("二手房参考均价走势", esf_pts, "#c62828")
    xf_svg = _svg_line_panel("新房参考均价走势", xf_pts, "#00695c")
    esc_city = escape_html(city)
    esc_slug = escape_html(slug)
    esc_url = escape_html(page_url)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>参考均价走势 · {esc_city}</title>
<style>
body {{ font-family: system-ui, "Segoe UI", Roboto, "PingFang SC", sans-serif;
  margin: 0; padding: 24px; background: #f5f5f5; color: #263238; }}
h1 {{ font-size: 1.35rem; font-weight: 600; margin: 0 0 8px; }}
.meta {{ font-size: 14px; color: #546e7a; margin-bottom: 20px; }}
.meta a {{ color: #0277bd; }}
.panel {{ background: #fff; border-radius: 10px; padding: 16px 12px 8px;
  margin-bottom: 18px; box-shadow: 0 1px 3px rgba(0,0,0,.07); }}
.panel svg {{ width: 100%; height: auto; display: block; max-width: 760px; }}
.foot {{ font-size: 13px; color: #78909c; margin-top: 8px; }}
code {{ background: #eceff1; padding: 2px 6px; border-radius: 4px; font-size: 13px; }}
</style>
</head>
<body>
<h1>参考均价走势 · {esc_city}</h1>
<p class="meta"><a href="{esc_url}" target="_blank" rel="noopener">查房价页面</a>
 · slug <code>{esc_slug}</code></p>
<div class="panel">{esf_svg}</div>
<div class="panel">{xf_svg}</div>
<p class="foot">说明：仅供参考，不作购房或投资依据。</p>
</body>
</html>
"""


def year_from_title(soup: BeautifulSoup) -> str:
    t = soup.find("title")
    if t and t.string:
        m = re.search(r"(20\d{2})", t.string)
        if m:
            return m.group(1) + "年"
    return ""


def month_from_block_label(label: str) -> str:
    """如「三月二手房参考均价」→ 三月。"""
    if not label:
        return ""
    m = re.match(r"^([一二三四五六七八九十两]{1,3}月|\d{1,2}月)", label.strip())
    return m.group(1) if m else ""


def change_direction_tag(text: str) -> str:
    """根据页面原文标出涨跌，便于扫读。"""
    if not text or text == "无":
        return ""
    if re.search(r"下跌|下降|降幅|减少|环比.*?跌|比上月.*?跌", text):
        return "跌"
    if re.search(r"上涨|上升|增长|升幅|增加|环比.*?涨|比上月.*?涨", text):
        return "涨"
    if "持平" in text or "不变" in text or "0\.00%" in text:
        return "平"
    return ""


def format_change_line(field_label: str, raw: str) -> str:
    """如：二手房环比上月：【跌】比上月下跌0.22%"""
    if not raw or raw == "无":
        return f"{field_label}：无"
    tag = change_direction_tag(raw)
    if tag:
        return f"{field_label}：【{tag}】{raw}"
    return f"{field_label}：{raw}"


def build_stat_month_line(
    soup: BeautifulSoup, esf: Optional[dict], xf: Optional[dict]
) -> str:
    """合并标题年份与均价块上的「x月」标注。"""
    y = year_from_title(soup)
    mesf = month_from_block_label((esf or {}).get("label", ""))
    mxf = month_from_block_label((xf or {}).get("label", ""))
    parts: list[str] = []
    if y:
        parts.append(y.rstrip("年") + "年" if not y.endswith("年") else y)
    if mesf and mxf and mesf == mxf:
        parts.append(mesf)
        return "".join(parts) + "（二手房、新房参考均价栏目标注）"
    if mesf or mxf:
        head = parts[0] if parts else ""
        bit = []
        if mesf:
            bit.append(f"二手房均价栏「{mesf}」")
        if mxf:
            bit.append(f"新房均价栏「{mxf}」")
        mid = "；".join(bit)
        sep = "；" if head and mid else ""
        return head + sep + mid + "（页面标注）"
    if parts:
        return parts[0] + "（仅标题年份；具体月份见页面）"
    return "无（请打开查房价链接查看页面标注）"


def parse_city_name(soup: BeautifulSoup) -> str:
    t = soup.find("title")
    if t and t.string:
        # 例: 长沙房价_长沙房价走势2026-…查房价网
        m = re.match(r"([^_＿]+)", t.string.strip())
        if m:
            name = m.group(1).strip()
            if name.endswith("房价"):
                name = name[: -len("房价")]
            return name or m.group(1).strip()
    h = soup.find("h1") or soup.find("h2")
    if h:
        return h.get_text(strip=True)[:20]
    return "未知"


def parse_price_blocks(soup: BeautifulSoup) -> List[dict]:
    """每个块: 二手房/新房参考均价 + 元/平 + 后续 li 文案（环比、同比、说明等）。"""
    blocks: List[dict] = []
    for num_li in soup.select("li.title_num"):
        prev = num_li.find_previous_sibling("li")
        if not prev or "title_list" not in (prev.get("class") or []):
            continue
        label = prev.get_text(strip=True)
        span = num_li.find("span")
        price = span.get_text(strip=True) if span else ""
        tail: list[str] = []
        sib = num_li.next_sibling
        while sib is not None:
            if getattr(sib, "name", None) != "li":
                break
            cls = sib.get("class") or []
            if "title_list" in cls or "title_num" in cls:
                break
            txt = sib.get_text(" ", strip=True)
            if txt:
                tail.append(txt)
            sib = sib.next_sibling
        blocks.append({"label": label, "price_yuan_per_ping": price, "tail": tail})
    return blocks


def split_esf_xf(blocks: List[dict]) -> Tuple[Optional[dict], Optional[dict]]:
    esf, xf = None, None
    for b in blocks:
        lab = b.get("label", "")
        if "二手" in lab:
            esf = b
        elif "新房" in lab:
            xf = b
    return esf, xf


def block_to_lines(b: dict | None, prefix: str) -> list[str]:
    if not b:
        out = [
            f"{prefix}参考均价：无",
            f"{prefix}环比上月：无",
        ]
        if prefix == "二手房":
            out.append(f"{prefix}同比去年：无")
        out.append(f"{prefix}数据说明摘要：无")
        return out
    price = b.get("price_yuan_per_ping") or ""
    tail = b.get("tail") or []
    mom, yoy, note = "无", "无", "无"
    for t in tail:
        if "数据说明" in t:
            note = t
            continue
        if prefix == "二手房" and (
            "比去年同期" in t
            or "同比去年" in t
            or "较上年同期" in t
            or (re.search(r"同比", t) and "%" in t)
        ):
            yoy = t
            continue
        if "比上月" in t or ("环比" in t and "%" in t):
            mom = t
            continue
    for t in tail:
        if t == note or "数据说明" in t:
            continue
        if prefix == "二手房" and yoy == "无" and (
            "同比" in t or "去年" in t
        ) and "%" in t:
            yoy = t
        elif mom == "无" and "%" in t:
            mom = t
        elif note == "无" and len(t) > 20:
            note = t
    lines = [
        f"{prefix}参考均价：{price} 元/㎡" if price else f"{prefix}参考均价：无",
        format_change_line(f"{prefix}环比上月", mom),
    ]
    if prefix == "二手房":
        lines.append(format_change_line(f"{prefix}同比去年", yoy))
    lines.append(f"{prefix}数据说明摘要：{note}")
    return lines


def print_report(
    city: str,
    slug: str,
    esf: Optional[dict],
    xf: Optional[dict],
    soup: BeautifulSoup,
    html: str,
    page_url: str,
    include_trend: bool,
    trend_months: int,
    chart_path: Optional[str] = None,
    spark: bool = False,
    svg_stdout: bool = True,
) -> None:
    url = f"https://fangjia.fang.com/{slug.strip('/')}/"
    print("城市：" + city)
    print("查房价链接：" + url)
    print("统计月份或口径：" + build_stat_month_line(soup, esf, xf))
    for line in block_to_lines(esf, "二手房"):
        print(line)
    for line in block_to_lines(xf, "新房"):
        print(line)
    esf_pts: List[Tuple[int, float]] = []
    xf_pts: List[Tuple[int, float]] = []
    if include_trend or chart_path is not None or spark or svg_stdout:
        esf_pts, xf_pts = fetch_both_trends(html, slug, page_url, trend_months)
    if include_trend:
        print_trend_section("二手房参考均价走势", esf_pts)
        print_trend_section("新房参考均价走势", xf_pts)
        if spark:
            print_spark_lines(esf_pts, xf_pts)
    if svg_stdout:
        print("── SVG：二手房参考均价走势 ──")
        print(_svg_line_panel("二手房参考均价走势", esf_pts, "#c62828"))
        print("── SVG：新房参考均价走势 ──")
        print(_svg_line_panel("新房参考均价走势", xf_pts, "#00695c"))
    if chart_path is not None:
        doc = build_trend_chart_html(city, slug, url, esf_pts, xf_pts)
        outp = Path(chart_path)
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(doc, encoding="utf-8")
        print(f"折线图：{outp.resolve()}", file=sys.stderr)
    print("极速 API 补充：无")
    print("说明：仅供参考，不作购房或投资依据。")


def main() -> int:
    ap = argparse.ArgumentParser(description="查房价：拉取城市页新房/二手房参考均价与走势")
    ap.add_argument("slug", nargs="?", help="城市 slug，如 cs、bj、nanjing")
    ap.add_argument("--url", help="完整 URL，如 https://fangjia.fang.com/cs/")
    ap.add_argument(
        "--no-trend",
        action="store_true",
        help="不请求走势接口（仅当前页均价与环比等）",
    )
    ap.add_argument(
        "--trend-months",
        type=int,
        default=0,
        metavar="N",
        help="仅输出走势最近 N 个月（0 表示接口返回的全部月份，通常约 12 个月）",
    )
    ap.add_argument(
        "--chart",
        nargs="?",
        const="",
        default=None,
        metavar="FILE.html",
        help="可选：写出含 SVG 的 HTML 折线图；省略路径时 fangjia_{slug}_trend.html",
    )
    ap.add_argument(
        "--spark",
        action="store_true",
        help="可选：在 stdout 追加 Unicode 走势条（一字一月），不写任何文件",
    )
    ap.add_argument(
        "--no-svg-stdout",
        action="store_true",
        help="关闭默认行为：不向 stdout 输出两段折线 SVG（与 --chart 同源绘图，不写文件）",
    )
    args = ap.parse_args()

    if args.no_trend and (args.chart is not None or args.spark):
        print(
            "error: --chart / --spark 需要按月走势列表，不能与 --no-trend 同用",
            file=sys.stderr,
        )
        return 1

    if args.url:
        u = args.url.strip()
        path = urlparse(u).path.strip("/").split("/")
        slug = path[0] if path and path[0] else ""
        if not slug:
            print("error: 无法从 URL 解析 slug", file=sys.stderr)
            return 1
    elif args.slug:
        slug = args.slug.strip().strip("/")
        u = f"https://fangjia.fang.com/{slug}/"
    else:
        ap.print_help()
        return 1

    try:
        html = fetch_html(u)
    except requests.RequestException as e:
        print("error: 请求失败", e, file=sys.stderr)
        return 1

    soup = BeautifulSoup(html, "html.parser")
    city = parse_city_name(soup)
    blocks = parse_price_blocks(soup)
    esf, xf = split_esf_xf(blocks)

    if not blocks:
        print("城市：" + city)
        print("查房价链接：" + u)
        print("统计月份或口径：无")
        print("二手房参考均价：无")
        print("二手房环比上月：无")
        print("二手房同比去年：无")
        print("二手房数据说明摘要：无")
        print("新房参考均价：无")
        print("新房环比上月：无")
        print("新房数据说明摘要：无")
        print("极速 API 补充：无")
        print("提示：未能解析价格区块，请打开查房价链接查看。")
        return 2

    chart_file: Optional[str] = None
    if args.chart is not None:
        chart_file = args.chart if args.chart else f"fangjia_{slug}_trend.html"

    print_report(
        city,
        slug,
        esf,
        xf,
        soup,
        html,
        u,
        include_trend=not args.no_trend,
        trend_months=max(0, args.trend_months),
        chart_path=chart_file,
        spark=bool(args.spark),
        svg_stdout=not args.no_svg_stdout,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
