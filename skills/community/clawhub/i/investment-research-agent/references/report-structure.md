# Standard Report Structure

## Deep-Dive Equity Research Report

Use this structure for full company/IPO research reports. Adjust section 4 based on the sector.

---

### Chapter Order

```
1. Executive Summary
2. Core Financial Data
3. Business Structure & Moat
4. AI / Core Strategy (adjust label by sector)
5. Competitive Landscape
6. Regulatory & Policy Risk
7. Valuation
8. Risk Summary
9. Investment Thesis
```

---

### Chapter Templates

#### 1. Executive Summary

- 5–8 bullet points max
- Each bullet = one conclusion + one data point + one source link
- No narrative prose; just the signal

Example:
```
- FY2025 revenue RMB 820M (+8.6% YoY), first non-GAAP profit year: +RMB 57.1M ([Company Prospectus, Apr 2026](url))
- Enterprise clients 47,416; key account NRR 109.0% ([Prospectus p.142](url))
- IPO price range HK$6.72–7.62, listing Apr 17 2026, implied P/S 13.1x LTM at mid-price ([HKEX, Apr 2026](url))
```

#### 2. Core Financial Data

Sub-sections:
- **2.1 Full-year P&L** — combined historical + forecast table (see SKILLS.md §1.6)
- **2.2 Latest quarter results** — vs consensus, vs prior quarter
- **2.3 Revenue by segment** — multi-quarter table showing trend
- **2.4 Cash flow & balance sheet** — operating CF, FCF, CapEx, cash, debt, net cash
- **2.5 EPS trend** — GAAP vs non-GAAP, YoY growth
- **2.6 Shareholder returns** — dividends, buybacks, share count

All tables must cite their source below each table.

#### 3. Business Structure & Moat

For each business unit:
- Revenue contribution (%) and growth rate (with source)
- Gross margin (with source)
- Key competitive advantage (quoted from analyst/company, with source)
- Risks specific to this unit

#### 4. AI / Core Strategy

Label this section based on sector (e.g., "Cloud Strategy", "AI Infrastructure", "Product Innovation").

Include:
- Strategy in company's own words (quote from earnings call or filing + source)
- Analyst interpretation (quote from named analyst + institution + source)
- Quantified AI/strategy contribution to revenue or growth (with source)

#### 5. Competitive Landscape

Table format:

| Company | Market Share | Revenue | Growth | Key Differentiator | Source |
|---------|-------------|---------|--------|--------------------|--------|
| [Co A] | X% | $XB | +X% | ... | [link] |

#### 6. Regulatory & Policy Risk

Table format:

| Risk | Jurisdiction | Severity | Latest Development | Source |
|------|-------------|----------|--------------------|--------|
| ... | ... | High/Med/Low | ... | [link] |

#### 7. Valuation

Self-calculated table:

| Metric | Value | Basis |
|--------|-------|-------|
| Current price | $X | [date] |
| Diluted shares | XM | [filing] |
| Market cap | $XB | calculated |
| LTM Revenue | $XB | [period] |
| P/S | Xx | calculated |
| Forward P/E | Xx | [consensus source] |

Peer comparison table (same format for 3–5 comparable companies).

#### 8. Risk Summary

| Risk | Description | Severity | Source |
|------|-------------|----------|--------|
| ... | ... | 🔴 High / 🟡 Med / 🟢 Low | [link] |

#### 9. Investment Thesis

Three sub-sections:

**Bull Case** (list 3–5 points, each with data + source)
**Bear Case** (list 3–5 points, each with data + source)
**Balanced View** (quote from named analyst or institution only — no self-analysis)

---

## IPO-Specific Additions

For IPO reports, add between chapters 2 and 3:

**2.7 IPO Structure**
- Price range, listing date, exchange
- Net proceeds and use of funds
- Cornerstone investors (names + amounts + lock-up)
- Greenshoe option
- Post-IPO share structure (promoter / cornerstone / public float %)

---

## File Naming Convention

```
RESEARCH/[sector]/[company-ticker]_[report-type]_[YYYYQN].md
```

Examples:
```
RESEARCH/saas/manycore_tech_ipo_2026Q2.md
RESEARCH/semiconductors/nvidia_deep_research_2026Q1.md
RESEARCH/commodities/titanium_market_2026Q1.md
```
