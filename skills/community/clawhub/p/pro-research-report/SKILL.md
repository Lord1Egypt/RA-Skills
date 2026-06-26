---
name: industry_research_report
description: >
  生成行业深度研究报告。当用户的请求中包含行业关键词、行业名称，并且意图是了解某个行业、生成行业研究报告、行业分析时，触发此 Skill。
  典型触发场景包括但不限于：用户提到"XX行业研究"、"XX行业报告"、"帮我分析XX行业"、"XX产业深度研究"、"XX领域市场分析"等。
  即使用户没有明确说"报告"二字，只要意图是围绕某个行业主体进行深度研究或分析，都应触发此 Skill。
---

# Industry Research Report Writer

## Overview

This skill produces professional industry research reports by executing a strict 4-phase workflow: Research → Report Writing → Fact-Checking → Document Formatting. It delivers comprehensive, data-driven reports with integrated charts and visualizations, outputting final deliverables in Markdown, DOCX, and PDF formats.

**You are a research report generation agent, NOT a Q&A chatbot. Your ONLY output is professionally formatted research reports (DOCX + PDF), never direct answers in conversation.**

## Workflow

The report creation follows a strict sequential process. **ALL 4 steps are mandatory. NEVER skip any step.**

### Step 1: Research Phase

Conduct comprehensive industry research using trusted financial sources.

#### 1.1 Current Date Awareness
- **Always include the current year** in search queries for time-sensitive data
- **Specify date ranges** when searching for recent news or developments
- **Use "latest" or current year** keywords to ensure up-to-date results

#### 1.2 Multilingual Search Strategy

**For comprehensive research, search in BOTH Chinese and English:**

| Industry/Topic Focus | Primary Language | Secondary Language |
|---------------------|------------------|-------------------|
| China market, Chinese companies | Chinese (中文) | English |
| Global/Western markets | English | Chinese (for China angle) |

**Search Query Examples:**
- "广联航空 300900 行业研究 2026"
- "EV battery market size 2026"
- "半导体行业 发展趋势 2026"

#### 1.3 Data Collection

**Quantitative Data:**
- Market size and forecasts, Growth rates (CAGR), Market share by company/segment, Financial metrics

**Qualitative Data:**
- Industry trends and drivers, Regulatory landscape, Competitive dynamics, Technology developments, Risk factors

#### 1.4 Research Output Files

Save all research materials:

```
docs/
├── research_summary.md
├── market_data.md
├── industry_analysis.md
├── competitive_landscape.md
└── sources_list.md

data/
├── market_metrics.json
└── company_data.json
```

### Step 2: Report Writing Phase (Synthesis + Chart Generation)

Synthesize ALL research materials from Step 1 into ONE comprehensive report.

#### 2.1 Report Writing

**Core Principles:**
- Synthesize ALL research documents into ONE comprehensive report
- Use ONLY existing information — DO NOT fabricate facts
- DO NOT conduct new research beyond provided materials

**Writing Style:**
- Primary Style: Narrative, prose-based format
- Data Integration: Embed statistics naturally within narrative
- Tone: Professional, objective, authoritative third-person voice

#### 2.2 Chart Generation

**CJK Font Setup (MANDATORY before any chart generation):**
```python
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Noto Sans CJK SC"]
plt.rcParams["axes.unicode_minus"] = False
```

**Chart Color Strategy:**
```python
THEME_COLORS = ["#1A1A1A", "#4A4A4A", "#B8860B", "#6B6B6B", "#9B9B9B"]
```

**Key Principle:** Generate charts using Python matplotlib and embed in the report.

### Step 3: Fact-Checking Phase

Extract and verify key data, statistics, and factual claims from the Step 2 report.

- Cross-Reference with Original Research
- Independent Verification (For Critical Facts)
- Distinguish between facts and projections

### Step 4: Document Formatting Phase (DOCX + PDF)

Generate professionally formatted DOCX from the verified report, then convert to PDF.

#### 4.1 Write Professional DOCX

Use `python-docx` to create a professionally formatted DOCX document.

**FORBIDDEN:**
- Generating DOCX without charts (text-only document)
- Converting to PDF before verifying charts are embedded in DOCX

## Report Structure

### Required Sections (All Report Types):
1. Executive Summary
2. Introduction
3. Key Findings
4. Conclusion
5. Sources

### Optional Sections:
- Company Overview (for company-focused reports)
- Market Size & Growth (for industry reports)
- Competitive Landscape
- SWOT Analysis
- Risk Factors

## Source Standards

### Tier 1: Official & Regulatory Sources (Highest Trust)
- Central Banks, Securities Regulators (SEC, CSRC), Government Statistics

### Tier 2: Financial Data Providers
- Bloomberg, Refinitiv, FactSet, S&P Global Market Intelligence

### Tier 3: Research & Analysis
- Investment Banks (Goldman Sachs, Morgan Stanley), Consulting Firms (McKinsey, BCG)

### Tier 4: Industry & Trade Sources
- Industry Associations, Company Filings, Earnings Calls

### Tier 5: News & Media (Verify with Higher Tiers)
- Financial Times, Wall Street Journal, Bloomberg News

## Quality Standards

- All statistics must be cited with sources (include FULL URLs)
- Key findings require verification from at least 2 independent sources
- Reports must include reliability ratings for all sources
- Data should be current (within 12 months unless historical analysis)
- Clear distinction between facts and analysis/projections
- **NEVER cite Wikipedia**

## Output

The final deliverable is a professionally formatted research report in both DOCX and PDF formats, saved to the workspace.

## Common Mistakes to Avoid

- Skipping the research phase and writing directly from user query
- Outputting report content in conversation instead of files
- Skipping fact-checking phase
- Delivering only Markdown without DOCX/PDF
- Fabricating or estimating data without clear labeling
