# Example: SEC Filing Analysis

This shows how the agent detects, summarizes, and evaluates an SEC filing against the user's thesis.

---

**Agent:** *(immediate alert — impact score ≥ 7)*

🚨 **SEC Filing Alert — MSFT 8-K (Material Event)**

**Filing:** Form 8-K | Filed: March 15, 2026, 5:47 PM ET
**Items:** Item 1.01 (Entry into a Material Definitive Agreement), Item 8.01 (Other Events)
**EDGAR URL:** https://www.sec.gov/Archives/edgar/data/789019/000078901926000045/msft-20260315.htm

---

**Summary:**

Microsoft has entered into a definitive agreement to acquire DataMesh Inc., a private enterprise data integration company, for approximately $4.2 billion in cash. The acquisition is expected to close in Q3 2026, subject to regulatory approval.

Key details from the filing:
- **Purchase price:** $4.2B cash (funded from existing reserves — no debt issuance)
- **Strategic rationale:** DataMesh's technology will be integrated into Azure's data platform to enable "seamless AI-ready data pipelines" for enterprise customers
- **Revenue impact:** DataMesh has ~$380M ARR, growing 45% YoY. Expected to be accretive to Azure's growth rate within 2 quarters
- **Regulatory note:** Filing indicates Microsoft expects standard HSR review with no significant antitrust concerns given DataMesh's market size

---

**Thesis Evaluation:**

🤖 **Impact: ACCELERATING** 📈 (Score: 8/10)

Your MSFT thesis: *"Enterprise AI adoption will accelerate cloud revenue growth."*

This acquisition directly reinforces the thesis:
1. DataMesh solves one of the biggest enterprise AI adoption blockers — messy, siloed data. Companies can't deploy AI workloads on Azure if their data isn't pipeline-ready.
2. $380M ARR at 45% growth adds fuel to Azure's revenue line, which just had guidance raised to 32-34%.
3. Cash acquisition (no dilution) from existing reserves — financially clean execution.
4. The "AI-ready data pipelines" framing signals Microsoft is building the full enterprise AI stack, not just selling compute.

**Cumulative MSFT thesis status: ACCELERATING** (4 bullish signals in 14 days, 0 bearish)

⚠️ *This is information only, not financial advice.*

---

**User:** "What about that Form 4 filing from the CFO we saw last week? Should I be worried about insider selling?"

**Agent:**

Good question. Here's the context on that Form 4:

**Filing:** Form 4 | Filed: March 10, 2026
**Insider:** Amy Hood, CFO
**Transaction:** Sold 5,000 shares at $423.15 ($2.1M total)

**Context that matters:**
- This was a **pre-planned sale** under a 10b5-1 trading plan, which means it was scheduled months in advance — not a reaction to current events.
- Amy Hood has executed similar sales at roughly this cadence every quarter for the last 3 years. This is routine portfolio diversification.
- Her remaining holdings: ~235,000 shares (~$99M). She sold ~2% of her position.
- **Cluster analysis:** No other MSFT insiders filed Form 4s this month. If 3+ insiders were selling simultaneously outside of planned sales, that would be a much stronger signal.

**Bottom line:** This is noise, not signal. Routine 10b5-1 plan execution. Impact: **2/10**.

For comparison, here's what insider selling that *should* concern you looks like:
- Multiple C-suite insiders selling within the same week
- Sales outside of pre-planned 10b5-1 plans
- Selling that immediately precedes negative news
- Sales that represent a large % of the insider's holdings (>20%)

None of those apply here.

⚠️ *This is information only, not financial advice.*

---

**User:** "Pull up all MSFT filings from this month."

**Agent:**

📋 **MSFT SEC Filings — March 2026**

| Date | Form | Summary | Impact |
|------|------|---------|--------|
| Mar 15 | 8-K | DataMesh acquisition ($4.2B) | 8/10 |
| Mar 10 | Form 4 | CFO sold 5,000 shares (10b5-1 plan) | 2/10 |
| Mar 7 | 8-K | Updated credit facility agreement — routine refinancing | 1/10 |
| Mar 3 | DEF 14A | Proxy statement for annual meeting. No unusual proposals. | 1/10 |

**Filing activity is normal for a company of MSFT's size.** The DataMesh acquisition is the only material event this month.

Want me to do a deeper dive on any of these?

⚠️ *This is information only, not financial advice.*

---

*This example demonstrates: immediate filing alerts for high-impact events, detailed filing summarization, thesis evaluation against specific filings, insider trading context and cluster analysis, historical filing retrieval, and consistent financial disclaimers.*
