#!/usr/bin/env python3
"""
newsletter_assemble.py
Assembles a mixed newsletter from article blocks + listings + images.
Reads /tmp/newsletter_parts/ directory, merges with design tokens,
renders HTML template, outputs /tmp/newsletter_assembled.html
"""

import os, sys, json, re
from datetime import datetime

PARTS_DIR = "/tmp/newsletter_parts"
OUTPUT_FILE = "/tmp/newsletter_assembled.html"
TEMPLATE_FILE = "/root/.openclaw/workspace/skills/journalism-agent/assets/newsletter-template.html"
TOKEN_FILE = "/root/.openclaw/workspace/skills/design-agent/references/design-tokens.md"

def load_parts():
    """Load all part files from /tmp/newsletter_parts/"""
    if not os.path.exists(PARTS_DIR):
        print(f"Error: {PARTS_DIR} not found. Run journalism-agent Writer stage first.")
        sys.exit(1)

    parts = {
        "articles": [],
        "listings": {"bristol": [], "bath": [], "live_music": [], "film": [], "community": []},
        "images": {},
        "sources": [],
    }

    for fname in os.listdir(PARTS_DIR):
        fpath = os.path.join(PARTS_DIR, fname)
        with open(fpath) as f:
            content = f.read().strip()

        if fname.startswith("article_"):
            try:
                data = json.loads(content)
                parts["articles"].append(data)
            except json.JSONDecodeError:
                parts["articles"].append({"html": content, "title": fname})

        elif fname.startswith("listing_"):
            try:
                data = json.loads(content)
                section = data.get("section", "bristol")
                parts["listings"][section].append(data)
            except json.JSONDecodeError:
                pass

        elif fname.startswith("image_"):
            with open(fpath) as f:
                parts["images"][fname] = f.read().strip()

        elif fname == "sources.txt":
            parts["sources"] = [l.strip() for l in content.split("\n") if l.strip()]

    return parts

def render_article(block):
    """Render a single article block to HTML."""
    img_html = ""
    if block.get("image_url"):
        img_html = (
            f'<img class="article-image" src="{block["image_url"]}" '
            f'alt="{block.get("image_alt","")}">'
            f'<p class="article-image-credit">{block.get("image_credit","")}</p>'
        )

    paras = "".join(f"<p>{p}</p>" for p in block.get("paras", []))

    return f"""
<article class="article-block">
  {img_html}
  <h2>{block.get('title','Untitled')}</h2>
  <p class="article-meta">{block.get('byline','')} &nbsp;·&nbsp; {block.get('date','')}</p>
  {paras}
</article>
"""

def render_listing(block):
    """Render a single listing block to HTML."""
    img_html = ""
    if block.get("image_url"):
        img_html = (
            f'<img class="listing-image" src="{block["image_url"]}" '
            f'alt="{block.get("image_alt","")}">'
        )

    venue = block.get("venue", "")
    dt = block.get("datetime", "")
    why = block.get("why", "")

    meta_parts = []
    if venue: meta_parts.append(venue)
    if dt: meta_parts.append(dt)
    meta = " &nbsp;·&nbsp; ".join(meta_parts)

    return f"""
<div class="listing">
  {img_html}
  <h3>{block.get("name","")}</h3>
  {f'<p class="listing-meta">{meta}</p>' if meta else ''}
  <p>{why}</p>
  {f'<p><a href="{block["url"]}">More info →</a></p>' if block.get("url") else ""}
</div>
"""

def build_html(parts, ctx):
    """Render the full HTML newsletter."""
    with open(TEMPLATE_FILE) as f:
        tmpl = f.read()

    # Articles
    articles_html = "\n".join(render_article(a) for a in parts["articles"])
    if articles_html:
        articles_html = f'<div class="section-header">Features</div>\n{articles_html}'

    # Listings by section
    def render_section(key, label):
        items = parts["listings"].get(key, [])
        if not items:
            return ""
        items_html = "\n".join(render_listing(l) for l in items)
        return f'<div class="section-header">{label}</div>\n{items_html}'

    bristol = render_section("bristol", "Bristol")
    bath = render_section("bath", "Bath")
    live_music = render_section("live_music", "Live Music")
    film = render_section("film", "Film & Cinema")
    community = render_section("community", "Community & Learning")

    # Sources
    srcs = ", ".join(f'<a href="{u}">{u[:60]}</a>' for u in parts.get("sources", [])) or "None"

    # Event count
    total = len(parts["articles"]) + sum(len(v) for v in parts["listings"].values())

    # Apply replacements
    replacements = {
        "{{PUBLICATION_NAME}}": ctx.get("publication_name", "Newsletter"),
        "{{TAGLINE}}": ctx.get("tagline", ""),
        "{{DATE}}": ctx.get("date", datetime.utcnow().strftime("%d %B %Y")),
        "{{COMPILED_TIME}}": datetime.utcnow().strftime("%H:%M"),
        "{{EVENT_COUNT}}": str(total),
        "{{FEATURE_ARTICLES}}": articles_html,
        "{{SECTION_BRISTOL}}": "Bristol",
        "{{BRISTOL_LISTINGS}}": bristol,
        "{{SECTION_BATH}}": "Bath",
        "{{BATH_LISTINGS}}": bath,
        "{{SECTION_LIVE_MUSIC}}": "Live Music",
        "{{LIVE_MUSIC}}": live_music,
        "{{SECTION_FILM}}": "Film & Cinema",
        "{{FILM_CINEMA}}": film,
        "{{SECTION_COMMUNITY}}": "Community & Learning",
        "{{COMMUNITY_LEARNING}}": community,
        "{{SOURCES_LIST}}": srcs,
    }

    html = tmpl
    for k, v in replacements.items():
        html = html.replace(k, v)

    # Remove unhandled {{ }} conditionals
    html = re.sub(r"\{\{#if [^}]+\}\}.*?\{\{/if\}\}", "", html, flags=re.DOTALL)
    html = re.sub(r"\{\{[^}]+\}\}", "", html)

    return html

def main():
    if len(sys.argv) > 1:
        ctx_file = sys.argv[1]
        with open(ctx_file) as f:
            ctx = json.load(f)
    else:
        ctx = {
            "publication_name": "The Weekly",
            "tagline": "",
            "date": datetime.utcnow().strftime("%d %B %Y"),
        }

    print(f"[{datetime.now().isoformat()}] Loading parts from {PARTS_DIR}...")
    parts = load_parts()
    print(f"  Articles: {len(parts['articles'])}")
    for sec, items in parts["listings"].items():
        print(f"  Listings [{sec}]: {len(items)}")

    print("Rendering HTML...")
    html = build_html(parts, ctx)

    with open(OUTPUT_FILE, "w") as f:
        f.write(html)

    size = os.path.getsize(OUTPUT_FILE)
    print(f"Done → {OUTPUT_FILE} ({size} bytes)")

if __name__ == "__main__":
    main()
