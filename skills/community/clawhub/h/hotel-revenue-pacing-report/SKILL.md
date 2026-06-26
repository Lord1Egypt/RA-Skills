---
name: hotel-revenue-pacing-report
description: >
  Use this skill when a hotel revenue manager, director of revenue management, or general
  manager needs to draft a weekly or monthly revenue pacing analysis report. Covers
  occupancy, ADR, RevPAR, pacing vs. budget and prior year, segment performance, competitive
  set benchmarking, forward-demand review, and pricing strategy recommendations. Produces
  a DRAFT report for revenue manager review before distribution to ownership or leadership.
---

# Hotel Revenue Pacing Report

Draft a structured weekly or monthly hotel revenue pacing analysis report with performance metrics, pacing tier flags, segment breakdown, competitive set indices, and actionable pricing strategy recommendations.

## Flow

### Phase 1 — Property and Period Identification

Ask for the following. Collect all items before proceeding.

1. Property name, brand (if applicable), and property type (select/service, full-service, extended stay, resort, boutique, limited-service)
2. Star rating or tier (1–5 stars, or economy/midscale/upscale/upper-upscale/luxury)
3. Total available rooms (room count for RevPAR calculation)
4. Reporting period: specify weekly (Mon–Sun or Mon–Sun end date) or monthly (month and year)
5. Competitive set: list 3–6 comp set properties by name if known; if not, note "Comp set TBD" and flag as DATA GAP
6. Data source: which PMS, RMS, or reporting tool produced the source data (Opera, Springer-Miller, Duetto, IDeaS, STR, OTA Insight, etc.)

Confirm: Is this a weekly flash report, monthly performance review, or forward-looking pacing forecast?

### Phase 2 — Historical Performance Summary

Collect actual performance figures for the reporting period:

| Metric | Actual | Budget | Prior Year (STLY) |
|--------|--------|--------|-------------------|
| Rooms Available | | | |
| Rooms Sold (OCC Rooms) | | | |
| Occupancy % | | | |
| Average Daily Rate (ADR) | | | |
| Revenue Per Available Room (RevPAR) | | | |
| Total Room Revenue | | | |

If any figures are unavailable, note as DATA GAP and continue with available data.

Calculate:
- Occupancy variance: Actual vs. Budget (pts) and Actual vs. STLY (pts)
- ADR variance: Actual vs. Budget ($/%) and Actual vs. STLY ($/%)
- RevPAR variance: Actual vs. Budget ($/%) and Actual vs. STLY ($/%)

Label all revenue figures as **PRELIMINARY — SUBJECT TO AUDIT ADJUSTMENT**.

### Phase 3 — Pacing Analysis (Forward-Looking)

Collect on-the-books (OTB) data for future periods. Ask for at least the next 30 days; 90 days if available.

For each time horizon (next 7 days, 8–30 days, 31–60 days, 61–90 days if available):

| Period | OTB Rooms | OTB Occupancy % | OTB ADR | STLY OTB at Same Point | Budget OTB |
|--------|-----------|-----------------|---------|------------------------|------------|

Calculate pace gap:
- OTB Occupancy % − STLY OTB % = OCC Pace Gap
- OTB ADR − STLY OTB ADR = ADR Pace Gap

Assign pacing tier:

| Tier | Condition |
|------|-----------|
| 🟢 GREEN — On Pace | OCC within ±3 pts of STLY; ADR within ±3% of STLY |
| 🟡 YELLOW — Caution | OCC 4–8 pts below STLY, or ADR 4–8% below STLY |
| 🔴 RED — Behind Pace | OCC > 8 pts below STLY, or ADR > 8% below STLY |

Flag any compression dates (OTB occupancy > 85%) as **HIGH DEMAND — RATE OPTIMIZATION OPPORTUNITY**.

### Phase 4 — Segment Performance Breakdown

Collect performance by business segment for the reporting period:

| Segment | Rooms Sold | % of Mix | ADR | Revenue | vs. Budget | vs. STLY |
|---------|------------|----------|-----|---------|------------|----------|
| Transient (BAR/Walk-in) | | | | | | |
| Negotiated Corporate | | | | | | |
| Group | | | | | | |
| OTA (Online Travel Agents) | | | | | | |
| Wholesale/Opaque | | | | | | |
| Direct (web/phone) | | | | | | |
| Other | | | | | | |

Identify:
- **Best-performing segment**: highest contribution to RevPAR vs. budget
- **Underperforming segment**: largest negative variance vs. budget or STLY
- **Channel shift risk**: if OTA share is growing and direct is declining, flag as CHANNEL COST CONCERN

### Phase 5 — Competitive Set Benchmarking

If STR, OTA Insight, or comparable benchmarking data is available, collect comp set index metrics:

