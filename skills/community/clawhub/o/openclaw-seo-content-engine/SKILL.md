---
name: seo-content-engine
description: Research competitors, analyze top-ranking content, and generate a fully SEO-optimized 2000+ word blog post with headings, FAQ, meta description, and internal linking suggestions.
version: 1.0.0
tags: [seo, content, blog, marketing, copywriting]
---

# SEO Content Engine

## Purpose
End-to-end SEO content generation. Takes a target keyword, researches the top competing articles via web search, analyzes their structure and topics, then generates a fully optimized 2000+ word blog post in Markdown — ready to publish.

## Requirements
- Python 3.10+
- `google-generativeai` package (`pip install google-generativeai`)
- Playwright (`pip install playwright`) for competitor research
- Chrome running with remote debugging on port 9222
- `GEMINI_API_KEY` in `/Users/edwin/.openclaw/workspace/dreams-arts/.env`

## Usage

### From Command Line
```bash
python engine.py "best custom printing services near me"
```

### Optional Flags
```bash
--tone "professional, authoritative"   # Writing style (default: "informative, engaging")
--word-count 3000                      # Target word count (default: 2000)
--brand "Dream's Arts Evolution"       # Brand to weave in naturally
--location "Caguas, PR"               # Local SEO focus
--output article.md                    # Save to file (default: stdout)
--skip-research                        # Skip web scraping, use keyword only
```

### From Python
```python
from engine import SEOContentEngine

engine = SEOContentEngine()
article = await engine.generate(
    keyword="custom t-shirt printing Puerto Rico",
    tone="professional",
    brand="Dream's Arts Evolution",
    location="Caguas, PR",
    word_count=2500
)
```

### Output Format
The script outputs a complete Markdown article with YAML frontmatter:

```markdown
---
title: "Custom T-Shirt Printing in Puerto Rico: The Ultimate 2026 Guide"
meta_description: "Looking for custom t-shirt printing in Puerto Rico? Compare top services, prices, and turnaround times. Free quotes from local shops in Caguas, San Juan & more."
target_keyword: "custom t-shirt printing Puerto Rico"
secondary_keywords: ["screen printing PR", "custom apparel Caguas"]
word_count: 2450
reading_time: "10 min"
internal_links_suggested:
  - anchor: "our custom printing services"
    target: "/services/custom-printing"
  - anchor: "request a free quote"
    target: "/contact"
---

# Custom T-Shirt Printing in Puerto Rico: The Ultimate 2026 Guide

## Introduction
...

## What to Look for in a Custom Printing Service
### Quality of Materials
...
### Turnaround Time
...

## Top Custom Printing Methods Compared
...

## Frequently Asked Questions

### How much does custom t-shirt printing cost in Puerto Rico?
...

### What is the minimum order for custom printing?
...
```

## How Claude Should Use This Skill

1. **Identify the keyword**: Extract the target keyword or topic from the user's request.
2. **Run research phase**: Execute `python engine.py "keyword"` — this scrapes Google results and analyzes competitors.
3. **Review the output**: Check that the article is coherent, accurate, and properly optimized.
4. **Customize if needed**: Add brand-specific details, local references, or adjust tone.
5. **Publish**: Copy to CMS, blog platform, or save as file.

## SEO Optimization Checklist (Built-in)
The engine automatically ensures:
- Target keyword in title (H1), first paragraph, and 2-3 H2 headings
- Keyword density between 1-2% (natural, not stuffed)
- LSI (Latent Semantic Indexing) keywords woven throughout
- Meta description under 160 characters with keyword and CTA
- H2/H3 heading hierarchy (no skipping levels)
- FAQ section based on "People Also Ask" data
- Internal linking suggestions with anchor text
- Readability: short paragraphs (2-4 sentences), bullet lists, bold key phrases
- Word count 2000+ (configurable)

## Competitor Research Phase
When `--skip-research` is NOT set, the engine:
1. Searches Google for the target keyword
2. Extracts the top 10 organic results (titles, URLs, snippets)
3. Visits the top 5 articles and extracts their heading structure
4. Identifies content gaps and unique angles
5. Feeds all this context to Gemini for article generation

## Notes
- The research phase requires Chrome on port 9222 with active Google session.
- If research fails (blocked, timeout), falls back to keyword-only generation.
- Articles are generated in English by default; add `--language es` for Spanish.
- Never plagiarizes — all content is original, informed by competitor analysis.
