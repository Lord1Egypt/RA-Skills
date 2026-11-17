# -*- coding: utf-8 -*-
"""
WeChat CSS Compatibility Converter
==================================
Converts design HTML to WeChat-compatible HTML.

WeChat editor/renderer has limited CSS support:
- Reliable: inline styles, table layout, solid backgrounds, borders,
  font-size, color, line-height, text-align, padding/margin
- Unreliable: display:flex/grid (ignored), linear-gradient (partial loss),
  box-shadow (lost), position (lost)

Conversion rules:
1. display:flex/inline-flex/grid -> table layout
2. linear-gradient -> solid color (first color in gradient)
3. box-shadow -> removed
4. <figure> -> <div>
5. Clean flex-only props (gap/flex-shrink/justify-content/align-items/flex:1)

Usage:
    python wechat_compat.py --src input.html --dst output.html
    python wechat_compat.py --src input.html --dst output.html --verbose
"""
import re
import argparse
from bs4 import BeautifulSoup
from bs4.element import Tag

HEX_RE = re.compile(r"#[0-9A-Fa-f]{3,8}")


def parse_style(s):
    d = {}
    for item in s.split(";"):
        item = item.strip()
        if ":" in item:
            k, v = item.split(":", 1)
            d[k.strip()] = v.strip()
    return d


def dump_style(d):
    parts = []
    seen = set()
    for k, v in d.items():
        if not v or k in seen:
            continue
        seen.add(k)
        parts.append(f"{k}:{v}")
    return ";".join(parts)


def drop_flex_props(d):
    for k in ("gap", "flex-shrink", "justify-content", "align-items",
              "grid-template-columns", "flex-direction"):
        d.pop(k, None)
    d.pop("flex", None)
    d.pop("display", None)
    return d


