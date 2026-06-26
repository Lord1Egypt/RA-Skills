# keyword_optimize

Page-level keyword optimization combining Ahrefs MCP data with GEO (Generative Engine Optimization) principles.

Targets both traditional search (Google) and AI-powered search (ChatGPT, Perplexity, Google AI Overviews, Gemini, Claude).

---

## What This Does

Takes a target page + competitor URLs, runs Ahrefs MCP to extract keyword gaps and opportunities, then produces a structured optimization plan covering:

- On-page keyword mapping (title, H1, H2, body, meta, alt, internal links)
- GEO citability layer (opening answer block, FAQ schema, CITE framework)
- Automated ranking health monitoring via Ahrefs API

---

## Requirements

- Ahrefs account (Lite plan or higher) with MCP access
- Ahrefs MCP configured in Claude Code (`ahrefs-mcp-server`)
- Target page URL and 3–5 competitor URLs at the same search intent

---

## Quick Start

1. Open `SKILL.md` — it contains the full step-by-step workflow.
2. Provide your target URL and competitors to Claude Code.
3. Claude will run the Ahrefs MCP phases sequentially and output a keyword matrix + optimization plan.

---

## Workflow Summary

```
Phase 1  Ahrefs MCP keyword intelligence
         └─ keywords_explorer → semantic cluster
         └─ site_explorer × competitors → their organic keywords
         └─ content_gap → your missing keywords

Phase 2  On-page keyword mapping
         └─ Title / H1 / H2 / body / meta / alt / internal links

Phase 3  GEO layer
         └─ 50-word authoritative opening block
         └─ FAQ schema from Ahrefs question keywords
         └─ CITE framework per section
         └─ Factual density check (≥3 verifiable facts per 500 words)

Phase 4  Monitoring
         └─ Weekly Ahrefs API rank check
         └─ Monthly content gap re-run
         └─ Alert on position drop or new high-volume gap keyword
```

---

## Priority Actions (Ranked by ROI)

| # | Action |
|---|--------|
| 1 | Content gap analysis vs. competitors (page-level) |
| 2 | FAQ Schema from Ahrefs question-type keywords |
| 3 | Title / H1 / H2 keyword remapping |
| 4 | 50-word authoritative answer block at page open |
| 5 | Internal link anchor text optimization |
| 6 | API ranking monitor + regression alerts |

---

## Reference Projects (GitHub, Stars Descending)

| Project | Stars | Role |
|---------|-------|------|
| [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) | ~7k | SEO/GEO automation framework for Claude Code |
| [serpapi/awesome-seo-tools](https://github.com/serpapi/awesome-seo-tools) | ~863 | Curated SEO + GEO tool directory |
| [teles/awesome-seo](https://github.com/teles/awesome-seo) | ~600+ | SEO resource links, keyword research references |
| [amplifying-ai/awesome-generative-engine-optimization](https://github.com/amplifying-ai/awesome-generative-engine-optimization) | ~300+ | GEO methodology and AI citability patterns |
| [aaron-he-zhu/seo-geo-claude-skills](https://github.com/aaron-he-zhu/seo-geo-claude-skills) | ~51 | CORE-EEAT + CITE frameworks, 20 actionable skills |

---

## Key Concepts

**GEO (Generative Engine Optimization)** — Optimizing content to be cited by AI engines, not just ranked by Google. Requires structured, factually dense, directly answerable content.

**Content Gap** — Keywords that competitor pages rank for on the same topic that your page does not cover. Closing gaps is the fastest path to traffic gains.

**CITE Framework** — Claim → Insight → Trust signal → Evidence. A writing structure that maximizes AI citability per paragraph.

**FAQ Schema** — Structured markup that surfaces question-type keywords as eligible for featured snippets and AI Overview extraction.
