---
name: google-analytics-and-search-improve
description: Understand website goals and user journeys first, then analyze GSC/GA4 data and audit the live site to validate whether users behave as intended. Identify gaps between goals and reality, and produce actionable, goal-aligned improvement plans. Use when user wants to diagnose website problems, improve search rankings, optimize traffic, analyze Google Analytics or Search Console data, audit website performance, or create a data-backed improvement roadmap.
---

# Goal-Driven Website Analytics & Improvement

First understand what the site does and what it wants users to do, then use GSC/GA4 data combined with live-site auditing to verify whether users actually follow the intended journey. Identify the gap between goals and reality, and generate prioritized, actionable improvement plans.

## Data Storage

All runtime data is stored in `$DATA_DIR`, separated from skill code.

```
<project_root>/.skills-data/google-analytics-and-search-improve/
  .env        # Configuration (auth, URLs, etc.), auto-loaded by scripts
  data/       # Raw data only: API responses, user-uploaded CSVs (GSC/GA4/PSI JSON/CSV)
  analysis/   # Analysis outputs: reports, audit results, website profile, funnel analysis
  charts/     # Generated chart images (PNG) for embedding in analysis reports
  scripts/    # Analysis scripts: code that reads from data/ and writes to analysis/
  tmp/        # Screenshots and temporary files
  cache/      # API response cache
  configs/    # Config files (including Service Account JSON keys)
  logs/       # Execution logs
  venv/       # Python virtual environment (managed by uv)
```

**Directory separation principle**:
- `data/` = raw, unprocessed data from APIs or user exports (input)
- `analysis/` = processed results, reports, insights, audit findings (output)
- `charts/` = generated chart images (PNG) that are embedded in analysis reports via relative paths
- `scripts/` = analysis code that transforms `data/` → `analysis/`

## Core Principles

### Goal → Data → Gap → Action

Every analysis must start from the website's purpose and intended user journey. Data is only valuable when measured against a goal. The skill's job is to:

1. Understand what the site wants users to do (goal)
2. Use data to check if users actually do it (reality)
3. Find where the gap is (diagnosis)
4. Tell the developer what to do next (action)

### Code-Driven Data Analysis & Visualization

**All data analysis MUST be done through code, not by directly reading JSON and manually summarizing.**

When analyzing raw data from `$DATA_DIR/data/` (GSC JSON, GA4 JSON, PSI JSON, Bing JSON, etc.):

1. **Write a Python script** in `$DATA_DIR/scripts/` that reads the raw JSON, processes and aggregates the data, and outputs the structured results
2. **Execute the script** to produce accurate, reproducible results
3. **Generate charts** in the same script (or a companion script) — every analysis phase that produces quantitative data MUST generate accompanying charts saved to `$DATA_DIR/charts/`
4. **Use the script output and charts** to write the analysis report — embed chart images in Markdown reports

**Why**: Raw JSON files from APIs can be large and complex. Manually reading JSON and converting to text is error-prone — it's easy to miscount, misinterpret nested structures, or miss data. Code execution guarantees data accuracy and reproducibility. Charts generated from the same code ensure visual evidence is consistent with the data.

This principle applies to **all phases**: GSC analysis, GA4 analysis, funnel analysis, site audit data extraction, and final report data summarization. Never skip the code step.

Standard code patterns (data analysis + chart generation in one script), chart type selection guide, per-phase chart requirements, and CJK font support: see [references/data-visualization-guide.md](references/data-visualization-guide.md).

## Workflow

```
Analysis Progress:
- [ ] Phase 0: Website reconnaissance & goal definition
- [ ] Phase 1: Select data source & collect data
- [ ] Phase 2: GSC data analysis (aligned to goals)
- [ ] Phase 3: GA4 data analysis (aligned to goals)
- [ ] Phase 3b: GA4 funnel exploration (optional, if user has custom events)
- [ ] Phase 4: Live site audit
- [ ] Phase 5: Source code review
- [ ] Phase 5b: SEO & GEO optimization checklist audit
- [ ] Phase 6: Generate goal-aligned improvement report
```

---

### Phase 0: Website Reconnaissance & Goal Definition

> **Purpose**: Without understanding what the site does and what it wants users to do, all subsequent data analysis is directionless.

**Steps**:

1. **Visit the site** using `agent-browser` — explore homepage + 3-5 key pages from navigation. Take full-page screenshots, extract page metadata (title, headings, nav links, CTAs, forms). Save screenshots to `$DATA_DIR/tmp/`.

2. **Classify the website type** (Content/Blog, SaaS/Tool, E-commerce, Lead Gen, etc.) based on observed elements.

3. **Infer goals and present to user** — determine Primary Goal, Secondary Goals, Intended User Journey, and Key Conversion Points. Ask user to confirm or correct.

