# Research Methodology — Full Reference

## Why These Rules Exist

These rules were developed through repeated iteration on real research tasks. Each rule has a concrete reason:

| Rule | Why It Exists |
|------|---------------|
| Inline source links | End-of-document references make it impossible to verify individual claims quickly |
| No self-analysis default | The agent's role is research aggregation, not advisory; the principal makes the judgment |
| English file paths only | CJK characters in filenames cause encoding issues across systems and tools |
| Price data ≤ 12 months | Stale prices mislead valuation; markets move fast |
| Self-calculated multiples | Third-party aggregators frequently have stale or incorrect data |
| Latest financial period required | Investment decisions require current, not historical, financials |

---

## Data Source Usage Guide

### SEC Filings (⭐⭐⭐⭐⭐)

Best for: 10-K, 10-Q, 20-F, 6-K, S-1/F-1 (IPO prospectus), proxy statements

```
https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=[TICKER]&type=10-K
```

Key data points: exact revenue figures, segment breakdown, risk factors, management discussion

### Exchange Filings (⭐⭐⭐⭐⭐)

- HKEX: `https://www1.hkexnews.hk/`
- SSE (Shanghai): `https://www.sse.com.cn/`
- SZSE (Shenzhen): `https://www.szse.cn/`

### Earnings Call Transcripts (⭐⭐⭐⭐)

Sources: Motley Fool, Seeking Alpha, Yahoo Finance, company IR
Key data: management guidance, qualitative color, Q&A

### Analyst Consensus Data (⭐⭐⭐⭐)

- StockAnalysis.com — free, reliable, covers US stocks
- TipRanks — analyst ratings + price targets
- MarketBeat — analyst consensus ratings

Format for citing analyst consensus:
```
Analyst consensus (StockAnalysis, Apr 2026): Strong Buy, avg price target $264.54 (+43.8% upside), 39 analysts
```

---

## Anti-Patterns (Do Not Do)

### ❌ Clustering sources at document end

```markdown
## References
1. SEC 10-K (2025)
2. Bloomberg consensus
3. Reuters report
```

This makes individual claims unverifiable. **Every data point needs its own link.**

### ❌ Copying valuation multiples

"According to Morningstar, NVDA trades at 61x forward P/E"

→ Pull the current stock price and diluted share count, pull EPS from the latest filing, calculate independently.

### ❌ Using outdated price data

"Titanium sponge prices reached 52,000 RMB/ton in 2023"

→ If writing in 2026, this is 3-year-old data. Find a source from the last 12 months.

### ❌ Industry background introductions

"Oracle was founded in 1977 by Larry Ellison..."
"Cloud computing refers to on-demand access to..."

→ Skip. Professional investors know this. Start with the data.

### ❌ Self-analysis without a source

"This suggests Oracle's AI strategy is well-positioned..."
"Overall, the valuation looks attractive at these levels..."

→ If this is the agent's own view and not from an external source, it is prohibited by default. Quote a specific analyst or institution instead.

---

## Handling Missing Data

When a required data point cannot be found:
- State clearly: "Analyst consensus data for [company] not available — company is pre-IPO / insufficient coverage"
- Do not substitute with unverified estimates
- Note what was searched and where
- If partial data exists, present it and flag what is missing

---

## PDF / Prospectus Analysis

For large PDFs (IPO prospectuses, annual reports):
- Use `pdfminer.six` for text extraction when direct API upload fails
- Extract in page ranges to avoid token limits
- Key sections to prioritize: financials, risk factors, use of proceeds, shareholder structure
- Always note the document version and date

Install if needed:
```bash
pip install pdfminer.six
# 推荐在虚拟环境中安装：
# python -m venv venv && source venv/bin/activate && pip install pdfminer.six
```

Basic extraction:
```python
from pdfminer.high_level import extract_text
text = extract_text('prospectus.pdf', page_numbers=list(range(0, 50)))
```
