# User Persona Analysis Reference

Data-driven user persona analysis methodology for websites and applications. Combines GA4 behavioral data, GSC search intent data, and live-site observation to build evidence-backed user profiles that directly guide product iteration and marketing optimization.

---

## 1. What Is Data-Driven User Persona Analysis?

A **data-driven user persona** is a fictional but evidence-backed representation of a user type, built from quantitative behavioral data and qualitative insights. Unlike traditional personas based on assumptions, data-driven personas are:

- **Verifiable**: Every attribute is backed by analytics data
- **Measurable**: Key metrics track each persona's behavior over time
- **Actionable**: Each persona maps to concrete product/marketing decisions
- **Iterative**: Personas are refreshed as new data arrives (recommended quarterly)

---

## 2. Persona Analysis Framework

### 2.1 The Five-Dimension Model

Build each persona across five dimensions, from outer (observable) to inner (inferred):

```
┌───────────────────────────────────────────────────┐
│  1. WHO — Demographics & Environment              │
│  ┌───────────────────────────────────────────────┐│
│  │  2. HOW — Behavioral Patterns                 ││
│  │  ┌───────────────────────────────────────────┐││
│  │  │  3. WHERE FROM — Acquisition & Context    │││
│  │  │  ┌───────────────────────────────────────┐│││
│  │  │  │  4. WHAT — Content & Feature Affinity ││││
│  │  │  │  ┌───────────────────────────────────┐││││
│  │  │  │  │  5. WHY — Intent & Goals          │││││
│  │  │  │  └───────────────────────────────────┘││││
│  │  │  └───────────────────────────────────────┘│││
│  │  └───────────────────────────────────────────┘││
│  └───────────────────────────────────────────────┘│
└───────────────────────────────────────────────────┘
```

| Dimension | Key Questions | Primary Data Source |
|-----------|---------------|---------------------|
| **1. WHO** | Age, gender, location, language, device, OS | GA4 demographics + device reports |
| **2. HOW** | Session patterns, engagement depth, visit frequency, journey paths | GA4 behavior + funnel data |
| **3. WHERE FROM** | Traffic channels, search queries, referral sources, first-touch attribution | GA4 acquisition + GSC queries |
| **4. WHAT** | Top pages visited, content preferences, feature usage, search terms | GA4 pages + events + site search |
| **5. WHY** | User intent stage, conversion behavior, goal completion | GSC intent mapping + GA4 conversions |

### 2.2 Analysis Phases

```
Phase A: Data Collection & Enrichment
  ↓
Phase B: Segmentation & Clustering
  ↓
Phase C: Persona Construction
  ↓
Phase D: Validation & Insights
  ↓
Phase E: Application & Iteration Recommendations
```

---

## 3. Phase A: Data Collection & Enrichment

### 3.1 GA4 Data Collection

Collect the following data using `ga4_query.py` presets and custom queries:

```bash
source "$DATA_DIR/venv/bin/activate"
set -a; source "$DATA_DIR/.env"; set +a

# ── Demographics ──────────────────────────────────────────
python scripts/ga4_query.py --preset demographics_age -o "$DATA_DIR/data/ga4_persona_age.json"
python scripts/ga4_query.py --preset demographics_gender -o "$DATA_DIR/data/ga4_persona_gender.json"
python scripts/ga4_query.py --preset demographics_geo -o "$DATA_DIR/data/ga4_persona_geo.json"
python scripts/ga4_query.py --preset demographics_language -o "$DATA_DIR/data/ga4_persona_language.json"
python scripts/ga4_query.py --preset demographics_interests -o "$DATA_DIR/data/ga4_persona_interests.json"

# ── Behavioral Patterns ───────────────────────────────────
python scripts/ga4_query.py --preset device_breakdown -o "$DATA_DIR/data/ga4_persona_devices.json"
python scripts/ga4_query.py --preset user_behavior --limit 200 -o "$DATA_DIR/data/ga4_persona_behavior.json"
python scripts/ga4_query.py --preset landing_pages --limit 100 -o "$DATA_DIR/data/ga4_persona_landing.json"
python scripts/ga4_query.py --preset top_pages --limit 200 -o "$DATA_DIR/data/ga4_persona_pages.json"

# ── Acquisition ───────────────────────────────────────────
python scripts/ga4_query.py --preset user_acquisition -o "$DATA_DIR/data/ga4_persona_acquisition.json"
python scripts/ga4_query.py --preset traffic_overview -o "$DATA_DIR/data/ga4_persona_traffic.json"

# ── New vs Returning ──────────────────────────────────────
python scripts/ga4_query.py --preset new_vs_returning -o "$DATA_DIR/data/ga4_persona_new_returning.json"

# ── Engagement Depth (custom) ─────────────────────────────
python scripts/ga4_query.py \
    --dimensions newVsReturning,deviceCategory \
    --metrics sessions,totalUsers,bounceRate,averageSessionDuration,engagementRate,screenPageViewsPerSession \
    -o "$DATA_DIR/data/ga4_persona_engagement_segments.json"

# ── Hourly / Day-of-Week Patterns (custom) ────────────────
python scripts/ga4_query.py \
    --dimensions dayOfWeekName,hour \
    --metrics sessions,totalUsers \
    --order-by="-sessions" \
    -o "$DATA_DIR/data/ga4_persona_time_patterns.json"

# ── Conversion by Segment (custom) ────────────────────────
python scripts/ga4_query.py \
    --dimensions sessionDefaultChannelGroup,deviceCategory \
    --metrics sessions,conversions,engagementRate \
    --order-by="-sessions" \
    -o "$DATA_DIR/data/ga4_persona_conversion_segments.json"
```

