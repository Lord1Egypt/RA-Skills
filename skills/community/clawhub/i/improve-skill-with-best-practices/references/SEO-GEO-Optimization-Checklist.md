# SEO & GEO Optimization Checklist

> **Purpose**: Reference document for the AI agent to audit any website's SEO (Search Engine Optimization) and GEO (Generative Engine Optimization) readiness.
> **Core principle**: SEO optimizes rankings; GEO optimizes AI citations. They are complementary, not competing.
> **Variable**: All commands below use `$SITE_URL` — the target website URL from `.env`.

---

## Table of Contents

- [1. Structured Data (JSON-LD)](#1-structured-data-json-ld)
- [2. AI Readability (GEO Core)](#2-ai-readability-geo-core)
- [3. Page Content Depth](#3-page-content-depth)
- [4. Technical SEO Basics](#4-technical-seo-basics)
- [5. Page Performance](#5-page-performance)
- [6. Off-page Authority Building](#6-off-page-authority-building)
- [7. Detection Commands](#7-detection-commands)
- [8. Priority Overview](#8-priority-overview)

---

## 1. Structured Data (JSON-LD)

### 1.1 Recommended JSON-LD Types

Select the types applicable to the target site. Not every site needs all types — choose based on site category.

| @type | Applicable Pages | Purpose | Check Points |
|-------|-----------------|---------|-------------|
| **WebSite** | All pages | Site-wide info with search box | Localize for each language version |
| **Organization** | All pages | Organization info (name, logo, contact) | `inLanguage` must match page language |
| **WebPage** | All pages | Current page info | Include `speakable` (voice search) and `dateModified` |
| **BreadcrumbList** | All pages | Breadcrumb navigation | Multi-level paths, e.g. `Home > Category > Page` |
| **SoftwareApplication** | Tool/product pages | Tool/product description | Each page must have unique content, not templated |
| **FAQPage** | Content/tool pages | FAQ section | 3-5 targeted Q&As matching user search intent per page |
| **ItemList** | Category/listing pages | List items in a category | Helps search engines understand page hierarchy |
| **HowTo** | Tutorial/tool pages | Step-by-step guide | 3-5 steps; can trigger Google rich snippets |
| **Article** | Blog/article pages | Article metadata | Include author, datePublished, dateModified |
| **Product** | E-commerce pages | Product info | Include price, availability, reviews |
| **LocalBusiness** | Local business sites | Location info | Include address, hours, phone |

### 1.2 Checklist

- [ ] **Coverage**: All indexable pages have at least WebSite + WebPage + BreadcrumbList JSON-LD
- [ ] **SSR output**: JSON-LD is rendered server-side in the HTML (some crawlers don't execute JS)
- [ ] **Content uniqueness**: Each page has distinct `name`, `description`, and FAQ content
- [ ] **Localization**: Multi-language sites have localized JSON-LD for each language version
- [ ] **Language tag**: `inLanguage` field is correct (e.g. `en-US`, `zh-CN`)
- [ ] **URL consistency**: `url` in JSON-LD matches the canonical URL

### 1.3 Common Pitfalls

| Problem | Symptom | Solution |
|---------|---------|---------|
| SSR empty shell | Page returns `<meta http-equiv="refresh">` self-redirect with no real content | Check SSG/SSR pre-rendering config (Nuxt/Next/Astro), ensure routes are correctly built |
| Trailing slash mismatch | `/page` returns 301 → `/page/`, causing crawl issues | Unify URL format; use `curl -sL` (follow redirects) when testing |
| Unlocalized JSON-LD | Non-English pages still have English WebSite/Organization | Configure localized JSON-LD blocks for each language in i18n setup |
| Duplicate content | Multiple pages share identical JSON-LD name/description | Generate page-specific structured data from actual page content |

---

## 2. AI Readability (GEO Core)

### 2.1 llms.txt File (P0 — Must Do)

> `llms.txt` is a standard proposed by Jeremy Howard in 2024, adopted by Anthropic, Mintlify and others. It provides AI crawlers with a curated site map.

- [ ] **`/llms.txt`**: Summary version — site overview + categorized page list with links and one-line descriptions
- [ ] **`/llms-full.txt`**: Full version — each page with URL + detailed description + use cases + technical details
- [ ] **robots.txt reference**: Add `Llms-txt: https://yoursite.com/llms.txt` at the end of robots.txt

**llms.txt template**:

```markdown
# Site Name

> One-line description of the site's purpose and core value

- Key feature 1
- Key feature 2
- Site URL

## Category 1
- [Page Name](URL): One-line description

## Category 2
- [Page Name](URL): One-line description

## Optional
- [Secondary Content](URL): Description
```

**llms-full.txt template**:

```markdown
# Site Name — Complete Reference

> Detailed description

## Overview
- Total pages/tools, privacy model, tech stack, supported languages, etc.

## Category (N items)

### Page/Tool Name
- **URL**: https://...
- **Description**: Detailed description (include technical details)
- **Use cases**: Usage scenario list

## Technical Details
- Tech stack, processing methods, i18n, SEO config, etc.

## Contact
- Contact info
```

### 2.2 robots.txt AI Crawler Configuration

- [ ] Explicitly allow major AI crawlers (global + China):

```
# --- Global AI Crawlers ---
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

# --- Chinese AI Crawlers ---
User-agent: Bytespider
Allow: /

User-agent: Doubaobot
Allow: /

User-agent: ERNIEBot
Allow: /

User-agent: Baiduspider
Allow: /

User-agent: DeepSeekBot
Allow: /

User-agent: QwenBot
Allow: /

User-agent: TongyiBot
Allow: /
```

| Crawler | Company | AI Product |
|---------|---------|------------|
| GPTBot / ChatGPT-User | OpenAI | ChatGPT, GPT Search |
| ClaudeBot / anthropic-ai | Anthropic | Claude |
| PerplexityBot | Perplexity | Perplexity AI Search |
| Google-Extended | Google | Gemini, AI Overviews |
| Bytespider / Doubaobot | ByteDance | Doubao (豆包) |
| ERNIEBot / Baiduspider | Baidu | ERNIE Bot (文心一言) |
| DeepSeekBot | DeepSeek | DeepSeek |
| QwenBot / TongyiBot | Alibaba | Qwen / Tongyi Qianwen (通义千问) |

- [ ] Avoid over-restriction: A single `Allow: /` per bot is sufficient
- [ ] Note: ByteSpider has aggressive crawl rates — if bandwidth is a concern, consider adding `Crawl-delay` or rate-limiting at the server level rather than blocking entirely

### 2.3 H2/H3 Heading Format (Question-style)

> AI engines pattern-match headings against user queries. Question-style headings are cited far more often than declarative ones.

- [ ] Convert declarative headings to question format:

| ❌ Declarative | ✅ Question-style |
|---------------|------------------|
| `Features` | `What Makes This Tool Different?` |
| `Getting Started` | `How to Get Started with [Product]?` |
| `Pricing` | `How Much Does [Product] Cost?` |
| `Related Tools` | `What Other Tools Are Available?` |

### 2.4 HowTo Schema + Visible Step Content

- [ ] Pages with tutorials or workflows should have `HowTo` JSON-LD (3-5 steps)
- [ ] Steps must also be **visually present** on the page (not just in JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to [Action]",
  "step": [
    {"@type": "HowToStep", "position": 1, "name": "Step 1 Title", "text": "Step 1 description..."},
    {"@type": "HowToStep", "position": 2, "name": "Step 2 Title", "text": "Step 2 description..."},
    {"@type": "HowToStep", "position": 3, "name": "Step 3 Title", "text": "Step 3 description..."}
  ]
}
```

---

## 3. Page Content Depth

### 3.1 Word Count Targets

> 2026 GEO research consistently shows: AI engines prefer reference-grade content. Content with statistics and cited sources gets 30-40% more AI citations.

- [ ] Target per key page (excluding navigation and footer):

| Language | Metric | Target | Notes |
|----------|--------|--------|-------|
| English | Words (space-separated) | **800-1200** | Standard GEO recommendation |
| Chinese | Characters (CJK codepoints) | **1600-2400** | ~2 Chinese chars ≈ 1 English word in information density |

> **Why separate thresholds?** Chinese text has no spaces between words. Counting by `split()` on Chinese content returns near-zero, severely underestimating actual content depth. Always use **CJK character count** for Chinese pages.

- [ ] Detection method: see [Detection Commands](#7-detection-commands) — the script auto-detects language and reports both metrics

### 3.2 Recommended Content Structure

| Content Block | Description | Target Words |
|--------------|-------------|:----------:|
| **Intro Summary** | Top of page (between H1 and first H2) — directly answers "what is this, what does it do" | 100 |
| **How to Use** | 3-5 step guide, paired with HowTo Schema | 200 |
| **Technical Details** | Technical principles (algorithms, architecture, privacy model) | 200 |
| **Use Cases / Scenarios** | Usage scenarios: "ideal for designers", "perfect for developers" | 150 |
| **Comparison** | Competitive comparison (features, pros/cons) | 150 |
| **FAQ** | 3-5 targeted questions matching user search intent | 200 |

### 3.3 Key Principles

- [ ] **First 200 words must directly answer the core question** (intro-summary-first principle)
- [ ] One deep guide > ten shallow pages
- [ ] Include specific data and cited sources (e.g. "reduces size by 70%", "based on WebAssembly")
- [ ] Avoid pure feature lists — add explanatory content

---

## 4. Technical SEO Basics

### 4.1 Meta Tags

- [ ] **title**: 50-60 characters, include core keyword, avoid truncation
- [ ] **description**: 150-160 characters, include call to action
- [ ] **canonical**: Every page has a unique canonical URL
- [ ] **hreflang**: Multi-language pages correctly configured (`<link rel="alternate" hreflang="zh" href="...">`)

### 4.2 Open Graph & Social

- [ ] **og:title**: Unique per page
- [ ] **og:description**: Unique per page
- [ ] **og:image**: Each page uses a distinct social share image (with page title and brief description)
- [ ] **Twitter Card**: Correctly set `twitter:card`, `twitter:title`, etc.

### 4.3 Sitemap

- [ ] sitemap.xml includes all indexable pages (separate by language if multi-language)
- [ ] Each URL has a `<lastmod>` date
- [ ] Sitemap declared in robots.txt

### 4.4 URL Structure

- [ ] Consistent trailing slash strategy (recommend always with `/`)
- [ ] URLs use lowercase English with hyphens
- [ ] Avoid deep nesting (recommend no more than 3 levels)

### 4.5 Security & Trust

- [ ] **HSTS Header**: `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- [ ] **HTTPS**: Enforced site-wide
- [ ] These factors affect E-E-A-T trust scores

### 4.6 Content Freshness

- [ ] Page displays a **visible** `Last Updated` date (not just in JSON-LD)
- [ ] `dateModified` in JSON-LD matches the actual update date

### 4.7 IndexNow

- [ ] Integrate IndexNow protocol (supported by Bing/Yandex)
- [ ] Automatically notify search engines on content updates for faster indexing

---

## 5. Page Performance

### 5.1 Loading Speed

> 2026 GEO research: Pages with FCP < 0.4s average 6.7 AI citations; pages > 1.13s average only 2.1. Fast pages are cited 3x more.

- [ ] **FCP (First Contentful Paint)**: Target < 0.4s
- [ ] **TLS optimization**: Enable OCSP Stapling, stable TLS Session Ticket reuse
- [ ] **Compression**: Enable Brotli compression (better than gzip)
- [ ] **CDN**: Use CDN for static assets (e.g. CloudFlare, Fastly)
- [ ] **HTML size**: Keep under 100KB, consider code splitting

### 5.2 Detection Method

```bash
# Page load time
curl -sL -o /dev/null -w "Total: %{time_total}s\nTLS: %{time_appconnect}s\nFCP proxy: %{time_starttransfer}s\n" "$SITE_URL/"

# Compression check
curl -sI -H "Accept-Encoding: gzip, br" "$SITE_URL/" | grep -i 'content-encoding'
```

---

## 6. Off-page Authority Building

> Research shows brands are cited by AI engines via third-party domains 6.5x more often than via their own domain.

### 6.1 Platform Presence

- [ ] **Product Hunt**: Publish a product page
- [ ] **AlternativeTo**: Create an entry benchmarked against competitors
- [ ] **Reddit**: Share in relevant subreddits (r/webdev, r/SideProject, etc.)
- [ ] **GitHub**: Open-source part of the code, link back in README
- [ ] **Wikidata**: Create a product entity
- [ ] **Industry directories**: Submit to relevant niche directories

### 6.2 Comparison Content Pages

> AI search queries average 23 words — much longer than traditional search — and often contain comparison intent.

- [ ] Create `vs` comparison pages (e.g. `/product-vs-competitor/`)
- [ ] Include feature comparison tables and pros/cons analysis

### 6.3 Multi-modal Optimization

- [ ] Add tutorial videos to key pages (YouTube embed + text transcript)
- [ ] All images have descriptive alt text
- [ ] Add `VideoObject` Schema when videos are present

---

## 7. Detection Commands

All audit scripts live in `scripts/` and accept the same core arguments. They use `$SITE_URL` from `.env` or `--url`.

> All example commands below assume the venv has been activated: `source "$DATA_DIR/venv/bin/activate"`

### 7.1 SEO Audit (`seo_audit.py`)

Covers: JSON-LD coverage, meta tags, headings, og:image, canonical, hreflang, SSR empty-shell detection, sitemap, HowTo/FAQ schema.

```bash
# Homepage only
python scripts/seo_audit.py --url "$SITE_URL"

# Specific pages
python scripts/seo_audit.py --url "$SITE_URL" --pages "/,/about,/pricing"

# Full-site audit via sitemap (JSON-LD + meta per page)
python scripts/seo_audit.py --url "$SITE_URL" --sitemap

# Save results to file
python scripts/seo_audit.py --url "$SITE_URL" --sitemap -o data/seo_audit.json
```

### 7.2 GEO Audit (`geo_audit.py`)

Covers: llms.txt / llms-full.txt, robots.txt AI crawler rules, content depth (auto-detects CJK vs English, see [3.1](#31-word-count-targets)), intro summary detection, FAQ/HowTo sections, question-style headings.

```bash
# Homepage only
python scripts/geo_audit.py --url "$SITE_URL"

# Specific pages
python scripts/geo_audit.py --url "$SITE_URL" --pages "/,/blog/my-post"

# Full-site audit via sitemap (max 50 pages)
python scripts/geo_audit.py --url "$SITE_URL" --sitemap

# Save results to file
python scripts/geo_audit.py --url "$SITE_URL" --sitemap -o data/geo_audit.json
```

### 7.3 Performance & Security Audit (`perf_audit.py`)

Covers: load time (TTFB, total), compression (Brotli/gzip), HTML size, HSTS, HTTPS/TLS version, cache headers, CSP, X-Frame-Options, CDN detection.

```bash
# Homepage only
python scripts/perf_audit.py --url "$SITE_URL"

# Specific pages
python scripts/perf_audit.py --url "$SITE_URL" --pages "/,/about"

# Full-site via sitemap (max 20 pages)
python scripts/perf_audit.py --url "$SITE_URL" --sitemap

# Save results to file
python scripts/perf_audit.py --url "$SITE_URL" --sitemap -o data/perf_audit.json
```

### 7.4 Run All Audits

```bash
python scripts/seo_audit.py  --url "$SITE_URL" --sitemap -o data/seo_audit.json
python scripts/geo_audit.py  --url "$SITE_URL" --sitemap -o data/geo_audit.json
python scripts/perf_audit.py --url "$SITE_URL" --sitemap -o data/perf_audit.json
```

---

## 8. Priority Overview

When generating the SEO/GEO audit section of the improvement report, use this priority matrix to classify findings:

```
Priority    Item                                    Impact    Effort   Est. Time
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
P0 🔴   JSON-LD site-wide coverage + SSR output      ★★★★★   ★★★     1-2 days
P0 🔴   Add llms.txt + llms-full.txt                 ★★★★★   ★☆☆     1 hour
P0 🔴   Increase page content depth                  ★★★★★   ★★★     2-3 days
P0 🔴   Convert H2/H3 to question format             ★★★★☆   ★☆☆     2 hours
P1 🟡   Add HowTo Schema                             ★★★★☆   ★★☆     Half day
P1 🟡   robots.txt AI crawler rules                   ★★★☆☆   ★☆☆     10 min
P1 🟡   Page load speed optimization                  ★★★★☆   ★★★     1-2 days
P1 🟡   og:image uniqueness per page                  ★★★☆☆   ★★☆     Half day
P2 🟢   Visible Last Updated date                     ★★★☆☆   ★☆☆     1 hour
P2 🟢   Title length optimization (50-60 chars)       ★★☆☆☆   ★☆☆     5 min
P2 🟢   HSTS Header                                   ★★☆☆☆   ★☆☆     5 min
P2 🟢   robots.txt reference to llms.txt              ★★☆☆☆   ★☆☆     1 min
P3 🔵   Off-page authority building                    ★★★★★   ★★★     Ongoing
P3 🔵   IndexNow integration                          ★★★☆☆   ★★☆     Half day
P3 🔵   Comparison content pages                       ★★★★☆   ★★★     Ongoing
P3 🔵   Multi-modal optimization (video + transcript)  ★★★☆☆   ★★★     Ongoing
```

---

## References

- [llms.txt Standard Proposal](https://llmstxt.org/) — Jeremy Howard, 2024
- [Google Structured Data Docs](https://developers.google.com/search/docs/appearance/structured-data)
- [Schema.org](https://schema.org/) — Structured data vocabulary
- [IndexNow Protocol](https://www.indexnow.org/)
- GEO Research: *"GEO: Generative Engine Optimization"* (2024)
