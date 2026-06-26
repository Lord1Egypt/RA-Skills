#!/usr/bin/env python3
import argparse
import html
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    from PIL import Image, ImageChops
except Exception:
    Image = None
    ImageChops = None


EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def compress_title(title: str, limit: int = 26) -> str:
    text = " ".join(str(title).replace("\n", " ").split()).strip(" ，、；：,.!?！？-—")
    if not text:
        return "未命名标题"
    if len(text) <= limit:
        return text

    preferred_splits = ["，", "：", "——", " - ", "｜", "|", "？", "！", "。", ":", ","]
    for sep in preferred_splits:
        if sep in text:
            head = text.split(sep)[0].strip(" ，、；：,.!?！？-—")
            if 8 <= len(head) <= limit:
                return head

    soft_cut = text[:limit]
    for sep in ["的", "在", "与", "和", "：", "，", "、", " "]:
        idx = soft_cut.rfind(sep)
        if idx >= max(6, limit // 2):
            candidate = soft_cut[:idx].strip(" ，、；：,.!?！？-—")
            if len(candidate) >= 6:
                return candidate

    return soft_cut.strip(" ，、；：,.!?！？-—")


def normalize_payload(data: dict[str, Any]) -> dict[str, Any]:
    raw_title = str(data.get("title") or "未命名标题")
    payload = {
        "paper_name": str(data.get("paper_name") or "紫音简报"),
        "issue": str(data.get("issue") or "特别刊"),
        "date": str(data.get("date") or ""),
        "title": compress_title(raw_title),
        "subtitle": str(data.get("subtitle") or ""),
        "summary": str(data.get("summary") or ""),
        "highlights": list(data.get("highlights") or []),
        "quote": str(data.get("quote") or ""),
        "sections": list(data.get("sections") or []),
        "footer_note": str(data.get("footer_note") or ""),
    }

    clean_highlights = []
    for item in payload["highlights"]:
        text = str(item).strip()
        if text:
            clean_highlights.append(text)
    payload["highlights"] = clean_highlights[:6]

    clean_sections = []
    for sec in payload["sections"]:
        if not isinstance(sec, dict):
            continue
        heading = str(sec.get("heading") or "未命名版块").strip()
        body = str(sec.get("body") or "").strip()
        bullets = [str(x).strip() for x in (sec.get("bullets") or []) if str(x).strip()]
        clean_sections.append({"heading": heading, "body": body, "bullets": bullets[:8]})
    payload["sections"] = clean_sections[:6]
    return payload


def esc(text: Any) -> str:
    return html.escape(str(text), quote=True)


def paragraphs(text: str) -> str:
    parts = [p.strip() for p in text.split("\n") if p.strip()]
    return "".join(f"<p>{esc(p)}</p>" for p in parts)


def render_section(section: dict[str, Any]) -> str:
    heading = esc(section.get("heading", "未命名版块"))
    body = paragraphs(section.get("body", ""))
    bullets = section.get("bullets") or []
    bullets_html = ""
    if bullets:
        bullets_html = "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in bullets) + "</ul>"
    return f"""
    <section class=\"section-card content-card\" data-kind=\"section\">
      <h2>{heading}</h2>
      {body}
      {bullets_html}
    </section>
    """


def render_highlights_card(highlights: list[str]) -> str:
    if not highlights:
        return ""
    highlights_html = "".join(f"<li>{esc(item)}</li>" for item in highlights)
    return f"""
    <section class=\"side-box content-card\" data-kind=\"highlights\">
      <h3>TL;DR</h3>
      <ul>{highlights_html}</ul>
    </section>
    """


def render_quote_card(quote: str) -> str:
    if not quote:
        return ""
    return f"""
    <section class=\"quote-card content-card\" data-kind=\"quote\">
      <blockquote class=\"quote-box\">“{esc(quote)}”</blockquote>
    </section>
    """


def estimate_section_weight(section: dict[str, Any]) -> float:
    body = str(section.get("body") or "")
    bullets = [str(x) for x in (section.get("bullets") or [])]
    weight = 2.8 + len(body) / 140
    for bullet in bullets:
        weight += 1.2 + len(bullet) / 90
    return weight


def render_float_rail(highlights: list[str], quote: str) -> str:
    rail_parts: list[str] = []
    if highlights:
        rail_parts.append(render_highlights_card(highlights))
    if quote:
        rail_parts.append(render_quote_card(quote))
    if not rail_parts:
        return ""
    return f"""
    <aside class=\"float-rail\">
      {''.join(rail_parts)}
    </aside>
    """


def build_html(payload: dict[str, Any]) -> str:
    highlights = payload.get("highlights") or []
    sections = payload.get("sections") or []
    float_rail_html = render_float_rail(highlights, payload.get("quote") or "")
    sections_html = "".join(render_section(sec) for sec in sections)

    subtitle_html = f'<div class="subtitle">{esc(payload["subtitle"])}</div>' if payload.get("subtitle") else ""
    summary_html = f'<div class="summary">{esc(payload["summary"])}</div>' if payload.get("summary") else ""
    date_text = " · ".join([x for x in [payload.get("issue", ""), payload.get("date", "")] if x])

    return f"""<!DOCTYPE html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{esc(payload['title'])}</title>
  <style>
    :root {{
      --paper: #f6f1e6;
      --ink: #141414;
      --muted: #5d5a53;
      --line: #1d1d1d;
      --soft-line: #c8beb0;
      --accent: #6f5a44;
      --card: rgba(255,255,255,0.28);
      --rail-width: 31%;
      --rail-gap: 24px;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; padding: 0; background: #ddd5c9; color: var(--ink); }}
    body {{
      font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", "Source Han Sans SC", sans-serif;
      display: flex;
      justify-content: center;
      padding: 24px 0;
    }}
    .page {{
      width: 1080px;
      background: linear-gradient(180deg, #f9f5ec 0%, var(--paper) 100%);
      box-shadow: 0 12px 40px rgba(0,0,0,0.12);
      padding: 40px 44px 32px;
      position: relative;
      overflow: hidden;
    }}
    .page::before {{
      content: "";
      position: absolute;
      inset: 0;
      pointer-events: none;
      background-image:
        radial-gradient(rgba(0,0,0,0.028) 0.8px, transparent 0.8px),
        linear-gradient(rgba(255,255,255,0.18), rgba(0,0,0,0));
      background-size: 7px 7px, 100% 100%;
      opacity: 0.6;
    }}
    .topbar {{
      position: relative;
      z-index: 1;
      display: flex;
      justify-content: space-between;
      align-items: end;
      gap: 20px;
      border-top: 6px solid var(--line);
      border-bottom: 2px solid var(--line);
      padding: 12px 0 10px;
      margin-bottom: 22px;
    }}
    .paper-name {{
      font-size: 56px;
      font-weight: 900;
      letter-spacing: 2px;
      line-height: 1;
    }}
    .issue {{
      font-size: 22px;
      color: var(--muted);
      white-space: nowrap;
    }}
    .hero {{ position: relative; z-index: 1; margin-bottom: 24px; }}
    .hero h1 {{
      margin: 0;
      font-size: 64px;
      line-height: 1.08;
      font-weight: 900;
      letter-spacing: -1px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      text-overflow: ellipsis;
      word-break: break-word;
      overflow-wrap: anywhere;
      max-height: calc(2 * 1.08em);
    }}
    .subtitle {{
      margin-top: 14px;
      font-size: 30px;
      line-height: 1.45;
      color: #2d2b28;
      font-weight: 700;
    }}
    .summary {{
      margin-top: 16px;
      font-size: 25px;
      line-height: 1.72;
      color: var(--muted);
      border-left: 8px solid var(--accent);
      padding-left: 18px;
    }}
    .story-wrap {{
      position: relative;
      z-index: 1;
    }}
    .float-rail {{
      float: right;
      width: var(--rail-width);
      min-width: 290px;
      margin: 14px 0 18px var(--rail-gap);
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .story-main {{
      min-width: 0;
    }}
    .story-main::after {{
      content: "";
      display: block;
      clear: both;
    }}
    .content-card {{
      width: 100%;
    }}
    .section-card {{
      border-top: none;
      padding-top: 14px;
      min-width: 0;
      clear: left;
      position: relative;
      width: 100%;
    }}
    .section-card::before {{
      content: "";
      display: block;
      height: 2px;
      width: 100%;
      background: var(--line);
      margin-bottom: 14px;
    }}
    .story-wrap.has-rail .section-card::before {{
      width: calc(100% - var(--rail-width) - var(--rail-gap));
    }}
    .story-wrap.has-rail .section-card.after-rail::before {{
      width: 100%;
    }}
    .section-card[data-kind="section"]:first-child {{
      margin-top: 0;
    }}
    .section-card h2 {{
      margin: 0 0 10px;
      font-size: 34px;
      line-height: 1.2;
      font-weight: 900;
    }}
    .section-card p {{
      margin: 0 0 12px;
      font-size: 25px;
      line-height: 1.78;
      text-align: justify;
    }}
    .section-card ul {{
      margin: 8px 0 0;
      padding-left: 30px;
    }}
    .section-card li {{
      margin: 0 0 10px;
      font-size: 25px;
      line-height: 1.66;
    }}
    .side-box {{
      border: 2px solid var(--line);
      background: var(--card);
      padding: 16px 18px;
      min-width: 0;
    }}
    .side-box h3 {{
      margin: 0 0 12px;
      font-size: 26px;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: 1px;
    }}
    .side-box ul {{ margin: 0; padding-left: 24px; }}
    .side-box li {{ margin: 0 0 10px; font-size: 22px; line-height: 1.6; }}
    .quote-card {{
      background: rgba(17,17,17,0.07);
      padding: 0;
    }}
    .quote-box {{
      margin: 0;
      padding: 20px 18px;
      font-size: 28px;
      line-height: 1.6;
      font-weight: 800;
      border-left: 8px solid var(--line);
      background: rgba(17,17,17,0.07);
    }}
    .footer {{
      position: relative;
      z-index: 1;
      margin-top: 28px;
      padding-top: 12px;
      border-top: 2px solid var(--line);
      font-size: 20px;
      color: var(--muted);
      display: flex;
      justify-content: space-between;
      gap: 16px;
    }}
    .stamp {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 18px;
      font-weight: 800;
      letter-spacing: 1px;
      text-transform: uppercase;
    }}
    .stamp::before {{
      content: "";
      width: 14px;
      height: 14px;
      border-radius: 999px;
      background: var(--line);
      display: inline-block;
    }}
  </style>
</head>
<body>
  <article class=\"page\">
    <header class=\"topbar\">
      <div class=\"paper-name\">{esc(payload['paper_name'])}</div>
      <div class=\"issue\">{esc(date_text)}</div>
    </header>

    <section class=\"hero\">
      <h1>{esc(payload['title'])}</h1>
      {subtitle_html}
      {summary_html}
    </section>

    <section class=\"story-wrap{' has-rail' if float_rail_html else ''}\" id=\"story-wrap\">
      {float_rail_html}
      <div class=\"story-main\" id=\"story-main\">
        {sections_html}
      </div>
    </section>
    <script>
      (() => {{
        const wrap = document.getElementById('story-wrap');
        const rail = wrap?.querySelector('.float-rail');
        const sections = Array.from(wrap?.querySelectorAll('.section-card') || []);
        if (!wrap || !rail || !sections.length) return;

        const apply = () => {{
          const railBottom = rail.offsetTop + rail.offsetHeight;
          for (const sec of sections) {{
            if (sec.offsetTop >= railBottom - 8) {{
              sec.classList.add('after-rail');
            }} else {{
              sec.classList.remove('after-rail');
            }}
          }}
        }};

        if (document.fonts && document.fonts.ready) {{
          document.fonts.ready.then(apply);
        }} else {{
          apply();
        }}
      }})();
    </script>

    <footer class=\"footer\">
      <div>{esc(payload.get('footer_note',''))}</div>
      <div class=\"stamp\">Mobile Brief</div>
    </footer>
  </article>
</body>
</html>
"""


def find_browser() -> str | None:
    env_browser = os.environ.get("NEWSPAPER_BRIEF_BROWSER")
    if env_browser and Path(env_browser).exists():
        return env_browser
    for candidate in EDGE_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    return None


def crop_bottom_whitespace(png_path: Path) -> tuple[bool, str]:
    if Image is None or ImageChops is None:
        return False, "Pillow unavailable"
    try:
        img = Image.open(png_path).convert("RGB")
        bg = Image.new("RGB", img.size, img.getpixel((0, img.height - 1)))
        diff = ImageChops.difference(img, bg)
        bbox = diff.getbbox()
        if not bbox:
            return False, "image is empty"
        left, top, right, bottom = bbox
        pad = 24
        crop_box = (
            max(0, left - pad),
            max(0, top - pad),
            min(img.width, right + pad),
            min(img.height, bottom + pad),
        )
        cropped = img.crop(crop_box)
        cropped.save(png_path)
        return True, f"cropped to {cropped.size[0]}x{cropped.size[1]}"
    except Exception as exc:
        return False, str(exc)


def screenshot_with_browser(html_path: Path, png_path: Path, browser_path: str) -> tuple[bool, str]:
    ensure_parent(png_path)
    file_url = html_path.resolve().as_uri()
    cmd = [
        browser_path,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=2",
        "--window-size=1242,10000",
        f"--screenshot={str(png_path.resolve())}",
        file_url,
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if proc.returncode == 0 and png_path.exists():
            cropped_ok, crop_msg = crop_bottom_whitespace(png_path)
            if cropped_ok:
                return True, crop_msg
            return True, ""
        return False, (proc.stderr or proc.stdout or "headless browser screenshot failed").strip()
    except Exception as exc:
        return False, str(exc)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render newspaper-style mobile HTML and optional PNG.")
    parser.add_argument("--input", required=True, help="Path to input JSON payload.")
    parser.add_argument("--html", required=True, help="Output HTML path.")
    parser.add_argument("--normalized", help="Optional normalized JSON output path.")
    parser.add_argument("--png", help="Optional PNG output path.")
    args = parser.parse_args()

    input_path = Path(args.input)
    html_path = Path(args.html)
    normalized_path = Path(args.normalized) if args.normalized else None
    png_path = Path(args.png) if args.png else None

    with input_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    payload = normalize_payload(raw)
    html_text = build_html(payload)

    ensure_parent(html_path)
    html_path.write_text(html_text, encoding="utf-8")
    print(f"HTML written: {html_path}")

    if normalized_path:
        ensure_parent(normalized_path)
        normalized_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Normalized JSON written: {normalized_path}")

    if png_path:
        browser_path = find_browser()
        if not browser_path:
            print("PNG skipped: no local Edge/Chrome found", file=sys.stderr)
            return 0
        ok, err = screenshot_with_browser(html_path, png_path, browser_path)
        if ok:
            print(f"PNG written: {png_path}")
        else:
            print(f"PNG failed: {err}", file=sys.stderr)
            return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