> **Note on Demographics data**: Age, Gender, and Interests dimensions (`userAgeBracket`, `userGender`, `brandingInterest`) require **Google Signals** to be enabled in the GA4 property. If not enabled, these queries return empty results. In that case, note the gap and proceed with behavioral data only. See [data-collection-reference.md](data-collection-reference.md) for auth setup.

### 3.2 GSC Search Intent Data

```bash
# Top queries reveal what users are looking for
python scripts/gsc_query.py --dimensions query --limit 500 -o "$DATA_DIR/data/gsc_persona_queries.json"

# Query + page mapping shows intent-to-content alignment
python scripts/gsc_query.py --dimensions query,page --limit 500 -o "$DATA_DIR/data/gsc_persona_query_pages.json"

# Device distribution in search
python scripts/gsc_query.py --dimensions device --limit 100 -o "$DATA_DIR/data/gsc_persona_devices.json"

# Country distribution in search
python scripts/gsc_query.py --dimensions country --limit 100 -o "$DATA_DIR/data/gsc_persona_countries.json"
```

### 3.3 Supplementary Data (If Available)

| Data Source | What It Reveals | How to Collect |
|-------------|-----------------|----------------|
| **Bing Webmaster** | Keyword research, related queries | `bing_query.py --mode keyword` / `--mode related_keywords` |
| **Site search logs** | On-site user intent | GA4 `searchTerm` dimension |
| **Funnel data** | Conversion journey patterns | `ga4_funnel.py` (see [data-collection-reference.md](data-collection-reference.md) §7) |
| **Heatmaps / Session recordings** | Click patterns, attention zones | Third-party tools (Hotjar, Clarity) |
| **User surveys / Interviews** | Motivations, pain points, goals | Qualitative research methods |
| **CRM / Support tickets** | Common questions, user frustrations | Internal data export |

---

## 4. Phase B: Segmentation & Clustering

### 4.1 Segmentation Strategies

Apply multiple segmentation lenses to identify distinct user groups:

#### Strategy 1: Behavioral Segmentation (Primary)

Segment by engagement level using GA4 metrics:

| Segment | Definition | Key Indicators |
|---------|------------|----------------|
| **Power Users** | High frequency + high engagement + repeat visits | `sessionsPerUser` > 3, `engagementRate` > 80%, `newVsReturning` = returning |
| **Engaged Explorers** | Moderate frequency, deep content consumption | `screenPageViewsPerSession` > 4, `averageSessionDuration` > 3 min |
| **Quick Scanners** | Brief visits, shallow engagement | `bounceRate` > 70%, `averageSessionDuration` < 30s |
| **One-Time Visitors** | Single visit, never return | `newVsReturning` = new, `sessions` = 1 |
| **Converting Users** | Completed key conversion events | `conversions` > 0, `keyEvents` > 0 |

#### Strategy 2: Acquisition Channel Segmentation

| Segment | Channel | Typical Behavior |
|---------|---------|------------------|
| **Organic Seekers** | Organic Search (Google/Bing) | Intent-driven, goal-oriented, query patterns reveal needs |
| **Social Browsers** | Social Media | Discovery-driven, shorter sessions, content-focused |
| **Direct Loyalists** | Direct | Repeat visitors, brand-aware, deeper engagement |
| **Referral Explorers** | Referral | Curiosity-driven, evaluate against known alternatives |
| **Paid Converters** | Paid Search / Display | High intent, expect immediate value delivery |

