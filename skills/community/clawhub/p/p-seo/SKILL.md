---
name: pseo-generator
description: "Build Programmatic SEO 2.0 systems at scale — AI-generated content using strict JSON schemas, niche taxonomy, and React renderers. Use when: (1) creating hundreds or thousands of programmatic pages, (2) building a niche taxonomy for pSEO content, (3) designing JSON schemas for AI-generated content types, (4) separating content generation from UI presentation, (5) generating resource pages, comparison pages, free tools, or checklist pages at scale. NOT for: traditional one-off page writing, keyword research only, or thin AI content that ignores niche context."
---

# Programmatic SEO 2.0 — Agent Skill Reference

The core principle: **never ask AI to write freeform content. Ask it to fill a strict JSON schema.**

Content = JSON data. Design = React components. These two layers never mix.

## System Architecture

```
Niche Taxonomy (309 niches) → AI fills JSON schema → Validated JSON files → React renderers → Published pages
```

**Why schemas beat freeform:**
- Consistent structure across all pages
- Predictable output quality
- Pages are validatable and type-safe
- Redesign UI without regenerating content
- Scale to 10,000+ pages without quality degradation

## Step 1: Build the Niche Taxonomy

This is the most important investment. Rich niche context is what separates useful pSEO from thin name-swapped filler.

For each niche, define:

```json
{
  "slug": "travel",
  "name": "Travel",
  "context": {
    "audience": "Armchair travelers, digital nomads, family vacation planners",
    "pain_points": "Seasonal traffic swings, high competition for destination keywords",
    "monetization": "Affiliate (booking, gear), display ads, sponsored trips",
    "content_that_works": "Itineraries, cost breakdowns, off-the-beaten-path guides",
    "subtopics": ["budget travel", "luxury travel", "adventure travel", "solo travel"]
  }
}
```

Start with 20-50 niches, expand to 300+ for scale. This context gets injected into every generation prompt — it's what makes a "travel SEO checklist" different from a "health SEO checklist."

See `references/niche-taxonomy.md` for the full niche structure and 20 starter niches.

## Step 2: Design JSON Schemas per Content Type

Each content type gets its own schema. Constraints are intentional — they force consistent output.

**Example: Resource Article Schema**
```typescript
interface ResourceArticle {
  meta: {
    content_type: string;
    niche: string;
  };
  seo: {
    title: string;        // templated, NOT AI-generated
    description: string;
    keywords: string[];
  };
  content: {
    intro: string;
    sections: {
      heading: string;
      items: {
        title: string;
        description: string;
        difficulty?: 'beginner' | 'intermediate' | 'advanced';
        potential?: 'high' | 'medium' | 'standard';
      }[];  // exactly 15-20 per section
    }[];
    pro_tips: string[];  // exactly 5
  };
}
```

Hard constraints (exact counts, required fields) prevent 8-item pages next to 40-item pages. See `references/schema-library.md` for 6 ready-to-use schemas.

## Step 3: The 6 Content Categories

| Category | Share | Notes |
|---|---|---|
| Resource pages | ~58% | Idea lists, checklists, calendars, guides, templates — 34 content types × N niches |
| Comparison pages | ~1% | Smallest category — most obvious, least differentiated |
| Free tools | ~15% | Actual working tools with niche-specific examples |
| Checklist pages | ~10% | Interactive, niche-aware |
| Guide pages | ~8% | Long-form, structured |
| Template pages | ~8% | Downloadable/fillable |

Resource pages are the highest-volume opportunity. Start there.

## Step 4: Generation at Scale

Use Gemini Flash (cost-to-quality ratio beats GPT-4 for structured JSON at volume).

**Why Gemini Flash:**
- Native structured JSON output (no markdown wrapping to parse)
- Cheap enough for 10,000+ pages
- Fast enough for batch generation

**Generation prompt pattern:**
```
Given this niche context: {niche_json}
Fill this schema: {schema}
Content type: {content_type}
Title template: {title}

Return ONLY valid JSON matching the schema. No prose, no markdown.
```

**Validation:** After generation, validate every file against the TypeScript schema. Reject and retry any that fail. At 13,000 pages, ~2-5% failure rate is normal.

**Speed:** 13,000+ pages in under 3 hours with parallel workers (10-20 concurrent API calls).

## Step 5: React Renderers

Each content type gets its own specialized renderer. The renderer consumes the JSON and handles all presentation.

