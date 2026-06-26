# Example: Thesis Tracking

This shows how the agent evaluates incoming data against your investment thesis over time, including a thesis status change alert.

---

**User:** "Add TSLA — 30 shares at free5. My thesis: Tesla's US manufacturing advantage and energy storage business will drive margin expansion that Wall Street is undervaluing."

**Agent:**

✅ Added TSLA to your portfolio:
- **Shares:** 30 @ free5.00 avg cost
- **Thesis:** US manufacturing advantage + energy storage → margin expansion (undervalued)
- **Status:** HOLDING (fresh entry — no signals evaluated yet)

I'm building your TSLA source network now. I'll monitor:
- SEC EDGAR filings (CIK: 0001318605)
- Tesla Investor Relations
- Key competitors: BYD, Rivian, Lucid
- Industry sources: Electrek, InsideEVs, CleanTechnica
- Energy storage publications: Energy Storage News, Utility Dive

You'll see TSLA in your next briefing.

---

*[3 days later — thesis log building up]*

**User:** "How's my TSLA thesis doing?"

**Agent:**

📊 **TSLA Thesis Status: ACCELERATING** 📈

**Your thesis:** US manufacturing advantage + energy storage → margin expansion (undervalued)

**Recent signals (last 7 days):**

| Date | Signal | Source | Impact |
|------|--------|--------|--------|
| Mar 11 | Gigafactory Texas hits full Model Y capacity | Electrek | 📈 Bullish |
| Mar 12 | Q4 energy storage revenue up 113% YoY (10-K detail) | SEC 10-K | 📈 Bullish |
| Mar 13 | BYD European deliveries down 12% in key markets | EU Auto Daily | ➡️ Neutral |
| Mar 14 | Megapack backlog extends to 2028 per IR update | Tesla IR | 📈 Bullish |

**Cumulative assessment:** 3 bullish signals directly supporting your thesis, 1 neutral. The energy storage data from the 10-K is particularly strong — 113% YoY growth validates the "undervalued energy business" component. Gigafactory capacity hitting full production supports the manufacturing advantage angle.

No bearish signals detected this week.

⚠️ *This is information only, not financial advice.*

---

*[2 weeks later — a bearish signal arrives]*

**Agent:** *(immediate alert, not waiting for next briefing)*

⚠️ **TSLA Thesis Alert — Potential Headwind Detected**

**What happened:** The Wall Street Journal reports that Tesla is pausing Megapack production at Lathrop, CA for 3 weeks due to a battery cell supply constraint from CATL. This affects Q2 energy storage delivery estimates.

**Thesis impact: WEAKENING signal** 📉
Your thesis specifically calls out energy storage as a margin driver. A 3-week production pause could delay revenue recognition and compress Q2 margins. The supply dependency on CATL (a Chinese supplier) also introduces geopolitical risk to the energy storage growth story.

**Updated thesis status: HOLDING** ➡️
*(Moved from Accelerating to Holding — one bearish signal against three prior bullish signals nets out to neutral. If another bearish signal arrives this week, status would move to Weakening.)*

**What I'm watching:**
- Tesla IR page for any response or clarification
- CATL earnings call next week for commentary on supply timelines
- Any competing energy storage announcements from competitors (Fluence, BYD)

**No action recommended** — just flagging this for your awareness. Your cost basis is free5; current price is $211.30.

⚠️ *This is information only, not financial advice. Always do your own research.*

---

**User:** "Good catch. Add a note: I want to watch whether CATL dependency is a one-off or a structural risk."

**Agent:**

📝 Note added to TSLA thesis log:
> "Watch: Is CATL supply dependency a one-off disruption or structural risk to energy storage growth thesis? — flagged March 24, 2026"

I'll specifically monitor for:
- Further CATL supply disruptions
- Tesla announcements about alternative cell suppliers
- Any mention of in-house cell production timelines (4680 cells)

This will be factored into future thesis evaluations.

---

*This example demonstrates: thesis setup on position entry, periodic thesis health checks, immediate alerts on status changes, signal logging with source attribution, user note integration, and proactive monitoring adjustments.*