#### Strategy 3: Demographics + Device Cross-Segmentation

| Lens | Dimensions | Use Case |
|------|-----------|----------|
| Age × Device | `userAgeBracket` × `deviceCategory` | Younger users on mobile vs older on desktop |
| Geo × Language | `country` × `language` | Localization priorities |
| Device × Channel | `deviceCategory` × `sessionDefaultChannelGroup` | Mobile-social vs desktop-organic patterns |
| Gender × Interests | `userGender` × `brandingInterest` | Content and marketing personalization |

#### Strategy 4: Intent-Based Segmentation (from GSC)

Classify search queries by user journey stage:

| Intent Stage | Query Pattern Examples | User Need |
|--------------|----------------------|-----------|
| **Awareness** | "what is...", "how to...", informational | Learning, exploring |
| **Consideration** | "[product] vs [alternative]", "best [category]", comparison | Evaluating options |
| **Decision** | "[brand] pricing", "[product] signup", transactional | Ready to act |
| **Retention** | "[brand] login", "[brand] support", navigational | Existing user needs |

### 4.2 Segmentation Analysis Script

Write a Python script in `$DATA_DIR/scripts/` to process the collected data and produce segmented profiles. The script should:

1. Load all `ga4_persona_*.json` and `gsc_persona_*.json` from `$DATA_DIR/data/`
2. Cross-tabulate dimensions (e.g., device × channel × new_vs_returning)
3. Calculate per-segment metrics (engagement rate, bounce rate, conversion rate, avg session duration)
4. Identify 3-5 distinct user clusters based on behavioral patterns
5. Output structured JSON to `$DATA_DIR/data/persona_segments.json`
6. Generate persona charts to `$DATA_DIR/charts/persona_*.png`

---

## 5. Phase C: Persona Construction

### 5.1 Persona Card Template

For each identified persona (recommend 3-5 personas), construct a card with:

```markdown
## Persona: [Name] — "[Tagline]"

### Quick Profile
| Attribute | Value |
|-----------|-------|
| **Archetype** | [e.g., Power User / Casual Browser / Intent Seeker] |
| **% of Total Users** | [e.g., 35%] |
| **% of Conversions** | [e.g., 60%] |
| **Primary Channel** | [e.g., Organic Search] |
| **Primary Device** | [e.g., Desktop] |

### Demographics (if available)
| Attribute | Value |
|-----------|-------|
| **Age Range** | [e.g., 25-34] |
| **Gender** | [e.g., 65% Male] |
| **Top Locations** | [e.g., US, UK, India] |
| **Languages** | [e.g., English, Chinese] |
| **Interests** | [e.g., Technology, Business] |

### Behavioral Fingerprint
| Metric | Value | vs Site Average |
|--------|-------|-----------------|
| **Sessions / User** | [value] | [+/-% vs avg] |
| **Avg Session Duration** | [value] | [+/-% vs avg] |
| **Pages / Session** | [value] | [+/-% vs avg] |
| **Bounce Rate** | [value] | [+/-% vs avg] |
| **Engagement Rate** | [value] | [+/-% vs avg] |
| **Conversion Rate** | [value] | [+/-% vs avg] |

### Journey Pattern
- **Entry Point**: [typical landing pages]
- **Content Preferences**: [top pages / content types consumed]
- **Search Queries**: [representative GSC queries that bring this persona]
- **Visit Pattern**: [e.g., weekday mornings, mobile-first, 2-3 visits before converting]

### Needs & Pain Points (Inferred)
1. [Need inferred from behavior data + search queries]
2. [Pain point inferred from high bounce / exit pages]

### Product Iteration Opportunities
1. [Specific recommendation tied to this persona's behavior]
2. [Content/feature gap identified from their journey]
```

### 5.2 Key Principles

1. **Name each persona** — use memorable names (e.g., "Alex the Analyst", "Sarah the Searcher"), not "Persona 1"
2. **Data-backed attributes only** — every attribute must trace to specific data evidence
3. **Decision-relevant** — only include attributes that influence product or marketing decisions; remove noise
4. **Quantify differences** — show how each persona differs from site averages and from other personas
5. **Link to actions** — each persona must map to at least 2-3 concrete product/marketing recommendations

---

## 6. Phase D: Validation & Insights

### 6.1 Cross-Validation Methods

