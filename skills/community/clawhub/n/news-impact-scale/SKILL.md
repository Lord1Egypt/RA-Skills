# News Impact Scale — Skill Specification

## What It Does

Analyzes a news article from a URL and returns a structured **prev/current/future impact analysis** in plain English — tailored to *you*, based on your stored location, interests, and travel plans.

**No opinions. Real data. Historical benchmarks. Extrapolated futures.**

---

## Activation Triggers

Any of these will activate the skill:

- `analyze news <url>`
- `analyze this news article <url>`
- `news impact <url>`
- `what's the impact of this news <url>`
- `analyze this <url>`

---

## How It Works (3 Stages)

### Stage 1 — Analyze
Triggered when you provide a URL. The skill:
1. Fetches the article
2. Classifies the event type (natural disaster, corporate, political, etc.)
3. Identifies affected geographic location and systems
4. Checks historical benchmark cache
5. Generates **benchmark research queries** for the agent to run
6. Produces a preliminary timeline (Medium/High confidence if benchmarks exist)

### Stage 2 — Benchmark Research (Agent does this)
The agent takes the benchmark queries from Stage 1 and runs web searches to find real historical data (e.g., "how long did roads take to restore after the 2011 Japan earthquake"). Results are fed into Stage 3.

### Stage 3 — Final Report
Produces the complete written analysis with:
- Prev/Current/Future timeline for each affected system
- Real historical benchmarks used as projection basis
- Confidence scores (grounded in how many comparable events exist)
- Trend direction (worsening / stable / improving)
- Plain-English explanation of what the news means for you personally

---

## Setup — Fill In Your Context

Before first use, edit `context.json` in this skill directory:

```json
{
  "location": {
    "city": "Belgrade",
    "country": "Serbia",
    "coordinates": "44.7866, 20.4489"
  },
  "interests": ["technology", "finance", "energy", "geopolitics"],
  "travelPlans": [
    { "destination": "Japan", "dates": "Q4 2026" }
  ],
  "exposure": {
    "industry": "technology",
    "companies": [],
    "assets": []
  }
}
```

---

## Output Sections

### 📰 What the News Says
Plain-English summary as a regular person would understand it.

### 🌍 Why It Matters to You
- **Geographic relevance** — near you? same country? 
- **Thematic relevance** — touches your interests or industry?
- **Overall personal impact** — High / Moderate / Low

### 📊 Three-State Impact Timeline
For each affected system (roads, power grid, markets, etc.):

| | State | Description |
|---|---|---|
| **Previous** | What was true before | e.g., "Roads fully operational" |
| **Current** | What is true now | e.g., "Highways closed, diversions in place" |
| **Future** | What historical data suggests | e.g., "Roads restored within 18 days (based on 2011 Tōhoku benchmark)" |

Each row includes:
- **Trend** — 🟢 Improving / 🟡 Stable / 🔴 Worsening
- **Confidence** — High / Medium / Low (based on number of comparable cases)
- **Benchmark source** — the actual historical case used

### 📈 Trend Direction
Overall trend across all affected systems.

### 🔍 Confidence & Caveats
What data was used, what the limitations are.

---

## Confidence Scoring

| Level | When |
|---|---|
| **High** | 3+ comparable historical events in the same location |
| **Medium** | 1–2 comparable cases found |
| **Low** | No precedent — projections are general patterns, not data-driven |

---

## File Structure

```
news-impact-scale/
├── SKILL.md              ← This file
├── analyze.js             ← Main engine (Stage 1 + Stage 3)
├── context.json           ← Your personal context (fill in)
├── benchmarks.json        ← Historical benchmark database (auto-updated)
├── stage1_output.json     ← Intermediate output from Stage 1
└── lib/
    ├── fetcher.js         ← Fetch + extract article text
    ├── classifier.js      ← Classify event type, location, systems
    ├── benchmarker.js     ← Historical data research + storage
    ├── projector.js       ← Build prev/current/future timeline
    └── explainer.js       ← Plain-English explanations
```

---

## Example Flow

```
You:    "analyze news https://example.com/article"
Agent:  (runs Stage 1) → generates benchmark queries → runs web searches → runs Stage 3
        → delivers full written report
```

---

## Notes

- Benchmarks are **location-specific**: Japan events benchmark against Japan history, not generic data
- Future projections are **extrapolations, not guarantees** — always shown with confidence
- `benchmarks.json` grows over time — the more you use it, the smarter it gets
- Some sites (BBC, WSJ) may block scraping — try Reuters or open-access sources if needed
