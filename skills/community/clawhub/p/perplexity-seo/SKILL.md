---
name: perplexity-seo
version: 1.0.0
description: |
  Perplexity SEO Optimization Guide — How to get cited by Perplexity AI. Covers Perplexity citation behavior, content structure for Perplexity answers, PerplexityBot crawling, FAQ schema for Perplexity, and real case studies of content being cited by Perplexity. Includes step-by-step Perplexity optimization checklist.

  Keywords: perplexity seo, perplexity seo optimization, perplexity search, perplexity ai optimization, how to rank on perplexity, perplexity citation, perplexitybot, perplexity seo guide, perplexity seo tutorial, perplexity content strategy, perplexity serp, perplexity search engine, perplexity seo tips, perplexity ai search
---

# Perplexity SEO Optimization Guide

> Get your content cited in Perplexity AI answers
> by Iris (@gingiris) — AFFiNE former COO, 30+ PH #1 launches

---

## TL;DR

- Perplexity cites **structured, authoritative content** — not keyword-stuffed pages
- **FAQPage Schema + clear Q&A** = highest citation rate
- PerplexityBot (CCBot) must be allowed in robots.txt
- **Freshness matters** — Perplexity prefers recent content
- Cite authoritative sources in your content to signal trust signals

---

## How Perplexity Cites Content

Perplexity uses a mix of:
1. **Web search** — Bing-indexed pages, prioritized by freshness
2. **Direct citations** — structured content from high-authority pages
3. **LLM-trained knowledge** — but current events require fresh sources

Perplexity tends to cite pages that have:
- **Clear Q&A structure** — questions as headings, direct answers first
- **Specific data** — numbers, statistics, dates beat vague claims
- **Authoritative sources** — cited references signal credibility
- **FAQ sections** — FAQPage Schema is heavily cited
- **Short, self-contained paragraphs** — each paragraph answers one thing

---

## Perplexity Citation Checklist

### Robots.txt — Allow PerplexityBot
```txt
User-agent: CCBot
Allow: /

User-agent: perplexitybot
Allow: /
```

### Content Structure

**The Q&A-First Pattern:**
```markdown
## [Specific Question in Heading]

**[Direct answer — 1-2 sentences]**
[Stat or data point]
[Source citation]

[Supporting detail — 1 paragraph]

[Actionable step]
```

**Example:**
```markdown
## How long does Product Hunt approval take?

Product Hunt approval typically takes 1-3 business days. 
New makers on Hacker News with 10+ posts get approved 
within 24 hours. Submissions without a working demo 
are rejected 40% of the time (based on 500+ submission analysis).

For fastest approval: submit Tuesday–Thursday with 
a 60-second demo video linked.
```

### FAQPage Schema (Critical for Perplexity)
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "How does Perplexity rank content?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Perplexity prioritizes pages with clear Q&A structure..."
    }
  }]
}
```

### Freshness Signals
- Add `dateModified` in Article Schema
- Update content monthly
- Link from recently published pages
- Use IndexNow to push updates to Bing (Perplexity crawls Bing)

---

## PerplexityBot vs Googlebot

| Factor | PerplexityBot (CCBot) | Googlebot |
|--------|----------------------|-----------|
| **Crawl frequency** | Lower | Higher |
| **Freshness priority** | Very high | High |
| **Schema importance** | Critical | Important |
| **Page speed** | Moderate | Critical |
| **Mobile-first** | Yes | Yes |

---

## Perplexity Optimization Prompt

```
You are a Perplexity SEO specialist.

Audit this content for Perplexity citation optimization:
1. Is the main question clear in the first 100 words?
2. Does each H2 start with a direct answer?
3. Is there an FAQ section with 5+ questions?
4. Is FAQPage Schema present?
5. Are there specific numbers/statistics cited?
6. Is CCBot allowed in robots.txt?
7. Is dateModified in Article Schema?
8. Are authoritative sources cited?

Output: Prioritized fix list with severity (high/medium/low).
```

---

## How to Submit to Perplexity

Perplexity doesn't have a direct submission tool, but:

1. **IndexNow push** — Bing → Perplexity (since Perplexity crawls Bing)
   ```bash
   curl "https://www.bing.com/indexnow?url=YOUR_URL&key=YOUR_KEY"
   ```

2. **Sitemap submission** — Submit to Bing Webmaster Tools
   ```
   https://www.bing.com/webmasters/sitemaps
   ```

3. **LinkedIn** — Perplexity shows LinkedIn results; having your brand on LinkedIn helps

4. **Press mentions** — News articles cited by Perplexity at higher rates

---

## Real Case Studies

### Case 1: AFFiNE Documentation
- Added FAQPage Schema to docs pages
- Structured each page as "How to [task]?" → direct answer first
- Result: cited in 12 Perplexity answers within 30 days

### Case 2: Growth Tools Blog
- IndexNow push on every new post
- Article Schema with author (Iris)
- Result: 8 Perplexity citations in first week

---

## Step-by-Step: Optimize for Perplexity

### Step 1: Audit (10 min)
```bash
# Check if PerplexityBot is allowed
curl -A "CCBot" http://yoursite.com/robots.txt | grep -i "ccbot\|perplexity"
```

### Step 2: Add FAQPage Schema (30 min)
- Add 5-10 FAQ questions to your key pages
- Use JSON-LD format
- Validate at https://search.google.com/test/rich-results

### Step 3: Restructure Content (60 min)
- Change H2 headings to question form
- Add 1-sentence direct answers before each section
- Insert specific statistics and dates

### Step 4: Push Updates (5 min)
```bash
curl "https://www.bing.com/indexnow?url=UPDATED_URL&key=YOUR_KEY"
```

### Step 5: Monitor (ongoing)
Search for your brand on Perplexity weekly.
```bash
# Check if your content is cited (manual)
# Search: site:yoursite.com on Perplexity
```

---

## Prompt Templates

### Prompt: Perplexity Article Writer
```
Write a Perplexity-optimized article targeting: [keyword]

Requirements:
1. Title: [keyword] question form
2. Opening 100 words: direct answer + key stats table
3. H2 = questions, each starts with 1-sentence direct answer
4. FAQ section: 8 questions with specific answers
5. FAQPage Schema (JSON-LD)
6. Article Schema with dateModified
7. Specific numbers, dates, sources cited
8. Internal links to 2+ related pages
```

### Prompt: Perplexity Audit
```
Audit [URL] for Perplexity SEO:
1. robots.txt — CCBot allowed?
2. FAQPage Schema — 5+ questions?
3. Opening — direct answer in 100 words?
4. H2 structure — questions with direct answers?
5. Freshness — dateModified present?
6. Specificity — numbers and sources cited?

Output: severity + fix for each issue.
```

---

## Related Resources

**Free Playbooks (GitHub):**
- SEO & GEO Playbook: https://github.com/Gingiris/seo-geo-playbook
- Gingiris Launch: https://github.com/Gingiris/gingiris-launch
- Growth Tools: https://gingiris.github.io/growth-tools/

**Author**: Iris (@gingiris) — AFFiNE former COO, open source growth consultant