4. **Rank analysis dimensions** — select and rank which dimensions matter most for this site type (Acquisition/SEO, Conversion Funnel, Content Engagement, UX, Performance, Retention, Technical SEO/GEO).

5. **Ask user for additional context** — traffic sources, GA4 custom events, known pain points, recent changes, target audience.

Save the Website Goal Profile to `$DATA_DIR/analysis/website-profile.md`.

Detailed browser commands, classification tables, and templates: see [references/website-reconnaissance-reference.md](references/website-reconnaissance-reference.md).

---

### Phase 1: Select Data Source & Collect Data

**1a. Initialize directories & Python environment**:
```bash
DATA_DIR=".skills-data/google-analytics-and-search-improve"
mkdir -p "$DATA_DIR"/{data,analysis,charts,scripts,cache,logs,tmp,configs}
```

Set up a Python 3.12 virtual environment via `uv` and install dependencies (only needed once):
```bash
uv venv "$DATA_DIR/venv" --python 3.12
uv pip install -p "$DATA_DIR/venv" -r skills/google-analytics-and-search-improve/scripts/pyproject.toml
```

> **IMPORTANT**: All Python script executions in this skill MUST activate the venv first, then use `python` directly. Never use the system Python.
> ```bash
> source "$DATA_DIR/venv/bin/activate"
> python scripts/xxx.py ...
> ```

**1b. Ask user to choose data source**:

| Mode | Description | When to Use |
|------|-------------|-------------|
| **A. API auto-collection** | Create Service Account, configure `.env`, scripts auto-collect data | Most complete data, recommended |
| **B. Manual CSV export** | User exports CSV from GA4/GSC web consoles | Zero config, simplest |
| **C. Browser audit only** | Visit site directly, no GA4/GSC data | Quick technical checks |

**Mode A**: Check `$DATA_DIR/.env` for required config. If missing, guide user to fill in `SITE_URL`, `GSC_SITE_URL`, `GA4_PROPERTY_ID`. Place Service Account JSON key in `$DATA_DIR/configs/` (scripts auto-discover it via `utils.py`). Run collection scripts to save data to `$DATA_DIR/data/`.

**Mode B**: Send export instructions to user. After receiving CSV files in `$DATA_DIR/data/`, proceed to Phase 2-3.

**Mode C**: Only collect `SITE_URL`, skip to Phase 4.

Detailed configuration, collection commands, CSV export instructions, and custom query guidance: see [references/data-collection-reference.md](references/data-collection-reference.md).

---

### Phase 2: GSC Data Analysis (Goal-Aligned)

> **Purpose**: Understand how users find the site through search, and whether the right pages rank for the right queries.

Read GSC data from `$DATA_DIR/data/`. Review the Website Goal Profile from `$DATA_DIR/analysis/website-profile.md` before analyzing.

**Write analysis scripts** in `$DATA_DIR/scripts/` to process raw GSC JSON data. Use code to extract, aggregate, and calculate metrics — do not manually read JSON.

**Goal-aligned analysis**:

1. **Map queries to user intent stages** — classify top queries by Awareness / Consideration / Decision / Retention stages of the intended user journey.

2. **Check page-query alignment** — are users arriving at stage-appropriate pages, or landing on irrelevant pages?

3. **Standard SEO diagnostics** — high-impression low-CTR keywords, keywords ranked 4-10, declining pages, index coverage and sitemap health.

Analyze against thresholds in [references/metrics-glossary.md](references/metrics-glossary.md).

**Bing analysis** (optional): When `BING_WEBMASTER_API_KEY` is configured, include cross-engine comparison (Bing vs Google), keyword research via Bing's unique endpoints, backlink and crawl health analysis. Details in [references/data-collection-reference.md](references/data-collection-reference.md) §8.

**Output**: Top 10 SEO optimization opportunities organized by user journey stage. Save to `$DATA_DIR/analysis/gsc_analysis.md`. Analysis scripts should also generate Phase 2 charts (see [references/data-visualization-guide.md](references/data-visualization-guide.md)) and save to `$DATA_DIR/charts/gsc_*.png`.

---

### Phase 3: GA4 Data Analysis (Goal-Aligned)

> **Purpose**: Compare the intended user journey with actual behavior — find where reality diverges from intention.

Read GA4 data from `$DATA_DIR/data/`. Review the Website Goal Profile before analyzing.

**Write analysis scripts** in `$DATA_DIR/scripts/` to process raw GA4 JSON data. Use code to extract, aggregate, and calculate metrics — do not manually read JSON.

**Goal-aligned analysis**:

1. **Intended Journey vs Actual Behavior** — landing page alignment, path progression, conversion point performance.

2. **Identify behavior gaps** — dead-end pages (high traffic, no next step), key pages with low traffic, high-bounce pages, device/channel disparities.