| Method | Description | Data Source |
|--------|-------------|-------------|
| **Behavioral consistency** | Check if persona segments show consistent patterns across time periods | Compare 30-day windows |
| **Channel-behavior alignment** | Verify that channel-based segments align with behavioral segments | Cross-tab acquisition × behavior |
| **Conversion correlation** | Confirm that high-engagement personas actually convert more | Conversion rate per segment |
| **Search intent match** | Verify GSC intent stages align with GA4 journey behavior | Map queries → landing pages → next actions |
| **Cohort stability** | Check if persona distributions remain stable over time | Monthly segment size tracking |

### 6.2 Key Insights to Extract

For each persona, answer these questions:

**Acquisition Efficiency**:
- Which channels bring the most users of this type?
- What's the cost-efficiency of acquiring this persona? (if ad data available)
- What search queries attract this persona?

**Engagement Quality**:
- Which content keeps this persona engaged?
- Where do they drop off in the journey?
- What's their typical visit cadence?

**Conversion Potential**:
- What's this persona's conversion rate?
- What % of revenue/conversions does this persona drive?
- What's the gap between their current and potential conversion rate?

**Retention Signals**:
- Does this persona return? How often?
- What triggers return visits?
- What are the early warning signs of churn for this persona?

---

## 7. Phase E: Application & Iteration Recommendations

### 7.1 Product Iteration Matrix

Map each persona to specific product decisions:

| Persona | UX Priority | Content Strategy | Feature Priority | Marketing Channel |
|---------|-------------|-----------------|------------------|-------------------|
| [Name A] | Mobile-first optimization | In-depth tutorials | Advanced features | SEO + Content marketing |
| [Name B] | Fast load, clear CTA | Quick-start guides | Core features, simple UI | Paid search |
| [Name C] | Browsing-friendly layout | Visual, shareable content | Social sharing, bookmarks | Social media |

### 7.2 Actionable Recommendations Checklist

For each persona, generate recommendations in these categories:

#### Content & Messaging
- [ ] Content gaps: topics this persona searches for but can't find on the site
- [ ] Content format: does this persona prefer long-form, video, interactive, or quick-reference?
- [ ] Messaging tone: formal vs casual, technical vs beginner-friendly
- [ ] Localization needs: language/regional preferences

#### UX & Design
- [ ] Device optimization: mobile-specific issues for mobile-heavy personas
- [ ] Navigation: are key pages easily reachable for this persona's entry point?
- [ ] Page speed: impact on bounce rate for this persona's device/network
- [ ] CTA placement: aligned with this persona's scrolling and engagement patterns

#### Conversion Optimization
- [ ] Landing page alignment: do landing pages match this persona's search intent?
- [ ] Conversion path: simplify the path from this persona's entry to conversion
- [ ] Trust signals: what does this persona need to see before converting?
- [ ] Friction points: specific pages where this persona drops off

#### Acquisition Strategy
- [ ] Channel investment: increase spend on channels that bring high-value personas
- [ ] Keyword strategy: target queries that attract converting personas
- [ ] Content marketing: create content for underserved persona segments
- [ ] Retargeting: build audience lists based on persona behavior patterns

---

## 8. Visualization Requirements

Generate the following charts for persona analysis (follow patterns in [data-visualization-guide.md](data-visualization-guide.md)):

### Required Charts

| Chart | Type | Description | Output File |
|-------|------|-------------|-------------|
| **Demographics overview** | Multi-panel (pie + bar) | Age, gender, top countries distribution | `persona_demographics.png` |
| **Device & technology** | Stacked bar / pie | Device type, OS, browser distribution | `persona_devices.png` |
| **Channel distribution** | Pie / horizontal bar | Traffic sources per persona | `persona_channels.png` |
| **Engagement comparison** | Grouped bar | Key metrics (bounce rate, engagement rate, session duration) by persona | `persona_engagement.png` |
| **Content affinity heatmap** | Heatmap / grouped bar | Top content categories per persona | `persona_content.png` |
| **Journey flow** | Sankey or funnel | Entry → key pages → conversion/exit per persona | `persona_journey.png` |
| **Time patterns** | Heatmap (day × hour) | Visit patterns by day-of-week and hour | `persona_time_patterns.png` |
| **New vs Returning** | Stacked bar | New/returning ratio with engagement overlay | `persona_new_returning.png` |
| **Persona summary** | Radar / spider chart | Multi-metric comparison across all personas | `persona_radar.png` |
| **Interests** | Horizontal bar | Top interest categories (if Google Signals enabled) | `persona_interests.png` |

### Chart Embedding in Report

