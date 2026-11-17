# Skill: Programmatic SEO Content Scale Architecture (pSEO Matrix Builder)

## Description
This skill provides comprehensive, end-to-end instructions for designing, structuring, and generating Programmatic SEO (pSEO) page templates and relational datasets. It enforces strict quality thresholds to ensure large-scale landing pages pass search engine helpfulness algorithms while targeting long-tail commercial and informational search intent.

---

## System Instructions & Protocol

### 1. Dataset & Variable Architecture Mapping
- **Seed Pattern Definition**: Identify base query patterns (e.g., `[Service] in [City]`, `[Tool A] vs [Tool B] for [Use Case]`).
- **Entity Variable Extraction**: Define primary keys and modifier variables:
  - `{primary_entity}`: The main subject or target topic.
  - `{location_modifier}`: Geo-targeting parameters (city, state, zip code).
  - `{feature_modifier}`: Specific product/service attributes or comparative data points.
  - `{target_audience}`: User demographic or industry vertical.

### 2. Programmatic Page Layout Blueprint
For every programmatic template, generate a modular section breakdown:
1. **Dynamic Hero Section**: H1 header with exact variable placement + direct value proposition block (50 words).
2. **Data-Driven Comparison / Metrics Matrix**: Dynamic Markdown comparison table populated via dataset variables.
3. **Contextual Use-Case Breakdown**: H2 sections that dynamically adapt based on variable attributes (avoiding repetitive copy).
4. **Structured Data Injection**: Auto-generate valid `<script type="application/ld+json">` code populated with dynamic page variables.

### 3. Thin Content & Penalty Avoidance Safeguards
- Ensure a minimum of **30–40% unique variable content** per page (unique data points, custom conditional paragraphs).
- Enforce strict Canonical URL mapping to prevent duplicate parameter indexing.
- Implement conditional rendering logic (e.g., if dynamic attribute is missing, suppress the section instead of outputting blank spaces).

### 4. Hub-and-Spoke Programmatic Internal Linking
- Build automated breadcrumb navigation paths.
- Generate parent hub category pages that dynamically aggregate child programmatic URLs.
- Include "Related Entities in [Region]" or "Alternative Comparisons for [Use Case]" contextual linking widgets.

---

## Workflow Execution Steps

1. **Input Phase**: Analyze input database structure, key variables, and target search patterns.
2. **Template Design Phase**: Output the complete programmatic Markdown blueprint with `{variable}` placeholders.
3. **Data Schema Phase**: Generate sample JSON / CSV formatting rules for dataset ingestion.
4. **SEO & Schema Output**: Generate dynamic Meta Title, Meta Description, and JSON-LD markup patterns.

---

## Reference Benchmarks
- [Google Search Central - Scaled Content Guidelines](https://developers.google.com/search/docs/advanced/guidance/scaled-content)
- [W3C Web Architecture Standards](https://www.w3.org/TR/html5/)
