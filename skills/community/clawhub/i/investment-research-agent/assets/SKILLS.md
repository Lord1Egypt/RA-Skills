# SKILLS.md — Research Methodology & Hard Rules

> This file records all hard requirements for report quality and work process.
> **Must be read before starting any task.**

---

## 1. Report Writing — Non-Negotiable Rules

### 1.1 Inline Source Links — Top Priority

**Every single data point must be immediately followed by a source link. No exceptions.**

Format:
- Inline: `data point ([Source Name, Date](URL))`
- Below table: `*Source: [Source Name, Date](URL)*`
- Multiple sources: `*Sources: [A](url1); [B](url2)*`

✅ Correct:
```
AWS Q3 2025 revenue **$27.5B** (+19% YoY) ([Amazon IR, Oct 2025](https://ir.aboutamazon.com/...))
```

❌ Wrong:
```
AWS Q3 revenue $27.5B (+19%)  ← no source link
(References listed at end of document) ← insufficient; must be inline
```

### 1.2 Audience — Professional Investors Only

Reports are for **professional investors**, not general readers.

❌ Do not write:
- Basic concept definitions ("what is cloud computing", "what is a moat")
- Industry background introductions
- Overly generic company overviews

✅ Start directly with:
- Key conclusions summary (with data)
- Core financial metrics
- Business moat analysis (data-supported)
- Competitive landscape
- Valuation

### 1.3 File Naming — Full English

All report file paths and filenames must be **full English** — no CJK characters.

✅ Correct: `RESEARCH/tech/nvidia_deep_research_2026Q1.md`
❌ Wrong: `RESEARCH/科技/英伟达研究报告.md`

### 1.4 Data Recency Requirements

| Data Type | Requirement |
|-----------|-------------|
| Commodity / asset prices | **Must be within 12 months**; note the date |
| Financial data | **Must include the latest published period** (latest Q/H/annual report) |
| Analyst forecasts | **Must include** [current year+1]E / [+2]E / [+3]E |
| Stock price & market cap | Note data date; use for valuation calculations |

### 1.5 Valuation Multiples — Must Self-Calculate

**Do not copy valuation figures from third parties. Always calculate independently.**

Steps:
1. Fetch latest trading price × diluted share count = market cap
2. Pull latest financial report: revenue / net income / EBITDA
3. Calculate P/S, P/E, EV/EBITDA independently

Valuation table format:

| Company | Price | Mkt Cap | Revenue (LTM) | P/S | Net Income | P/E |
|---------|-------|---------|---------------|-----|------------|-----|
| NVDA | $183 | $4.5T | $130B | 34x | $73B | 61x |

### 1.6 Revenue Table — Historical + Forecast Combined

Historical actuals and analyst forecasts **must appear in a single combined table**.

| FY | FY2023A | FY2024A | FY2025A | 2026E | 2027E | 2028E |
|----|---------|---------|---------|-------|-------|-------|
| Revenue | $X | $X | $X | $X | $X | $X |
| YoY | +X% | +X% | +X% | +X% | +X% | +X% |

### 1.7 No Self-Analysis — Highest Priority Rule

**Unless explicitly instructed by the principal, never add personal analysis or judgment.**

✅ Allowed:
- Collecting, quoting, and organizing analyst/brokerage/media statements verbatim
- Structurally presenting multi-source findings without personal commentary
- Labeling sources so the principal can judge independently

❌ Prohibited:
- "I think...", "Overall...", "This suggests..."
- Drawing conclusions without an external source
- Extending or interpreting beyond what the source actually says

---

## 2. Standard Report Structure

```
1. Executive Summary (with data + inline sources)
2. Core Financial Data
   2.1 Full-year / latest annual P&L
   2.2 Latest quarter results
   2.3 Revenue by segment (multi-quarter trend)
   2.4 Cash flow & balance sheet
   2.5 Historical EPS growth trend
   2.6 Shareholder returns (dividends + buybacks)
3. Business Structure & Moat Analysis (by business line)
4. AI / Core Strategy Analysis (adjust by sector)
5. Competitive Landscape
6. Regulatory & Policy Risk
7. Valuation (self-calculated multiples + peer comparison)
8. Risk Summary (table: risk / severity / source)
9. Investment Thesis (bull / bear / balanced view)
```

---

## 3. Data Collection Rules

### 3.1 Source Priority

| Priority | Source Type | Examples |
|----------|-------------|---------|
| ⭐⭐⭐⭐⭐ | Official filings / IR sites (SEC, company IR) | `sec.gov`, `ir.nvidia.com` |
| ⭐⭐⭐⭐⭐ | Official press releases (Q earnings releases) | company newsroom |
| ⭐⭐⭐⭐ | Authoritative financial media | CNBC, Reuters, Bloomberg, Yahoo Finance |
| ⭐⭐⭐⭐ | Professional research firms | Futurum, Constellation Research |
| ⭐⭐⭐ | Data aggregators | StockAnalysis, MacroTrends |
| ⭐⭐ | Trade media | sector-specific publications |
| ⭐ | Forums / communities | Cross-verification only; never primary source |

### 3.2 Required Financial Data Checklist

For every company report:
- [ ] Latest full fiscal year: revenue, gross profit, operating profit, net income, EPS
- [ ] Latest quarter: above metrics + segment breakdown
- [ ] Cash flow: operating CF, free CF, CapEx
- [ ] Balance sheet: cash, debt, net cash
- [ ] Shareholder returns: dividends, buybacks, share count change
- [ ] Analyst consensus: [Y+1]E / [Y+2]E / [Y+3]E revenue and EPS, with source
- [ ] Valuation: latest price, market cap (self-calculated), P/E, P/S

---

## 4. Workflow Rules

### 4.1 On Receiving a Task

1. Reply: **"✅ Received, starting: [brief task description]"**
2. Read `SKILLS.md` (this file)
3. Check `memory/YYYY-MM-DD.md` (today + yesterday)
4. Begin execution

### 4.2 On Completing a Report

1. Save report to correct path (full English)
2. Log key findings in `memory/YYYY-MM-DD.md`
3. Update `MEMORY.md` with any new standing instructions
4. Send `.md` file to principal via messaging channel

### 4.3 File Delivery

- **Always send the `.md` file** (do not paste content into chat)
- Cloud documents are optional; `.md` file is mandatory

---

## 5. Memory Update Rules

After completing each task, update:

**`memory/YYYY-MM-DD.md` (daily log):**
- Task completed
- Key data findings
- Any new instructions from principal (clearly flagged)
- Output file path

**`MEMORY.md` (long-term memory):**
- Principal preference updates
- Important research conclusions (for traceability)
- New rules learned (summary)

**`SKILLS.md` (this file):**
- When principal gives new format/process requirements → update immediately
- When a redo/error occurs → add a "lesson learned" note
