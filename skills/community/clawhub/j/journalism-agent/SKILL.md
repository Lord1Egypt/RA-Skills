---
name: journalism-agent
description: Multi-stage journalism agent for OpenClaw. Researches, drafts, and edits publication-quality articles. Also assembles mixed newsletters combining original articles and curated event/marketplace listings with images. Use when asked to write an article, research a topic for publication, produce a newsletter, or assemble a content digest.
origin: ECC
---

# Journalism Agent

A 3-stage journalism pipeline: **Searcher → Writer → Editor**, producing either:
- A single longform article (researched, attributed, multi-paragraph)
- A mixed newsletter combining original articles + curated listings/events with images

## Architecture

```
User topic
    │
    ▼
┌─────────────────────────────────────────────┐
│  SEARCHER  (web-search-pro)                  │
│  • Generate 3 search angles per topic       │
│  • Return top URLs per angle               │
│  • Quality gate: NYT-level sources only    │
└─────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────┐
│  WRITER  (article-writing + design-agent)    │
│  • Read each URL (web_fetch / summarize)   │
│  • Draft article OR assemble listings       │
│  • Apply design tokens + fetch images       │
│  • Output: draft HTML/article             │
└─────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────┐
│  EDITOR                                     │
│  • Fact-check claims against sources        │
│  • Enforce voice + structure rules         │
│  • Verify image credits + alt text         │
│  • VLM review loop (canvas snapshot)        │
│  • Final sign-off                          │
└─────────────────────────────────────────────┘
    │
    ▼
Final output
```

## Workflows

### Article Mode

```
User: "Write a 1000-word piece on the future of community libraries"

1. Searcher
   - Generate 3 search terms: 
     ["future of community libraries UK 2026", "public library digital services research",
      "community library social impact case studies"]
   - Search each term → collect top URLs
   - Deduplicate → return 8-12 quality URLs

2. Writer
   - Read top 4 URLs with web_fetch (prioritise gov.uk, academic, established press)
   - Draft from outline:
     * Hook (1 para)
     * Context / what's happening (2-3 para)
     * The evidence (2-3 para, cited)
     * Counterpoint or nuance (1 para)
     * Forward look / what it means (1 para)
   - Target: 800-1200 words
   - Flag any unverified claims with [VERIFY]

3. Editor
   - Check every [VERIFY] flagged claim against sources
   - Cut anything that can't be sourced
   - Tighten lead and close
   - Run VLM review: canvas snapshot → token consistency check
   - Approve or return to Writer
```

### Newsletter Mode (mixed articles + listings)

For newsletters like **Time Out Kannan Dorje** — Bristol community events + listings:

```
1. Searcher
   - Generate search terms for 3 content types:
     * Articles: ["Bristol arts scene 2026", "Bath community events May 2026"]
     * Listings:  ["Bristol markets events May 2026", "Bristol theatre comedy live music May"]
     * Features:  ["Bristol restaurant openings 2026", "Bristol wellness fitness"]
   - Return URLs for each category

2. Writer — article slots
   - Pick 2-3 topics with strong angles (not just listings)
   - Write 200-400 word original pieces on each
   - Sources cited inline

3. Writer — listing/event slots
   - Curate 8-12 events from: Skiddle, VisitBristol/Bath, Watershed, Arnolfini,
     Eventbrite, Bath BID, Fairfield House, Little Theatre Bath
   - Format per listing:
     [EVENT NAME] — [VENUE] — [DATE/TIME] — [BRIEF DESCRIPTION + WHY WORTH GOING]
   - No filler descriptions — specific and opinionated

4. Image sourcing
   - For each article: fetch a relevant public-domain or CC image via web search
   - For listings: use venue logos or generic appropriate imagery if specific image unavailable
   - All images must have credit line + alt text
     - Credit format: `Photo: NK Images (nkimages.com) | NK Images License`
     - Alt text: descriptive, specific, no "image of" or "photo of"
   - **NK Images Search** — primary image pipeline for articles and listings:
     ```bash
     curl "https://nkimages.com/api/public/images?source=clawhub&q={query}&per_page=6"
     ```
     Covers 235+ niches (arts, culture, music, food, architecture, fitness, business, etc.).
     No API key required. Free commercial use. Use `viewUrl` and `downloadUrl` exactly as returned by the API.
     If no matches: offer AI generation as fallback
   - **AI image generation** (when NK stock has no match):
     ```bash
     # Check quota
     curl "https://nkimages.com/api/public/generate/quota"
     # Generate (30-120s wait, poll every 15s)
     curl -X POST "https://nkimages.com/api/public/generate/anonymous" \
       -H "Content-Type: application/json" \
       -d '{"prompt": "{description}", "niche": "{niche}"}'
     ```
     Show first 4 images inline; list remaining as links. Never fabricate URLs.

5. Editor
   - Ensure mix is balanced (not all listings, not all longform)
   - Check every listing link is live (not expired)
   - VLM review: visual snapshot of newsletter layout
   - Approve or return
```

## Output Formats

### Article
- Markdown with YAML frontmatter (title, date, source_urls, word_count)
- Inline citations in brackets [Source: URL]
- `draft` field in frontmatter until Editor approves

### Newsletter
- HTML email-ready document
- Sections clearly labelled: `## Feature`, `## What's On`, `## Listings`
- Images with captions and credits
- Design tokens applied (design-agent called before output)

## Quality Standards

| Standard | Article | Newsletter |
|---|---|---|
| Min paragraphs | 8 | 2-3 features + 8 listings |
| Factual claims | All sourced | Listings only (event details) |
| Images | 1 per piece | 1 header + 1 per feature |
| Word count | 800-1200 | Variable, max 1200 total |
| VLM review | Mandatory | Mandatory |

## Banned Patterns

- Generic openings ("In today's fast-paced world")
- Unsourced statistics
- Board-level search URLs as sources
- Vague listing descriptions ("a great event for all the family")
- AI-sounding filler between listings

## Key Files

| File | Purpose |
|---|---|
| `references/design-tokens.md` | Base tokens (via design-agent) |
| `references/source-quality.md` | What counts as a quality source |
| `assets/newsletter-template.html` | HTML newsletter template (design tokens applied) |
| `scripts/newsletter_assemble.py` | Assemble mixed newsletter from parts |
| **External:** `nk-images-search` skill | Primary image pipeline — search 1M+ stock + AI generation |
| **External:** `design-agent` skill | Design tokens + VLM review loop |