3. **Standard GA4 diagnostics** — traffic trends, channel effectiveness, mobile vs desktop gaps, conversion events.

4. **Flag missing data** — explicitly tell the user what additional data would help explain gaps.

Analyze against thresholds in [references/metrics-glossary.md](references/metrics-glossary.md).

**Output**: Top 10 GA4 insights framed as "expected behavior vs actual behavior". Save to `$DATA_DIR/analysis/ga4_analysis.md`. Analysis scripts should also generate Phase 3 charts (see [references/data-visualization-guide.md](references/data-visualization-guide.md)) and save to `$DATA_DIR/charts/ga4_*.png`.

---

### Phase 3b: GA4 Funnel Exploration (Optional)

> **Purpose**: Deep-dive into multi-step conversion funnels when the user has custom events.

Ask the user if they have custom events for funnel analysis (e.g., signup flow, purchase flow). Skip if no custom events.

Use `ga4_funnel.py` to generate funnel reports. Supports: step-by-step completion/abandonment rates, device/channel breakdown, daily trends, advanced JSON config for complex filters.

**Write analysis scripts** in `$DATA_DIR/scripts/` to process raw funnel JSON data. Use code to calculate drop-off rates and segment comparisons.

> **API note**: `ga4_funnel.py` uses GA4 v1alpha API — functional but may have breaking changes. No additional auth needed beyond existing Service Account.

Script usage, CLI options, JSON config format, output format: see [references/data-collection-reference.md](references/data-collection-reference.md) §7.

**Output**: Funnel conversion analysis with per-step metrics. Save to `$DATA_DIR/analysis/funnel_analysis.md`. Analysis scripts should also generate Phase 3b charts (see [references/data-visualization-guide.md](references/data-visualization-guide.md)) and save to `$DATA_DIR/charts/funnel_*.png`.

---

### Phase 4: Live Site Audit

> **Purpose**: Performance audit and visual inspection of the live site.

**Steps**:

1. **Screenshot the site** (desktop + mobile) using `agent-browser`. Save to `$DATA_DIR/tmp/`.

2. **Run PageSpeed Insights** (mobile + desktop) — save JSON to `$DATA_DIR/data/psi_mobile.json` and `psi_desktop.json`. Extract Core Web Vitals; thresholds in [references/metrics-glossary.md](references/metrics-glossary.md).

3. **Screenshot top landing pages** (if GA4 data available) — desktop + mobile for each of the Top 10 landing pages.

4. **Extract front-end metadata** via browser (when no source code available) — title, meta description, H1, JSON-LD, images without alt, viewport, canonical.

**Write analysis scripts** in `$DATA_DIR/scripts/` to process raw PSI JSON data. Use code to extract scores and CWV metrics — do not manually read JSON.

PSI data collection commands: see [references/data-collection-reference.md](references/data-collection-reference.md).

**Output**: Performance scores + visual issue checklist. Save to `$DATA_DIR/analysis/site_audit.md`. Analysis scripts should also generate Phase 4 charts (see [references/data-visualization-guide.md](references/data-visualization-guide.md)) and save to `$DATA_DIR/charts/audit_*.png`.

---

### Phase 5: Source Code Review

> **Purpose**: Find code-level SEO and performance issues.

If `SOURCE_CODE_PATH` is configured in `.env`, analyze project source code. Skip if no source code is available.

Check items detailed in the "Technical Issues" checklist in [references/metrics-glossary.md](references/metrics-glossary.md). Core focus:

- **SEO**: Meta tag completeness, JSON-LD, robots.txt / sitemap.xml, image alt, H1 conventions
- **Performance**: JS/CSS splitting and lazy loading, image formats and responsive images, third-party scripts, render-blocking resources
- **Technical**: `<html lang>`, viewport, HTTPS, canonical URL, internal dead links

**Output**: Code-level improvement checklist. Save to `$DATA_DIR/analysis/code_review.md`.

---

### Phase 5b: SEO & GEO Optimization Checklist Audit

> **Purpose**: Evaluate the site's search engine and generative AI readiness.

Run audit scripts against the checklist in [references/SEO-GEO-Optimization-Checklist.md](references/SEO-GEO-Optimization-Checklist.md):

```bash
source "$DATA_DIR/venv/bin/activate"
set -a; source "$DATA_DIR/.env"; set +a
python scripts/seo_audit.py --url "$SITE_URL" --sitemap -o "$DATA_DIR/analysis/seo_audit.json"
python scripts/geo_audit.py --url "$SITE_URL" --sitemap -o "$DATA_DIR/analysis/geo_audit.json"
python scripts/perf_audit.py --url "$SITE_URL" --sitemap -o "$DATA_DIR/analysis/perf_audit.json"
```