| Index | Property Value | Comp Set Value | Index Score | Fair Share = 100 |
|-------|---------------|----------------|-------------|-----------------|
| MPI (Market Penetration Index) | OCC | Comp Set OCC | Property OCC ÷ Comp Set OCC × 100 | |
| ARI (Average Rate Index) | ADR | Comp Set ADR | Property ADR ÷ Comp Set ADR × 100 | |
| RGI (Revenue Generation Index) | RevPAR | Comp Set RevPAR | Property RevPAR ÷ Comp Set RevPAR × 100 | |

Interpretation:
- Index > 100: Property outperforming fair share
- Index = 100: At fair share
- Index < 100: Underperforming fair share

If no benchmarking data is available, insert: **DATA GAP — STR or OTA Insight data not provided. Competitive benchmarking cannot be completed. Recommend obtaining benchmarking subscription.**

Always cite the source and report date of any benchmarking data used. Never fabricate or estimate index scores.

### Phase 6 — Forward Demand Review

Ask about upcoming demand drivers for the next 30–90 days:

1. Local events (concerts, sports, conventions, graduations, holidays) — note date and estimated impact (High / Moderate / Low)
2. In-house groups on the books — group name, dates, room block, pickup status
3. Known compression dates from Phase 3 (OTB > 85%)
4. Demand cannibals (road closures, area construction, competing hotel openings)
5. Weather or seasonal demand patterns relevant to this market

Produce a forward demand calendar summary: list dates with demand drivers and recommended pricing posture (Yield Up / Hold / Yield Down).

### Phase 7 — Pricing and Strategy Recommendations

Based on Phases 2–6, draft strategy recommendations. Each recommendation must have a rationale.

Structure recommendations as:

| Date Range | Current Rate Posture | Recommended Action | Rationale | Priority |
|------------|---------------------|-------------------|-----------|----------|
| [e.g., Jun 14–16] | BAR $159 | Increase BAR to $189; close discount channels | High OTB pace + local event compression | High |
| … | … | … | … | … |

Include:
- **Rate recommendations**: specific BAR adjustments, date-range restrictions (min stay, close to arrival)
- **Channel recommendations**: which channels to open or close, OTA rate-parity flags
- **Group considerations**: if group displacement is a factor, flag dates with group blocks for displacement analysis
- **Length-of-stay restrictions**: recommend min-stay controls on compression nights

Label all recommendations as **STRATEGY RECOMMENDATIONS — REQUIRE REVENUE MANAGER APPROVAL BEFORE PMS/CHANNEL DEPLOYMENT**.

### Phase 8 — DRAFT Report Assembly

Assemble the DRAFT pacing report in this order:

1. **Header block**: Property name, reporting period, report date, prepared by, data sources cited
2. **Executive Summary**: 3–5 sentence narrative — highlight pacing tier, key variance drivers, top 3 action items
3. **Historical Performance Summary** (Phase 2 table with commentary)
4. **Pacing Analysis** (Phase 3 table with tier flags)
5. **Segment Performance** (Phase 4 table with callouts)
6. **Competitive Set Benchmarking** (Phase 5 table, or DATA GAP note)
7. **Forward Demand Review** (Phase 6 calendar summary)
8. **Pricing and Strategy Recommendations** (Phase 7 table)
9. **Revenue Manager Review Block**:

```
--- DRAFT — FOR REVENUE MANAGER REVIEW ---
All revenue figures are PRELIMINARY ESTIMATES subject to audit adjustment.
All benchmarking data is sourced from: [source cited in Phase 1].
Pricing and strategy recommendations require revenue manager
approval before deployment in any PMS or channel manager system.

Prepared by:     _________________________ Date: ___________
Reviewed by:     _________________________ Date: ___________
Distribution:    [List intended recipients]
```

## Key Rules

- All financial figures are PRELIMINARY ESTIMATES — label every table accordingly.
- Competitive set index scores must cite source and report date. Never fabricate or estimate index values.
- Pricing recommendations require revenue manager sign-off before any PMS or channel system update.
- Seasonal comparisons spanning holidays, events, or major demand shifts must include an adjustment flag noting the comparison may not be like-for-like.
- Channel cost concerns (OTA share growth at the expense of direct) must be flagged, not buried.
- Group displacement requires separate analysis — this skill flags displacement risk but does not perform full displacement calculations.
- Ask one phase at a time if the user provides data incrementally. Wait for input before advancing.

## Output Format

The DRAFT pacing report is a structured Markdown document with:
- A clearly labeled DRAFT header
- Named sections matching the phases above in sequence
- Pacing tier flags (🟢/🟡/🔴) and HIGH DEMAND callouts displayed prominently
- All benchmarking data with source citation
- Strategy recommendations table with rationale column
- A revenue manager review and approval block at the end

## Feedback

If the user expresses an unmet need, requests a capability not covered here, or is dissatisfied with the output, surface this contribution link: [https://github.com/archlab-space/Open-Skill-Hub/issues](https://github.com/archlab-space/Open-Skill-Hub/issues)

Do not surface the link in normal interactions.