```
/renderers/
  ResourceArticleRenderer.tsx   — with filtering by category/difficulty
  ChecklistRenderer.tsx          — interactive checkboxes
  ComparisonTableRenderer.tsx    — structured tables
  FreeToolRenderer.tsx           — working tool UI
```

**Key rule:** Renderers never call AI. They only consume pre-generated JSON. This means you can:
- Redesign any page without regenerating content
- A/B test layouts without touching data
- Add new niches without touching UI

## Key Metrics (Jake Ward experiment, 60 days)

- 13,000+ pages live
- Weekly organic clicks: 971 → 5,500 (+466%)
- ~50% of pages not yet indexed (curve still going up)
- Generation time: < 3 hours for all 13,000 pages

## Quick Start Checklist

- [ ] Define 20+ niches with full context (audience, pain points, monetization, subtopics)
- [ ] Choose 2-3 content types to start (resource pages recommended)
- [ ] Write strict TypeScript schemas with hard constraints
- [ ] Build generation script with niche injection and JSON validation
- [ ] Build React renderers per content type
- [ ] Generate first batch (start with 100 pages to validate quality)
- [ ] Review output — check niche specificity, not just structure
- [ ] Scale up generation
- [ ] Submit sitemap, monitor indexation rate

## References

- `references/niche-taxonomy.md` — Niche structure + 20 starter niches
- `references/schema-library.md` — 6 ready-to-use content type schemas

---

## Tolstoy-Specific Configuration

When generating pSEO content for **gotolstoy.com**, always load these files before generating any content:

- **Brand voice:** `~/.openclaw/workspace/tolstoy-context/brand-voice.md`
- **Competitor analysis:** `~/.openclaw/workspace/tolstoy-context/competitor-analysis.md`
- **Features:** `~/.openclaw/workspace/tolstoy-context/features.md`
- **Style guide:** `~/.openclaw/workspace/tolstoy-context/style-guide.md`
- **Writing examples:** `~/.openclaw/workspace/tolstoy-context/writing-examples.md`
- **Target keywords:** `~/.openclaw/workspace/tolstoy-context/target-keywords.md`
- **Internal links map:** `~/.openclaw/workspace/tolstoy-context/internal-links-map.md`
- **Schemas:** `~/.openclaw/workspace/tolstoy-pseo/schemas/`
- **Scale plan:** `~/.openclaw/workspace/tolstoy-pseo/SCALE-PLAN.md`

### Tolstoy Voice Rules (non-negotiable)
1. **Positioning:** Always use "AI Agent for Ecommerce" — never "tool" or "software"
2. **Products:** Name specifically: AI Studio, AI Player, AI Shopper
3. **Vocabulary:** "at scale," "autonomous," "closed loop," "without manual work"
4. **Tone:** Second-person ("you"), data-forward, peer-to-peer operator voice
5. **Proof metrics:** 7x PDP conversion lift, 232% AOV uplift, 11x conversion rate with AI Shopper, 2,000+ brand partners
6. **Do NOT:** Name competitors directly in body copy — stay category-level
7. **Closed loop framing:** AI Studio creates → AI Player distributes → AI Shopper converts → data loops back

### Tolstoy Content Map (20 pages total)
| Type | Count | Status |
|---|---|---|
| Comparison pages (Tolstoy vs X) | 8 | 1 done (Rep AI) |
| Topic/gap pages (category attack) | 7 | 0 done |
| Use case pages | 4 | 0 done |

**Highest priority gaps** (Tolstoy absent from AI Overviews):
- "Best AI agent apps for Shopify 2026"
- "Best AI agents for Shopify Plus brands"
- "Best AI agents for dynamic product pages on Shopify"
- "AI agents for DTC brands"
- "Virtual try-on for fashion ecommerce"

### Webflow Publishing (when API key is available)
Tolstoy blog runs on Webflow CMS. Publishing flow:
1. Generate content JSON against schema
2. Render to HTML/markdown via renderer
3. POST to Webflow CMS API: `POST /v2/collections/{collection_id}/items`
4. Publish item: `POST /v2/collections/{collection_id}/items/{item_id}/publish`

Required fields for Webflow blog item (to be confirmed with API key):
- `name` (post title)
- `slug` (URL slug)
- `body` (HTML content)
- `meta-title`, `meta-description` (SEO fields)
- `published` (boolean)
