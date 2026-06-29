#!/usr/bin/env python3
"""
Gxpcode HTML — generate bilingual side-by-side HTML from paddleocr elements + translated text.

Usage:
  python Gxpcode_html.py --elements recognition.json --translated translated.txt --out-dir output/ --title "ISPE Guide"
"""

import html as html_mod, json, sys, re
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")


def preprocess_latex(text: str) -> str:
    """Convert inline LaTeX to HTML/Unicode, eliminating MathJax dependency.

    Two-phase approach:
    1. Match ALL $...$ blocks as complete units (not pattern-by-pattern)
    2. Inside each block: fix paddleocr artifacts → map LaTeX commands → convert ^{}/_{}

    Fixes the root cause where $ m^{3} $, $ \\mu $, $ \\geq $ etc. were silently dropped
    because individual regexes couldn't match content-before-superscript or unknown commands.
    """
    # ── Complete LaTeX math → Unicode mapping ──
    latex_unicode = {
        # Greek lowercase
        r'\alpha': 'α', r'\beta': 'β', r'\gamma': 'γ', r'\delta': 'δ',
        r'\epsilon': 'ε', r'\zeta': 'ζ', r'\eta': 'η', r'\theta': 'θ',
        r'\iota': 'ι', r'\kappa': 'κ', r'\lambda': 'λ', r'\mu': 'μ',
        r'\nu': 'ν', r'\xi': 'ξ', r'\pi': 'π', r'\rho': 'ρ',
        r'\sigma': 'σ', r'\tau': 'τ', r'\upsilon': 'υ', r'\phi': 'φ',
        r'\chi': 'χ', r'\psi': 'ψ', r'\omega': 'ω',
        # Greek uppercase
        r'\Gamma': 'Γ', r'\Delta': 'Δ', r'\Theta': 'Θ', r'\Lambda': 'Λ',
        r'\Xi': 'Ξ', r'\Pi': 'Π', r'\Sigma': 'Σ', r'\Phi': 'Φ',
        r'\Psi': 'Ψ', r'\Omega': 'Ω',
        # Math operators / relations
        r'\geq': '≥', r'\leq': '≤', r'\neq': '≠',
        r'\approx': '≈', r'\equiv': '≡', r'\propto': '∝',
        r'\pm': '±', r'\mp': '∓', r'\times': '×', r'\cdot': '·',
        r'\div': '÷',
        # Arrows
        r'\leftarrow': '←', r'\rightarrow': '→', r'\leftrightarrow': '↔',
        r'\uparrow': '↑', r'\downarrow': '↓',
        r'\Leftarrow': '⇐', r'\Rightarrow': '⇒', r'\Leftrightarrow': '⇔',
        # Brackets
        r'\langle': '⟨', r'\rangle': '⟩',
        # Other symbols
        r'\infty': '∞', r'\partial': '∂', r'\nabla': '∇',
        r'\angle': '∠', r'\degree': '°',
        r'\textregistered': '®', r'\texttrademark': '™',
        r'\circledR': '®', r'\ddagger': '‡', r'\dagger': '†',
        r'\#': '#',
    }
    # Sort by length descending: long commands (e.g. \leftrightarrow) matched before short (e.g. \mu)
    _sorted_cmds = sorted(latex_unicode.keys(), key=len, reverse=True)
    _cmd_pattern = re.compile('|'.join(map(re.escape, _sorted_cmds)))

    def _process_block(m: re.Match) -> str:
        """Process a complete $...$ block: fix artifacts → map commands → convert sup/sub."""
        inner = m.group(1)

        # Fix paddleocr artifact: &gt;/&lt; HTML entities inside $...$
        inner = inner.replace('&gt;', '>').replace('&lt;', '<')

        # Map all LaTeX commands to Unicode in a single pass (longest-first)
        inner = _cmd_pattern.sub(lambda m2: latex_unicode[m2.group(0)], inner)

        # Convert ^{...} → <sup>...</sup>
        inner = re.sub(r'\^\{([^}]*)\}', r'<sup>\1</sup>', inner)

        # Convert _{...} → <sub>...</sub>
        inner = re.sub(r'_\{([^}]*)\}', r'<sub>\1</sub>', inner)

        return inner.strip()

    # Match any $...$ block (non-empty content between $ delimiters)
    text = re.sub(r'\$([^$]+?)\$', _process_block, text)

    # Handle standalone $ (N) $ (USP references without langle/rangle)
    text = re.sub(r'\$\s*\((\d+)\)\s*\$', r'⟨\1⟩', text)

    return text