def convert(src_path: str, dst_path: str, verbose: bool = False) -> dict:
    """Convert HTML to WeChat-compatible format. Returns check report dict."""
    with open(src_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")

    for el in soup.find_all(True):
        style = el.get("style")
        if not style:
            continue
        d = parse_style(style)
        changed = False

        cls = " ".join(el.get("class", []))
        tokens = set(cls.split())

        if "linear-gradient" in d.get("background", ""):
            colors = HEX_RE.findall(d["background"])
            d["background"] = colors[0] if colors else "#F5F0FF"
            changed = True

        if "box-shadow" in d:
            del d["box-shadow"]
            changed = True

        if "num" in cls and "inline-flex" in d.get("display", ""):
            height = d.get("height", "34px")
            d["display"] = "inline-block"
            d["line-height"] = height
            d["text-align"] = "center"
            d["vertical-align"] = "middle"
            d.pop("flex-shrink", None)
            d.pop("align-items", None)
            d.pop("justify-content", None)
            changed = True

        if ("step-num" in cls or "c-badge" in cls) and "flex" in d.get("display", ""):
            height = d.get("height", "32px")
            d["display"] = "inline-block"
            d["line-height"] = height
            d["text-align"] = "center"
            d.pop("flex-shrink", None)
            d.pop("align-items", None)
            d.pop("justify-content", None)
            changed = True

        container_tokens = {"data-grid", "kpis", "step", "check-item", "compare-grid"}
        if not container_tokens & tokens:
            if "flex" in d.get("display", ""):
                d["display"] = "block"
                changed = True

        if changed:
            el["style"] = dump_style(d)

    for el in soup.find_all(True):
        cls = " ".join(el.get("class", []))
        style = el.get("style")
        d = parse_style(style) if style else {}
        tokens = set(cls.split())

        if "data-grid" in tokens or "kpis" in tokens:
            margin = d.get("margin", "14px 8px 20px" if "data-grid" in cls else "10px 0 0")
            cards = [c for c in el.children if isinstance(c, Tag)]
            tr = soup.new_tag("tr")
            for card in cards:
                td = soup.new_tag("td")
                cs = parse_style(card.get("style", ""))
                cs.pop("flex", None)
                cs.pop("box-shadow", None)
                td["style"] = "width:33.3%;vertical-align:top;" + dump_style(cs)
                tr.append(td)
                card.extract()
            el.name = "table"
            el.clear()
            el.append(tr)
            el["style"] = f"width:100%;margin:{margin};border-collapse:separate;border-spacing:8px 0;"
            continue

        if "step" in tokens or "check-item" in tokens:
            keep = {}
            for k in ("padding", "border-bottom", "font-size", "color", "line-height"):
                if k in d:
                    keep[k] = d[k]
            children = [c for c in el.children if isinstance(c, Tag)]
            tr = soup.new_tag("tr")
            badge_td = soup.new_tag("td")
            content_td = soup.new_tag("td")
            if "check-item" in cls:
                badge_td["style"] = "width:38px;vertical-align:middle;"
                content_td["style"] = "vertical-align:middle;"
            else:
                badge_td["style"] = "width:46px;vertical-align:top;"
                content_td["style"] = "vertical-align:top;"
            if children:
                badge_td.append(children[0].extract())
            for c in children[1:]:
                content_td.append(c.extract())
            tr.append(badge_td)
            tr.append(content_td)
            el.name = "table"
            el.clear()
            el.append(tr)
            el["style"] = "width:100%;" + dump_style(keep)
            continue

        if "compare-grid" in tokens:
            drop_flex_props(d)
            el["style"] = dump_style(d)
            continue

        if el.name == "figure":
            el.name = "div"
            continue

        if el.name in ("h1", "h2", "h3", "h4"):
            if "flex" in d.get("display", ""):
                drop_flex_props(d)
                el["style"] = dump_style(d)
            continue

    for el in soup.find_all(True):
        style = el.get("style")
        if not style:
            continue
        d = parse_style(style)
        if "linear-gradient" in d.get("background", ""):
            colors = HEX_RE.findall(d["background"])
            d["background"] = colors[0] if colors else "#F5F0FF"
        d.pop("box-shadow", None)
        if "display" in d and d["display"] in ("flex", "inline-flex"):
            if el.name == "table":
                d.pop("display", None)
            else:
                d["display"] = "block"
        d.pop("grid-template-columns", None)
        el["style"] = dump_style(d)

    with open(dst_path, "w", encoding="utf-8") as f:
        f.write(str(soup))

    with open(dst_path, encoding="utf-8") as f:
        out = f.read()

    checks = {
        "display:flex": out.count("display:flex"),
        "display:inline-flex": out.count("display:inline-flex"),
        "linear-gradient": out.count("linear-gradient"),
        "box-shadow": out.count("box-shadow"),
        "grid-template": out.count("grid-template"),
        "figure_tags": out.count("<figure"),
        "table_tags": out.count("<table"),
        "td_tags": out.count("<td"),
        "img_count": out.count("<img"),
    }

    if verbose:
        print("=== WeChat compat check ===")
        for k, v in checks.items():
            should_be_zero = k in ("display:flex", "display:inline-flex", "linear-gradient", "box-shadow", "grid-template", "figure_tags")
            flag = "OK" if (v == 0 and should_be_zero) or (not should_be_zero) else "FAIL"
            print(f"  [{flag}] {k}: {v}")
        print(f"\nOutput: {dst_path}")

    return checks


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert HTML to WeChat-compatible format")
    parser.add_argument("--src", required=True, help="Source HTML file path")
    parser.add_argument("--dst", required=True, help="Destination HTML file path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print detailed check report")
    args = parser.parse_args()

    result = convert(args.src, args.dst, args.verbose)
    unsafe = sum(v for k, v in result.items() if k in ("display:flex", "display:inline-flex", "linear-gradient", "box-shadow", "grid-template", "figure_tags"))
    if unsafe > 0:
        print(f"WARNING: {unsafe} unsafe CSS properties remain. Review output.")
        sys.exit(1)
    else:
        print(f"OK: All unsafe CSS properties removed. Output: {args.dst}")
