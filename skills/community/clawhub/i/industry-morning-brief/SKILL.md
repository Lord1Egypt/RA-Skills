---
name: industry-morning-brief
description: "Generate a structured daily morning brief for an industry vertical by searching public web sources and synthesizing the latest developments into a concise, actionable bulletin. Use when: the user asks for today's/this morning's news, roundup, recap, or update for an industry (e.g. new energy, renewables, EV, battery, solar, wind, hydrogen, semiconductor, biotech). Not for: historical analysis, deep financial modeling, or private/internal data."
homepage: https://github.com/openclaw/openclaw
metadata:
  {
    "openclaw":
      {
        "emoji": "📰⚡",
        "requires": { "bins": ["curl"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "curl",
              "bins": ["curl"],
              "label": "Install curl (brew)",
            },
          ],
      },
  }
---

# Industry Morning Brief

Generate a structured daily morning brief for an industry vertical by searching public web sources and synthesizing the latest developments.

## When to Use

✅ **USE this skill when:**

- "Give me today's new energy news / morning brief"
- "What's happening in EV / battery / solar / wind today?"
- "Recap the latest developments in [industry] this week"
- "Show me today's headlines in renewables"

❌ **DON'T use this skill when:**

- Historical data or deep trend analysis spanning months/years
- Private/internal company data or confidential earnings calls
- Financial modeling, valuations, or portfolio decisions
- Real-time trading signals or price predictions

## Approach

The skill fetches recent public content and synthesizes it into a structured brief. Do not fabricate facts — every claim must be traceable to a source URL.

**Standard workflow:**

1. Pick the industry (default: new-energy). See `references/sources.md` for per-vertical search terms and trusted sources.
2. Run the fetcher script (see below) to pull recent headlines + snippets.
3. Deduplicate across sources and drop anything older than ~48h unless it is still unfolding.
4. Synthesize into the canonical sections below.
5. End with `Sources:` listing URLs.

## Structured Output

Use exactly these sections (Markdown). Keep each section tight — aim for ~3–6 bullet points per section, ~500–800 words total.

```
# [Industry] Morning Brief — YYYY-MM-DD

## 1. 重点新闻 / Headlines
- 3–5 top stories, 1 line each with company/policy names.

## 2. 政策与监管 / Policy & Regulation
- Government, regulator, or legislative moves (subsidies, tariffs, permits, standards).

## 3. 产业链动向 / Supply-Chain & Companies
- M&A, partnerships, financing, capacity expansions, supply deals, tech launches.

## 4. 潜在影响 / Potential Impact
- How the above could shift the competitive landscape, costs, or timelines.

## 5. 需跟踪事项 / Items to Track
- Upcoming catalysts: product launches, earnings, policy deadlines, trade talks.

---
Sources:
- https://...
- https://...
```

## Command-line Entrypoint

A helper script is bundled: `scripts/brief.sh`. It wraps the retrieval and prints a draft-ready brief to stdout. You still need to synthesize the final text.

```bash
# Default: new-energy brief for today
bash scripts/brief.sh

# Specific industry (see references/sources.md for supported keys)
bash scripts/brief.sh --industry new-energy
bash scripts/brief.sh --industry ev
bash scripts/brief.sh --industry semiconductor

# Custom query (free text)
bash scripts/brief.sh --query "solid state battery 2026"

# N days back (default 1)
bash scripts/brief.sh --days 2
```

The script emits raw headline entries to stderr and the synthesized Markdown brief to stdout.

## Sources

For trusted source lists and search keywords per industry, read `references/sources.md`.

## Notes

- No API key required; uses public search engines and publisher sites.
- Respect robots.txt and rate limits — the script spaces requests.
- Always include `Sources:` with URLs at the bottom of the output.