# ── Risograph CSS ──────────────────────────────────────────────
CSS = """
  :root { --bg: #faf5eb; --card: #ffffff; --text: #3a3226; --accent: #c44f4f; --green: #5b8c5a; --border: #e0d8c8; --muted: #8b7e6a; --sidebar-w: 220px; --header-h: 56px; --disc-h: 38px; }
  *, *::before, *::after { box-sizing: border-box; }
  html { scroll-behavior: smooth; }
  body { margin: 0; padding: 0; font-family: "Microsoft YaHei","\u5fae\u8f6f\u96c5\u9ed1",sans-serif; background: var(--bg); color: var(--text); line-height: 1.75; font-size: 15px; }

  #topbar { position: fixed; top: 0; left: 0; right: 0; z-index: 100; height: var(--header-h); background: var(--card); border-bottom: 1px solid var(--border); display: flex; align-items: center; padding: 0 20px; gap: 14px; }
  #topbar .title { font-weight: 600; flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: var(--accent); }
  #topbar .tag { background: #fdf9f0; border: 1px solid var(--border); padding: 2px 10px; border-radius: 12px; font-size: 0.78em; color: var(--muted); white-space: nowrap; }

  #disclaimer { position: fixed; top: var(--header-h); left: 0; right: 0; z-index: 91; background: #fdf0f0; border-bottom: 1px solid var(--border); padding: 3px 20px; font-size: 0.7em; color: var(--accent); text-align: center; height: var(--disc-h); overflow: hidden; }

  #controls { position: fixed; top: calc(var(--header-h) + var(--disc-h)); left: 0; right: 0; z-index: 90; background: var(--card); border-bottom: 1px solid var(--border); padding: 8px 20px; display: flex; gap: 10px; align-items: center; font-size: 0.86em; overflow-x: auto; white-space: nowrap; }
  /* hide actual radio inputs */
  #controls input[type=radio] { position: absolute; opacity: 0; pointer-events: none; }
  .ctrl-btn { background: var(--card); border: 1px solid var(--border); padding: 4px 12px; border-radius: 6px; cursor: pointer; color: var(--text); font-size: 0.92em; transition: 0.15s; display: inline-block; user-select: none; -webkit-user-select: none; text-decoration: none; }
  .ctrl-btn:hover { border-color: var(--accent); color: var(--accent); }
  /* radio-checked label gets active style */
  input[name=gxp-view]:checked + .ctrl-btn { background: #fdf0f0; border-color: var(--accent); color: var(--accent); }
  input[name=gxp-font]:checked + .ctrl-btn { background: #fdf0f0; border-color: var(--accent); color: var(--accent); }
  /* view-mode CSS-only rules (via :has) */
  body:has(#view-src:checked) .seg .col-zh { display: none; }
  body:has(#view-src:checked) .seg { grid-template-columns: 1fr; }
  body:has(#view-tgt:checked) .seg .col-en { display: none; }
  body:has(#view-tgt:checked) .seg { grid-template-columns: 1fr; }
  /* font-size CSS-only rules */
  body:has(#font-sm:checked) main { font-size: 14px; }
  body:has(#font-lg:checked) main { font-size: 17px; }
  /* TOC checkbox toggle */
  #toc-toggle { position: absolute; opacity: 0; pointer-events: none; }
  #toc-toggle:checked + label { background: #fdf0f0; border-color: var(--accent); color: var(--accent); }
  body:has(#toc-toggle:checked) #sidebar { transform: translateX(0); }
  #controls .sep { width: 1px; height: 18px; background: var(--border); }

  #sidebar { position: fixed; top: calc(var(--header-h) + var(--disc-h) + 42px); bottom: 0; left: 0; width: var(--sidebar-w); background: var(--card); border-right: 1px solid var(--border); overflow-y: auto; padding: 18px 0 30px; z-index: 80; transform: translateX(-100%); transition: transform 0.2s; }
  #toc-details[open] ~ #sidebar { display: block; }
  #toc-details[open] ~ main { margin-left: 0; }
  #sidebar h3 { font-size: 0.78em; text-transform: uppercase; color: var(--muted); margin: 0 0 8px 18px; letter-spacing: 0.05em; }
  #sidebar nav a { display: block; padding: 6px 18px; color: var(--text); text-decoration: none; font-size: 0.9em; border-left: 3px solid transparent; }
  #sidebar nav a:hover { background: #fdf0f0; color: var(--accent); }
  #sidebar nav a.active { background: #fdf0f0; border-left-color: var(--accent); color: var(--accent); font-weight: 600; }

  main { margin-left: var(--sidebar-w); padding: calc(var(--header-h) + var(--disc-h) + 56px) 24px 60px; max-width: 1300px; }

  .header { text-align: center; padding: 32px 20px; margin-bottom: 28px; }
  .header h1 { font-size: 1.6em; color: var(--accent); font-weight: 700; }
  .header .meta { color: var(--muted); font-size: 0.85em; margin-top: 8px; }

  .info-card { background: #fdf9f0; border: 1px solid var(--border); border-radius: 12px; padding: 14px 18px; margin: 24px 0; font-size: 0.92em; }
  .info-card h3 { margin: 0 0 8px; font-size: 1em; color: var(--accent); }


  .card.header-card { background: #c44f4f; color: #fff; border: none; padding: 10px 18px; font-size: 0.85em; font-weight: 600; letter-spacing: 0.5px; border-radius: 12px; margin-bottom: 12px; scroll-margin-top: calc(var(--header-h) + var(--disc-h) + 50px); }
  .card.header-card.green { background: var(--green); }

  .seg { display: grid; grid-template-columns: 1fr 1fr; grid-auto-flow: column; gap: 0; margin-bottom: 14px; background: var(--card); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; scroll-margin-top: calc(var(--header-h) + var(--disc-h) + 50px); position: relative; }
  .seg .col { padding: 14px 18px; font-size: 0.92em; overflow-wrap: break-word; word-break: break-word; min-width: 0; }
  .seg .col-en { grid-column: 1; grid-row: 1; border-right: 1px dashed var(--border); color: #4a4035; font-family: "Segoe UI",Georgia,serif; background: #fefef9; }
  .seg .col-zh { grid-column: 2; grid-row: 1; color: #3a3226; }

  .seg .copy-btn { position: absolute; top: 6px; right: 8px; background: var(--card); border: 1px solid var(--border); border-radius: 4px; padding: 2px 8px; font-size: 0.72em; cursor: pointer; color: var(--muted); opacity: 0; transition: 0.15s; }
  .seg:hover .copy-btn { opacity: 1; }

  body.hide-src .seg { grid-template-columns: 1fr; }
  body.hide-src .seg .col-en { display: none; }
  body.hide-tgt .seg { grid-template-columns: 1fr; }
  body.hide-tgt .seg .col-zh { display: none; }
  body.font-sm { font-size: 14px; }
  body.font-lg { font-size: 17px; }

  .footer { text-align: center; color: var(--muted); font-size: 0.75em; padding: 24px; margin-top: 40px; }

  img { cursor: pointer; transition: 0.15s; touch-action: manipulation; }
  img:hover { opacity: 0.85; }

  #lightbox { opacity: 0; pointer-events: none; display: flex; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.88); z-index: 300; cursor: pointer; align-items: center; justify-content: center; transition: opacity 0.2s; -webkit-tap-highlight-color: transparent; }
  #lightbox.show { opacity: 1; pointer-events: auto; }
  #lightbox img { max-width: 92vw; max-height: 92vh; object-fit: contain; border-radius: 6px; box-shadow: 0 8px 40px rgba(0,0,0,0.6); cursor: default; touch-action: auto; }
  #lightbox img:hover { opacity: 1; }
  #lightbox .lb-close { position: fixed; top: 16px; right: 20px; color: #fff; font-size: 2.5em; z-index: 301; cursor: pointer; opacity: 0.7; transition: 0.15s; line-height: 1; min-width: 44px; min-height: 44px; text-align: center; -webkit-tap-highlight-color: transparent; }
  #lightbox .lb-close:hover { opacity: 1; }

  @media (max-width: 900px) {
    :root { --header-h: 44px; --disc-h: 42px; --ctrl-h: 52px; }
    body { font-size: 14px; }

    #topbar { padding: 0 12px; gap: 8px; }
    #topbar .title { font-size: 0.92em; }
    #topbar .tag { padding: 1px 8px; font-size: 0.72em; }

    #disclaimer { padding: 2px 12px; font-size: 0.68em; }

    #controls { position: fixed; top: auto; bottom: 0; left: 0; right: 0; z-index: 110; min-height: var(--ctrl-h); background: var(--card); border-top: 1px solid var(--border); border-bottom: none; padding: 6px 6px; padding-bottom: max(6px, env(safe-area-inset-bottom)); gap: 4px; font-size: 0.78em; display: flex; flex-wrap: wrap; align-items: center; justify-content: center; touch-action: manipulation; }
    .ctrl-btn { padding: 8px 10px; min-height: 44px; min-width: 44px; font-size: 0.85em; touch-action: manipulation; -webkit-tap-highlight-color: transparent; white-space: nowrap; flex-shrink: 0; cursor: pointer; user-select: none; -webkit-user-select: none; }
    .ctrl-btn:active { background: #fdf0f0; }
    #controls .sep { display: none; }

    #sidebar { transform: translateX(-100%); width: 260px; z-index: 105; }
    body:has(#toc-toggle:checked) #sidebar { transform: translateX(0); position: fixed; top: calc(var(--header-h) + var(--disc-h)); left: 0; bottom: var(--ctrl-h); width: 260px; background: var(--card); border-right: 1px solid var(--border); box-shadow: 2px 0 20px rgba(0,0,0,0.15); overflow-y: auto; padding: 12px 0 20px; }
    #toc-details[open] ~ main { margin-left: 0; }
    #toc-details[open] ~ #sidebar nav a { display: none; }  /* unused, kept for safety */
    main { margin-left: 0; padding: calc(var(--header-h) + var(--disc-h) + 32px) 12px calc(var(--ctrl-h) + 24px); }

    .header { padding: 20px 12px; margin-bottom: 16px; }
    .header h1 { font-size: 1.3em; }

    .seg { grid-template-columns: 1fr; grid-auto-flow: row; touch-action: manipulation; }
    .seg .col-en, .seg .col-zh { grid-column: auto; grid-row: auto; }
    .seg .col { padding: 12px 14px; font-size: 0.88em; }
    .seg .col-en { border-right: none; border-bottom: 1px dashed var(--border); }
    .seg .col-zh { border-bottom: none; }

    .card.header-card { padding: 8px 14px; font-size: 0.8em; }
    .info-card { padding: 10px 14px; margin: 16px 0; font-size: 0.85em; }

    .footer { padding: 16px; font-size: 0.7em; }
  }
"""


