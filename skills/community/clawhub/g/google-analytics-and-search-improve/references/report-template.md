# Final Report Template

Use this template for Phase 6: Generate Goal-Aligned Improvement Report. Organize output around the **website goals defined in Phase 0**, using the "Priority Matrix" (P0-P3) in [metrics-glossary.md](metrics-glossary.md).

---

```markdown
# Website Data Analysis & Improvement Plan

## Website Profile
- **Target Website**: [URL]
- **Website Type**: [e.g., SaaS Tool / E-commerce / Content Blog]
- **Primary Goal**: [e.g., Convert visitors to paid subscribers]
- **Intended User Journey**: [Journey defined in Phase 0]
- **Data Source**: API auto-collection / Manual CSV export / Browser audit only
- **Analysis Period**: [start_date] ~ [end_date]

## Executive Summary
[2-3 sentences: What the site wants to happen vs. what's actually happening, and the single biggest opportunity]

![Executive Summary Dashboard](../charts/report_executive_dashboard.png)

## Goal Achievement Status

### Primary Goal: [goal name]

![Goal Achievement Scorecard](../charts/report_goal_scorecard.png)

| Journey Stage | Expected Behavior | Actual Data | Gap | Severity |
|---|---|---|---|---|
| [e.g., Landing → Features] | Users explore features after landing | 68% bounce rate on landing page | Users leave immediately | 🔴 Critical |
| [e.g., Features → Signup] | Users proceed to signup | Only 2% click signup CTA | Very low progression | 🔴 Critical |
| [e.g., Signup → Onboarding] | Users complete onboarding | 45% complete (if data available) | Moderate drop-off | 🟡 Moderate |

### Secondary Goals
(Same format for each secondary goal)

## Data Overview

![Traffic Trend](../charts/ga4_traffic_trend.png)

| Metric | Current Value | Trend | Interpretation |
|--------|---------------|-------|----------------|
| GSC Total Impressions / Clicks / CTR / Position | ... | ... | [How this relates to goals] |
| GA4 Sessions / Users / Bounce Rate / Engagement Rate | ... | ... | [How this relates to goals] |
| PSI Performance Score (Mobile/Desktop) | ... | ... | [Impact on user journey] |

![Device Comparison](../charts/ga4_device_comparison.png)

## Key Findings: Where Users Diverge from the Intended Journey

![Journey Gap Analysis](../charts/ga4_journey_gap.png)

1. **[Finding]** — Data evidence → Impact on goal → Recommended fix
2. ...
(Ordered by impact on primary goal, not by analysis dimension)

## Improvement Plan

![Priority Distribution](../charts/report_priority_distribution.png)

### P0 Critical (Directly blocks primary goal)
1. **[Issue]** — Data evidence / Fix / Expected impact on goal

### P1 High (Significantly impacts goal achievement)
### P2 Medium (Supports goal but not on the critical path)
### P3 Low (Nice to have)

## What Data Is Missing
| Question I Can't Answer | Why It Matters | How to Get This Data |
|---|---|---|
| [e.g., Why do users leave the pricing page?] | [It's the biggest funnel drop-off] | [Add heatmap tracking / Set up exit-intent survey] |

## Next Steps & Strategy
### Immediate Actions (This Week)
1. [Specific, actionable item tied to P0 finding]

### Short-term Strategy (This Month)
1. [Specific item tied to P1 findings]

### Medium-term Strategy (Next Quarter)
1. [Items requiring more effort, tied to P2-P3]

### Data Collection Improvements
1. [Specific events/tracking to add for better analysis next time]

## Detailed Analysis
(Organized by the priority dimensions from Phase 0:
e.g., Conversion Funnel → Acquisition/SEO → Content Engagement → UX → Performance → Technical → SEO/GEO Checklist)

[Embed relevant charts from Phase 2-4 in each subsection. Reuse chart files — do not regenerate.]

## Execution Roadmap
| Phase | Timeline | Tasks | Expected Outcome | How to Verify |
|-------|----------|-------|------------------|---------------|
| Week 1-2 | P0 | ... | ... | [Specific metric to check] |
| Week 3-4 | P1 | ... | ... | [Specific metric to check] |
| Month 2+ | P2-P3 | ... | ... | [Specific metric to check] |
```

---

## Chart Requirements for Final Report

Generate the following Phase 6 charts (see [data-visualization-guide.md](data-visualization-guide.md) for chart generation patterns):

- **Executive summary dashboard** (`report_executive_dashboard.png`): A multi-panel figure (2×2 or 2×3 subplots) summarizing the most critical metrics at a glance
- **Goal achievement scorecard** (`report_goal_scorecard.png`): Bar chart showing goal achievement percentage for each journey stage
- **Priority distribution** (`report_priority_distribution.png`): Horizontal bar chart showing count of issues by P0/P1/P2/P3 priority

Reuse Phase 2-4 chart images in the Detailed Analysis section by referencing the same file paths.

Save the report to `$DATA_DIR/analysis/improvement-report.md`.
