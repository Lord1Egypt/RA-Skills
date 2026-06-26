# Global Nuclear Brief (OpenClaw Skill)

## Main idea
Global Nuclear Brief is an OpenClaw skill that monitors recent nuclear energy policy/regulatory developments and produces a concise, decision‑ready brief for analysts. It turns live public information into grounded, actionable summaries so teams can quickly understand what changed, why it matters, and what to do next.

## Why it matters
Policy and regulatory shifts in nuclear energy are frequent and global. Manually tracking updates across sources is slow and error‑prone. This skill automates the monitoring and synthesizes the signal into a structured brief.

## How it works
1. **Live data pull (Apify)**: Fetches recent nuclear policy/regulatory news.
2. **Grounded synthesis (Contextual)**: Generates a structured brief using only retrieved sources.
3. **Output**: A clear, 5‑section brief with sources.

## Output format
1. Top changes (3‑5 bullets)
2. Why it matters (3 bullets)
3. Risks and uncertainties (2‑3 bullets)
4. Recommended actions (3 bullets)
5. Sources (titles + links)

## Quickstart
```bash
export APIFY_API_TOKEN=your_apify_token
export CONTEXTUAL_API_KEY=your_contextual_key

python3 bin/nuclear_brief.py \
  --query "nuclear energy policy OR nuclear regulation" \
  --topic "Global nuclear energy policy" \
  --audience "policy analysts" \
  --country "US" \
  --timeframe "7d"
```

## Demo tips
- Show the Apify run (live data) and one or two source URLs.
- Show the brief output and the Sources section.
- Emphasize that the brief is grounded in real, current material.