def load_elements(path: str) -> dict:
    """Load paddleocr recognition JSON."""
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def load_translated_json(path: str) -> dict:
    """Load element-indexed translated JSON."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def fix_image_paths(text: str, paddleocr_dir: str, html_out_dir: str) -> str:
    """Embed images as base64 data URIs for fully self-contained HTML.
    paddleocr markdown uses src="imgs/xxx.jpg" but actual image is at
    paddleocr/markdown/figures/imgs/xxx.jpg.
    """
    import os, re, base64

    figures_dir = os.path.join(paddleocr_dir, "markdown", "figures")
    if not os.path.isdir(figures_dir):
        return text

    def embed_img(m: re.Match) -> str:
        src = m.group(1)
        img_path = os.path.join(figures_dir, src)
        if os.path.isfile(img_path):
            ext = os.path.splitext(img_path)[1].lower()
            mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "gif": "gif", "webp": "webp"}.get(ext.lstrip("."), "jpeg")
            with open(img_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("ascii")
            return f'src="data:image/{mime};base64,{b64}"'
        return m.group(0)  # keep original if file not found

    return re.sub(r'src="(imgs/[^"]+)"', embed_img, text)


def flatten_elements(data: dict) -> list:
    """Flatten all elements across pages into a single list with page numbers."""
    flat = []
    for page in data.get("pages", []):
        pn = page["page_number"]
        for el in page.get("elements", []):
            flat.append({
                "label": el["label"],
                "text": el["text"],
                "page": pn,
                "reading_order": el.get("reading_order", 0),
            })
    # Sort by page then reading_order
    flat.sort(key=lambda x: (x["page"], x["reading_order"]))
    return flat


def build_zh_lookup(translated_json: dict) -> dict:
    """Build {index: zh_text} lookup from translated.json."""
    return {el["index"]: el["zh"] for el in translated_json.get("elements", [])}


def is_heading(label: str) -> bool:
    return label in ("sec", "sub_sec", "sub_sub_sec")


def heading_level(label: str) -> int:
    return {"sec": 1, "sub_sec": 2, "sub_sub_sec": 3}.get(label, 0)


def build_toc(elements: list) -> list:
    """Extract TOC entries from heading elements."""
    toc = []
    for i, el in enumerate(elements):
        if is_heading(el["label"]):
            toc.append({
                "id": f"sec-{i}",
                "text": el["text"],
                "level": heading_level(el["label"]),
                "element_idx": i,
            })
    return toc


def build_html(data: dict, translated_json: dict, title: str, direction: str = "EN \u2192 ZH", paddleocr_dir: str = "", out_dir: str = "") -> str:
    """Build complete HTML document from element-indexed translations."""
    elements = flatten_elements(data)
    zh_lookup = build_zh_lookup(translated_json)
    total_pages = data.get("total_pages", len(data.get("pages", [])))
    toc = build_toc(elements)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Alignment check
    n = len(elements)
    zh_count = len(zh_lookup)
    mismatch_report = ""
    if zh_count != n:
        gap = n - zh_count
        empty_indices = []
        for i in range(n):
            if i not in zh_lookup or not zh_lookup[i]:
                empty_indices.append(f"[{i}] {elements[i]['text'][:80]}...")
        if empty_indices:
            mismatch_report = f"""<!-- ELEMENT MISMATCH: {zh_count} translations vs {n} elements, gap={gap} -->
