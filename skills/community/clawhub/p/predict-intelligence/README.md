# Predict Intelligence Skill

> One prompt → professional PDF intelligence brief, powered by real-money prediction market signals.

Stop guessing. This skill turns any AI agent into a predict analyst — it researches the topic, formulates probability-ranked predictions, cross-references **Polymarket** (the world's largest prediction market) for market consensus, builds D3 visualizations, and delivers a polished, source-verified PDF report you can scan in 30 seconds.

## How It Works

```
Prompt → Research (8+ source types) → Predictions → Polymarket consensus → D3 visualization → PDF
```

The agent reads `SKILL.md` and autonomously:

1. **Researches** across breaking news, think tanks, expert analysis, official statements, historical precedent, and OSINT sources
2. **Formulates predictions** — probability-ranked outcomes with Bayesian-calibrated confidence levels that sum to ~100%
3. **Pulls Polymarket data** — fetches live implied probabilities, computes delta between your assessment and market consensus, highlights undervalued positions
4. **Builds visualizations** — picks from 9 built-in D3 chart types (regional maps, entity graphs, sankey flows, timelines, choropleths, and more)
5. **Outputs a PDF** — CIA-brief-style single-page intelligence assessment with white monochrome design

## Output

The final report is a self-contained HTML file converted to PDF. Each report includes:

- **52px verdict number** — the headline probability, scannable in 1 second
- **Probability-ranked outcome bars** — all scenarios with calibrated percentages
- **5 key drivers** — each with causal logic (fact → mechanism → direction) and source URLs
- **Watch list** — 5 future triggers with conditional impact ("If X → probability shifts Y")
- **1–2 D3 visualizations** — data-driven charts selected for the specific domain
- **Polymarket delta comparison** — where your assessment diverges from market consensus
- **Full source list** — every claim backed by a verified article URL

## Try It

| Domain | Example Prompt |
|--------|---------------|
| Geopolitics | `"Predict: Will there be a US-Iran ceasefire before April 2026?"` |
| Finance | `"Generate a predict report: Will the Fed cut rates before July 2026?"` |
| Crypto | `"Intelligence brief: Bitcoin probability of hitting $150k by end of 2026"` |
| Tech | `"Predict: When will OpenAI release GPT-5?"` |
| Elections | `"Predict report: Who wins the 2026 US midterm Senate majority?"` |
| Corporate | `"Intelligence brief: Probability of a TikTok US ban in 2026"` |

## Setup

```bash
pip install playwright && playwright install chromium
```

That's it. No other dependencies. D3.js and fonts load from CDN. The HTML template is fully self-contained.

## Why This Skill

- **Polymarket-powered** — built-in script fetches live prediction market data, computes consensus deltas, and highlights where the crowd might be wrong
- **9 D3 visualization types** — maps, entity graphs, timelines, sankey flows, choropleths, comparison bars, gantt charts, big numbers — all pre-built, agent just fills in data
- **Source-verified** — every claim requires a real article URL; homepage links are rejected
- **30-second scannability** — designed for decision-makers who need the answer first, details second
- **Agent-agnostic** — works with any AI agent that can search the web, read/write files, and run shell commands
- **Single dependency** — only Playwright (for HTML → PDF); everything else is self-contained

## File Structure

```
predict-intelligence/
├── SKILL.md                        # Agent instructions (10-step workflow)
├── README.md                       # This file
├── reference.md                    # Data sources & Bayesian methodology guide
├── templates/
│   └── report_template.html        # Self-contained HTML template (CSS + D3)
├── scripts/
│   ├── to_pdf.py                   # HTML → PDF (Playwright)
│   ├── fetch_polymarket.py         # Polymarket API data fetcher
│   ├── build_report.py             # Legacy pipeline
│   └── requirements.txt
└── examples/
    ├── example_report.html         # Filled example
    └── sample_data.json            # Sample data
```

## License

[MIT](../../../LICENSE)