Each script supports `--url`, `--sitemap`, `--pages`, `--max-pages`, `-o`. Checks: Structured Data, Meta Tags, Headings, Sitemap, AI Readability, Content Depth, Performance, Security.

**Write analysis scripts** in `$DATA_DIR/scripts/` to process audit JSON results. Use code to aggregate pass/fail counts and classify by priority — do not manually read JSON.

**Output**: SEO/GEO readiness checklist with pass/fail status, classified by P0-P3 priority. Save to `$DATA_DIR/analysis/seo_geo_checklist.md`.

---

### Phase 6: Generate Goal-Aligned Improvement Report

> **Purpose**: Synthesize all findings into a single, actionable, goal-organized report.

Organize output around the **website goals defined in Phase 0**, using the "Priority Matrix" (P0-P3) in [references/metrics-glossary.md](references/metrics-glossary.md).

**Write analysis scripts** in `$DATA_DIR/scripts/` to aggregate key metrics from all phases into a summary. Use code to calculate goal achievement percentages and priority distributions.

Follow the report template in [references/report-template.md](references/report-template.md). Key sections: Website Profile, Executive Summary, Goal Achievement Status, Data Overview, Key Findings, Improvement Plan (P0-P3), Missing Data, Next Steps, Execution Roadmap. Analysis scripts should also generate Phase 6 charts (executive dashboard, goal scorecard, priority distribution — see [references/data-visualization-guide.md](references/data-visualization-guide.md)). Reuse Phase 2-4 charts in Detailed Analysis.

Save the report to `$DATA_DIR/analysis/improvement-report.md`.

## User Persona Analysis

> **When to use**: When the user wants to understand who their users are, build data-driven user personas, or get recommendations for product iteration based on user profiling.

This skill supports a complete data-driven user persona analysis workflow. Instead of following the standard Phase 0-6 improvement pipeline, use the dedicated persona analysis flow:

**Steps**:

1. **Collect persona data** — run GA4 demographics, behavioral, and acquisition presets plus GSC query data. The persona-specific presets include: `demographics_age`, `demographics_gender`, `demographics_geo`, `demographics_language`, `demographics_interests`, `new_vs_returning`. Combine with existing presets (`device_breakdown`, `user_behavior`, `landing_pages`, `user_acquisition`, `top_pages`) and custom queries for time patterns and cross-segments.

2. **Segment & cluster** — apply behavioral, channel, demographic, and intent-based segmentation strategies to identify 3-5 distinct user groups.

3. **Build persona cards** — for each group, construct a data-backed persona with demographics, behavioral fingerprint, journey patterns, needs, and product iteration opportunities.

4. **Validate & extract insights** — cross-validate segments, analyze acquisition efficiency, engagement quality, conversion potential, and retention signals.

5. **Generate iteration recommendations** — map each persona to specific product, content, UX, and marketing recommendations.

**Write analysis scripts** in `$DATA_DIR/scripts/` to process all persona raw data, produce segmented profiles, and generate persona charts. Save charts to `$DATA_DIR/charts/persona_*.png`.

**Output**: User persona report with persona cards, cross-persona comparison, and actionable recommendations. Save to `$DATA_DIR/analysis/user-persona-report.md`.

Full methodology, data collection commands, segmentation strategies, persona card template, visualization requirements, and report structure: see [references/user-persona-analysis-reference.md](references/user-persona-analysis-reference.md).

---

## Companion Skills

- SEO implementation → `seo-geo`
- Browser automation → `agent-browser`
- Frontend redesign → `frontend-design`

## Reference Docs

| Document | Contents |
|----------|----------|
| [references/data-collection-reference.md](references/data-collection-reference.md) | Auth setup (GSC/GA4/Bing), .env configuration, collection commands, script usage (gsc_query.py, ga4_query.py, ga4_funnel.py, bing_query.py), dimensions & metrics, CSV export instructions, custom queries, PSI collection |
| [references/metrics-glossary.md](references/metrics-glossary.md) | Six analysis dimensions: thresholds, diagnostics, priority matrix |
| [references/SEO-GEO-Optimization-Checklist.md](references/SEO-GEO-Optimization-Checklist.md) | SEO & GEO optimization checklist: structured data, AI readability, content depth, performance |
| [references/data-visualization-guide.md](references/data-visualization-guide.md) | Chart generation patterns, type selection, per-phase chart requirements, CJK font support |
| [references/website-reconnaissance-reference.md](references/website-reconnaissance-reference.md) | Browser commands, website type classification, analysis dimensions, goal profile templates |
| [references/report-template.md](references/report-template.md) | Phase 6 final report Markdown template |
| [references/user-persona-analysis-reference.md](references/user-persona-analysis-reference.md) | User persona analysis: five-dimension model, segmentation strategies, persona card template, GA4 demographics presets, visualization requirements, iteration recommendations |