<div class="info-card" style="background:#fff0f0; border-color:#c44f4f;">
  <h3>⚠ 段落对齐警告</h3>
  <p>译文条目数 ({zh_count}) ≠ 元素数 ({n})，相差 {abs(gap)} 段。以下元素缺少译文：</p>
  <ol style="font-size:0.85em; max-height:200px; overflow-y:auto;">
""" + "\n".join(f"    <li>{idx}</li>" for idx in empty_indices) + """
  </ol>
  <p style="font-size:0.8em; margin-top:8px;">修复: 重新运行 merge_translations.py。</p>
</div>"""

    # Build TOC nav — visual hierarchy via padding + font size
    toc_html = ""
    for entry in toc:
        lvl = entry["level"]
        pl = 18 + (lvl - 1) * 18   # L1=18px, L2=36px, L3=54px
        fs = 0.9 - (lvl - 1) * 0.06  # L1=0.90em, L2=0.84em, L3=0.78em
        toc_html += f'<a href="#{entry["id"]}" style="padding-left:{pl}px;font-size:{fs}em">{entry["text"]}</a>\n'

    # Build segments
    segs_html = ""
    current_section = None
    section_counter = {}

    for i, el in enumerate(elements):
        zh = zh_lookup.get(i, "")
        en = el["text"]

        # Pre-process LaTeX → HTML (eliminates MathJax dependency)
        en = preprocess_latex(en)
        zh = preprocess_latex(zh)

        # Fix image paths for HTML
        if paddleocr_dir and out_dir:
            en = fix_image_paths(en, paddleocr_dir, out_dir)
            zh = fix_image_paths(zh, paddleocr_dir, out_dir)

        # Image lightbox: inline handler (desktop JS works)
        en = re.sub(r'(<img\s)', r'\1onpointerup="event.stopPropagation();toggleLightbox(this)" ', en)
        zh = re.sub(r'(<img\s)', r'\1onpointerup="event.stopPropagation();toggleLightbox(this)" ', zh)

        if is_heading(el["label"]):
            # Build section number
            lvl = heading_level(el["label"])
            if lvl == 1:
                section_counter = {1: section_counter.get(1, 0) + 1}
                sec_num = str(section_counter[1])
            elif lvl == 2:
                section_counter[2] = section_counter.get(2, 0) + 1
                sec_num = f"{section_counter.get(1,1)}.{section_counter[2]}"
            else:
                section_counter[3] = section_counter.get(3, 0) + 1
                sec_num = f"{section_counter.get(1,1)}.{section_counter.get(2,1)}.{section_counter[3]}"

            card_class = "header-card" if lvl <= 1 else "header-card green"
            segs_html += f'<div class="card {card_class}" id="sec-{i}">\u00a7{sec_num} {en} \u00b7 \u00a7{sec_num} {zh}</div>\n'
        else:
            segs_html += f"""<div class="seg">
  <div class="col col-en">{en}</div>
  <div class="col col-zh">{zh}</div>
  <button class="copy-btn" data-copy="{html_mod.escape(zh).replace('$', '&#36;')}" onclick="var t=this.dataset.copy;navigator.clipboard.writeText(t).then(function(){{this.textContent='\u2713 \u5df2\u590d\u5236';setTimeout(function(){{this.textContent='\u590d\u5236';}}.bind(this),1500);}}.bind(this))">\u590d\u5236</button>
