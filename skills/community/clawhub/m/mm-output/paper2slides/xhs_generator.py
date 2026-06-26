"""
XHS (小红书/RedNote) content generator.
Generates:
  1. XHS-style copywriting via LLM
  2. Mobile-first HTML page with swipeable image carousel
"""
import json
import os
import re
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from openai import OpenAI

from .prompts import XHS_COPYWRITING_PROMPT

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Copywriting generation
# ---------------------------------------------------------------------------

def generate_xhs_copy(
    markdown_text: str,
    model: str = None,
    api_key: str = None,
    base_url: str = None,
) -> Dict[str, Any]:
    """Generate XHS-style titles + body + tags from content.

    Returns:
        {"titles": [...], "body": "...", "tags": [...]}
    """
    model = model or os.getenv("TEXT_MODEL", "qwen3-vl-235b-a22b-instruct")
    client = OpenAI(
        api_key=api_key or os.getenv("OPENAI_API_KEY"),
        base_url=base_url or os.getenv("OPENAI_BASE_URL"),
    )

    summary = markdown_text[:6000]
    prompt = XHS_COPYWRITING_PROMPT.format(summary=summary)

    logger.info("[XHS] Generating copywriting with %s ...", model)
    print("[XHS] Generating 小红书 copywriting...")

    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096,
    )
    raw = resp.choices[0].message.content or ""

    json_match = re.search(r"```json\s*(.*?)\s*```", raw, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        json_match = re.search(r"\{.*\}", raw, re.DOTALL)
        json_str = json_match.group(0) if json_match else "{}"

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        logger.warning("[XHS] Failed to parse JSON, using fallback")
        data = {
            "titles": ["📝 精彩内容速递"],
            "body": raw,
            "tags": ["#知识分享"],
        }

    titles = data.get("titles", ["📝 精彩内容速递"])
    body = data.get("body", "")
    tags = data.get("tags", [])

    logger.info("[XHS] Generated %d titles, body %d chars, %d tags",
                len(titles), len(body), len(tags))
    print(f"[XHS] Generated {len(titles)} titles, body {len(body)} chars")

    return {"titles": titles, "body": body, "tags": tags}


# ---------------------------------------------------------------------------
# XHS HTML generation
# ---------------------------------------------------------------------------

def build_xhs_html(
    image_paths: List[str],
    xhs_copy: Dict[str, Any],
    output_dir: str,
    title_index: int = 0,
) -> str:
    """Build a XHS-style HTML page with swipeable image carousel.

    Args:
        image_paths: List of image file paths (absolute or relative)
        xhs_copy: Output from generate_xhs_copy()
        output_dir: Where to write the HTML
        title_index: Which title to use as the main display title (0-4)

    Returns:
        Path to the generated HTML file.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    html_path = out / "xhs_post.html"

    rel_images = []
    for p in image_paths:
        try:
            rel = os.path.relpath(p, str(out))
        except ValueError:
            rel = p
        rel_images.append(rel)

    title = xhs_copy.get("titles", ["📝"])[title_index % max(len(xhs_copy.get("titles", [""])), 1)]
    all_titles = xhs_copy.get("titles", [])
    body = xhs_copy.get("body", "")
    tags = xhs_copy.get("tags", [])
    num_images = len(rel_images)

    body_html = _body_to_html(body)
    tags_html = " ".join(
        f'<span class="tag">{t}</span>' for t in tags
    )
    titles_html = "\n".join(
        f'            <div class="alt-title">{t}</div>' for t in all_titles
    )

    slides_html = "\n".join(
        f'          <div class="slide"><img src="{img}" alt="slide {i+1}"></div>'
        for i, img in enumerate(rel_images)
    )

    dots_html = "\n".join(
        f'          <span class="dot{" active" if i == 0 else ""}" data-idx="{i}"></span>'
        for i in range(num_images)
    )

    html = _XHS_TEMPLATE.format(
        title=_escape(title),
        slides_html=slides_html,
        dots_html=dots_html,
        num_images=num_images,
        body_html=body_html,
        tags_html=tags_html,
        titles_html=titles_html,
    )

    html_path.write_text(html, encoding="utf-8")
    logger.info("[XHS] HTML saved: %s", html_path)
    print(f"[XHS] HTML saved: {html_path}")
    return str(html_path)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _body_to_html(body: str) -> str:
    paragraphs = [p.strip() for p in body.split("\n") if p.strip()]
    return "\n".join(f"        <p>{_escape(p)}</p>" for p in paragraphs)


# ---------------------------------------------------------------------------
# HTML template — mobile-first XHS style
# ---------------------------------------------------------------------------

_XHS_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>{title}</title>
<style>
  :root {{
    --xhs-red: #ff2442;
    --xhs-bg: #fafafa;
    --xhs-card: #ffffff;
    --xhs-text: #333333;
    --xhs-sub: #999999;
    --xhs-tag: #f0f0f0;
    --radius: 12px;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html {{ font-size: 16px; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", "Microsoft YaHei", sans-serif;
    background: var(--xhs-bg);
    color: var(--xhs-text);
    max-width: 480px;
    margin: 0 auto;
    min-height: 100vh;
    -webkit-font-smoothing: antialiased;
  }}

  /* ---- Carousel ---- */
  .carousel-wrap {{
    position: relative;
    width: 100%;
    background: #000;
    overflow: hidden;
  }}
  .carousel {{
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }}
  .carousel::-webkit-scrollbar {{ display: none; }}
  .slide {{
    flex: 0 0 100%;
    scroll-snap-align: start;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  .slide img {{
    width: 100%;
    height: auto;
    display: block;
    object-fit: contain;
  }}

  /* ---- Counter ---- */
  .counter {{
    position: absolute;
    top: 14px;
    right: 14px;
    background: rgba(0,0,0,.55);
    color: #fff;
    font-size: 12px;
    padding: 3px 10px;
    border-radius: 20px;
    pointer-events: none;
    z-index: 5;
  }}

  /* ---- Dots ---- */
  .dots {{
    display: flex;
    justify-content: center;
    gap: 6px;
    padding: 10px 0 6px;
    background: var(--xhs-card);
  }}
  .dot {{
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #ddd;
    transition: all .3s;
    cursor: pointer;
  }}
  .dot.active {{
    background: var(--xhs-red);
    width: 18px;
    border-radius: 3px;
  }}

  /* ---- Arrows ---- */
  .arrow {{
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 36px; height: 36px;
    background: rgba(255,255,255,.75);
    border: none;
    border-radius: 50%;
    font-size: 18px;
    color: #333;
    cursor: pointer;
    z-index: 5;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity .2s;
  }}
  .carousel-wrap:hover .arrow {{ opacity: 1; }}
  .arrow-left {{ left: 10px; }}
  .arrow-right {{ right: 10px; }}

  /* ---- Content card ---- */
  .content {{
    background: var(--xhs-card);
    padding: 16px 18px 24px;
  }}
  .main-title {{
    font-size: 18px;
    font-weight: 700;
    line-height: 1.5;
    margin-bottom: 12px;
    color: var(--xhs-text);
  }}
  .body p {{
    font-size: 15px;
    line-height: 1.75;
    margin-bottom: 10px;
    color: #444;
  }}
  .tags {{
    margin-top: 14px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }}
  .tag {{
    display: inline-block;
    font-size: 13px;
    color: #4a90d9;
    background: var(--xhs-tag);
    padding: 4px 12px;
    border-radius: 20px;
  }}

  /* ---- Alt titles ---- */
  .alt-titles {{
    padding: 16px 18px;
    background: var(--xhs-card);
    margin-top: 8px;
    border-radius: var(--radius);
  }}
  .alt-titles-label {{
    font-size: 13px;
    color: var(--xhs-sub);
    margin-bottom: 8px;
  }}
  .alt-title {{
    font-size: 14px;
    color: #555;
    padding: 6px 0;
    border-bottom: 1px solid #f5f5f5;
  }}
  .alt-title:last-child {{ border-bottom: none; }}

  /* ---- Footer ---- */
  .footer {{
    text-align: center;
    padding: 20px;
    font-size: 12px;
    color: var(--xhs-sub);
  }}
</style>
</head>
<body>

  <div class="carousel-wrap">
    <div class="counter"><span id="cur">1</span>/{num_images}</div>
    <button class="arrow arrow-left" onclick="go(-1)">‹</button>
    <button class="arrow arrow-right" onclick="go(1)">›</button>
    <div class="carousel" id="carousel">
{slides_html}
    </div>
  </div>

  <div class="dots" id="dots">
{dots_html}
  </div>

  <div class="content">
    <div class="main-title">{title}</div>
    <div class="body">
{body_html}
    </div>
    <div class="tags">
      {tags_html}
    </div>
  </div>

  <div class="alt-titles">
    <div class="alt-titles-label">📌 备选标题</div>
{titles_html}
  </div>

  <div class="footer">Generated by mm-output</div>

<script>
(function() {{
  const carousel = document.getElementById('carousel');
  const dots = document.querySelectorAll('.dot');
  const counter = document.getElementById('cur');
  const total = {num_images};
  let idx = 0;

  function update(i) {{
    idx = Math.max(0, Math.min(i, total - 1));
    carousel.children[idx].scrollIntoView({{ behavior: 'smooth', block: 'nearest', inline: 'start' }});
    dots.forEach((d, j) => d.classList.toggle('active', j === idx));
    counter.textContent = idx + 1;
  }}

  carousel.addEventListener('scroll', function() {{
    const w = carousel.offsetWidth;
    const newIdx = Math.round(carousel.scrollLeft / w);
    if (newIdx !== idx && newIdx >= 0 && newIdx < total) {{
      idx = newIdx;
      dots.forEach((d, j) => d.classList.toggle('active', j === idx));
      counter.textContent = idx + 1;
    }}
  }});

  dots.forEach(d => d.addEventListener('click', function() {{
    update(parseInt(this.dataset.idx));
  }}));

  window.go = function(dir) {{ update(idx + dir); }};

  document.addEventListener('keydown', function(e) {{
    if (e.key === 'ArrowLeft') update(idx - 1);
    if (e.key === 'ArrowRight') update(idx + 1);
  }});
}})();
</script>

</body>
</html>"""