```markdown
![Demographics Overview](../charts/persona_demographics.png)
![Persona Engagement Comparison](../charts/persona_engagement.png)
![User Journey by Persona](../charts/persona_journey.png)
```

---

## 9. Output & Report

Save the persona analysis report to `$DATA_DIR/analysis/user-persona-report.md`.

### Report Structure

```markdown
# User Persona Analysis Report

## Overview
- **Website**: [URL]
- **Analysis Period**: [start_date] ~ [end_date]
- **Total Users Analyzed**: [count]
- **Personas Identified**: [count]
- **Data Sources**: [GA4 demographics / GA4 behavior / GSC queries / ...]

## Key Findings Summary
[3-5 bullet points: most impactful persona insights]

## Site-Wide User Profile
[Aggregate demographics, device, channel, behavior overview — the "average user"]

![Demographics Overview](../charts/persona_demographics.png)
![Device Distribution](../charts/persona_devices.png)
![Time Patterns](../charts/persona_time_patterns.png)

## Persona Profiles
### Persona 1: [Name] — "[Tagline]"
[Full persona card using template from §5.1]

### Persona 2: [Name] — "[Tagline]"
...

## Cross-Persona Comparison

![Engagement Comparison](../charts/persona_engagement.png)
![Persona Radar](../charts/persona_radar.png)

| Metric | [Persona A] | [Persona B] | [Persona C] | Site Average |
|--------|-------------|-------------|-------------|--------------|
| % of Users | ... | ... | ... | 100% |
| % of Conversions | ... | ... | ... | 100% |
| Bounce Rate | ... | ... | ... | ... |
| Engagement Rate | ... | ... | ... | ... |
| Avg Session Duration | ... | ... | ... | ... |
| Pages / Session | ... | ... | ... | ... |

## Product Iteration Recommendations
[Organized by persona, using the matrix from §7.1]

## Content Strategy Recommendations
[Content gaps, format preferences, localization needs per persona]

## Data Gaps & Next Steps
| Missing Data | Impact | How to Collect |
|---|---|---|
| [e.g., Google Signals not enabled] | Cannot determine age/gender | Enable in GA4 Admin |
| [e.g., No custom events] | Cannot track micro-conversions | Add event tracking |
| [e.g., No user survey data] | Cannot validate intent assumptions | Run user survey |

## Appendix: Raw Segment Data
[Link to or embed key data tables for reference]
```

---

## 10. GA4 API Dimensions & Metrics Quick Reference

### Demographics Dimensions

| API Name | Description | Requires Google Signals |
|----------|-------------|------------------------|
| `userAgeBracket` | Age range (18-24, 25-34, etc.) | ✅ Yes |
| `userGender` | Gender (male, female) | ✅ Yes |
| `brandingInterest` | Interest categories | ✅ Yes |
| `country` | Country | No |
| `city` | City | No |
| `region` | Region | No |
| `continent` | Continent | No |
| `language` | Browser language | No |
| `languageCode` | Language code (e.g., en-us) | No |

### Behavioral Dimensions

| API Name | Description |
|----------|-------------|
| `newVsReturning` | New or returning user |
| `deviceCategory` | Desktop / mobile / tablet |
| `operatingSystem` | OS name |
| `browser` | Browser name |
| `screenResolution` | Screen resolution |
| `dayOfWeekName` | Day of week |
| `hour` | Hour of day (0-23) |

### Key Metrics for Persona Analysis

| API Name | Description | Use In Persona |
|----------|-------------|----------------|
| `totalUsers` | Total unique users | Segment sizing |
| `newUsers` | First-time users | New user ratio |
| `sessions` | Total sessions | Visit frequency |
| `sessionsPerUser` | Sessions per user | Loyalty indicator |
| `bounceRate` | Bounce rate | Engagement quality |
| `engagementRate` | Engagement rate | Content relevance |
| `averageSessionDuration` | Avg session duration (sec) | Depth of interest |
| `screenPageViewsPerSession` | Pages per session | Exploration depth |
| `conversions` | Conversion count | Business value |
| `eventCount` | Total events | Activity level |
| `userEngagementDuration` | Total engagement time (sec) | Time invested |

### Custom User Properties

If the site tracks custom user attributes (e.g., membership level, plan type), query them via:

```bash
python scripts/ga4_query.py \
    --dimensions "customUser:membership_level" \
    --metrics sessions,totalUsers,engagementRate,conversions \
    -o "$DATA_DIR/data/ga4_persona_custom.json"
```

> Custom user properties must be registered in GA4 Admin > Custom definitions before querying via API.