</div>
"""

    html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{CSS}</style>
</head>
<body>
<script>document.write('<div style="position:fixed;top:0;left:0;z-index:99999;background:#5b8c5a;color:#fff;padding:2px 8px;font:10px monospace;">JS:ON</div>');</script>

<!-- Hidden radio controls for CSS-only view/font switching -->
<input type="radio" name="gxp-view" id="view-dual" checked>
<input type="radio" name="gxp-view" id="view-src">
<input type="radio" name="gxp-view" id="view-tgt">
<input type="radio" name="gxp-font" id="font-sm">
<input type="radio" name="gxp-font" id="font-md" checked>
<input type="radio" name="gxp-font" id="font-lg">
{mismatch_report}
<div id="topbar">
  <span class="title">{title}</span>
  <span class="tag">{direction}</span>
  <span class="tag">{total_pages} \u9875</span>
  <span class="tag">{ts}</span>
</div>

<div id="disclaimer">Gxpcode \u4ec5\u63d0\u4f9b\u4e13\u4e1a\u7ffb\u8bd1\u5de5\u5177\uff0c\u4e0d\u5bf9\u7ffb\u8bd1\u5185\u5bb9\u505a\u4efb\u4f55\u4fdd\u8bc1\u4e0e\u8d1f\u8d23<br>\u5982\u5bf9\u7ffb\u8bd1\u6587\u6863\u6709\u9690\u79c1\u8981\u6c42\uff0c\u53ef\u8054\u7cfb Gxpcode \u63d0\u4f9b\u672c\u5730\u5316\u79c1\u6709\u90e8\u7f72\u65b9\u6848</div>

<div id="controls">
  <input type="radio" name="gxp-view" id="view-dual" checked>
  <label class="ctrl-btn" for="view-dual">\u53cc\u680f</label>
  <input type="radio" name="gxp-view" id="view-src">
  <label class="ctrl-btn" for="view-src">\u4ec5\u539f\u6587</label>
  <input type="radio" name="gxp-view" id="view-tgt">
  <label class="ctrl-btn" for="view-tgt">\u4ec5\u8bd1\u6587</label>
  <span class="sep"></span>
  <input type="checkbox" id="toc-toggle" tabindex="-1">
  <label class="ctrl-btn" for="toc-toggle">\u76ee\u5f55</label>
  <span class="sep"></span>
  <input type="radio" name="gxp-font" id="font-sm">
  <label class="ctrl-btn" for="font-sm">\u5c0f</label>
  <input type="radio" name="gxp-font" id="font-md" checked>
  <label class="ctrl-btn" for="font-md">\u4e2d</label>
  <input type="radio" name="gxp-font" id="font-lg">
  <label class="ctrl-btn" for="font-lg">\u5927</label>
</div>

<div id="sidebar">
  <h3>\u76ee\u5f55</h3>
  <nav>{toc_html}</nav>
</div>

<main>
<div class="header">
  <h1>{title}</h1>
  <div class="meta">{direction} | {total_pages} \u9875 | {ts}</div>
</div>

<div class="info-card">
  <h3>\u4f7f\u7528\u8bf4\u660e</h3>
  <ul>
    <li>\u53cc\u680f\u5bf9\u7167\uff1a\u5de6\u5217\u539f\u6587\uff08EN\uff09\uff0c\u53f3\u5217\u8bd1\u6587\uff08ZH\uff09</li>
    <li>\u60ac\u505c\u6bb5\u843d\u53ef\u590d\u5236\u8bd1\u6587</li>
    <li>\u9876\u90e8\u63a7\u5236\u680f\u53ef\u5207\u6362\u89c6\u56fe\u548c\u5b57\u53f7</li>
    <li>\u5de6\u4fa7\u76ee\u5f55\u6eda\u52a8\u8054\u52a8</li>
  </ul>
</div>

{segs_html}
</main>

<div class="footer">Gxpcode-translator \u00b7 \u5236\u836f\u4e13\u4e1a\u7ffb\u8bd1 \u00b7 \u53cc\u8bed\u5bf9\u7167</div>

<div id="lightbox"><span class="lb-close">&times;</span><img id="lightbox-img" src="" alt=""></div>

<script>
(function(){{
  try {{
    // Diagnostic
    var d = document.querySelector('#js-ok') || document.getElementById('js-ok');
    if (d) {{ d.style.color = '#5b8c5a'; d.title = 'JS OK'; }}

    // Lightbox functions
    window.toggleLightbox = function(el) {{
      var lb = document.getElementById('lightbox');
      if (lb.classList.contains('show')) {{
        lb.classList.remove('show');
      }} else {{
        var img = document.getElementById('lightbox-img');
        if (img && el && el.src) img.src = el.src;
        lb.classList.add('show');
      }}
    }};
    window.closeLightbox = function() {{
      document.getElementById('lightbox').classList.remove('show');
    }};

    // Lightbox event listeners
    var lb = document.getElementById('lightbox');
    var lbClose = document.querySelector('.lb-close');
    var lbImg = document.getElementById('lightbox-img');
    if (lb) lb.addEventListener('click', function(e) {{ if (e.target===lb) closeLightbox(); }});
    if (lbClose) lbClose.addEventListener('click', function(e) {{ e.stopPropagation(); closeLightbox(); }});
    if (lbImg) lbImg.addEventListener('click', function(e) {{ e.stopPropagation(); closeLightbox(); }});
  }} catch(e) {{ console.error(e); }}
}})();
</script>

</body>
</html>"""

    return html


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate Gxpcode bilingual HTML")
    parser.add_argument("--elements", type=str, required=True, help="PaddleOCR recognition JSON path")
    parser.add_argument("--translated", type=str, required=True, help="Translated text file path")
    parser.add_argument("--out-dir", type=str, required=True, help="Output directory")
    parser.add_argument("--title", type=str, default="Gxpcode Translation", help="Document title")
    parser.add_argument("--direction", type=str, default="EN \u2192 ZH", help="Translation direction")
    parser.add_argument("--paddleocr-dir", type=str, default="", help="PaddleOCR output directory (for image path fixing)")
    args = parser.parse_args()

    data = load_elements(args.elements)
    translated_json = load_translated_json(args.translated)

    out_dir = Path(args.out_dir)
    html = build_html(data, translated_json, args.title, args.direction,
                      paddleocr_dir=args.paddleocr_dir, out_dir=str(out_dir))

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    import re
    safe_title = re.sub(r'[\\/*?:"<>|]', '', args.title).replace(' ', '_')[:80]
    out_path = out_dir / f"Gxpcode-{safe_title}.html"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Gxpcode-{safe_title}.html written to {out_path}")


if __name__ == "__main__":
    main()
