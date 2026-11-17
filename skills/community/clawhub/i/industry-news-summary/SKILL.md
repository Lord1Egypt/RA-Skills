---
name: industry-news-summary
description: "Fetch current AI industry news from public web sources and generate a structured summary with Topic Overview, Key Events, Potential Impact, and Information Sources. Use when: user requests a daily AI industry update or summary. Uses the web_search tool with a query for today's AI news."
homepage: https://example.com/industry-news-summary
metadata:
  {
    "openclaw":
      {
        "emoji": "🤖",
        "requires": { "tools": ["web_search"] },
        "install":
          [
            {
              "id": "skill-install",
              "kind": "local",
              "label": "Install industry-news-summary skill",
            },
          ],
      },
  }
---

# Industry News Summary Skill

Generate structured daily AI industry news summaries.

## When to Use

✅ **USE this skill when:**

- "Give me today's AI industry news summary"
- "What's happening in AI today?"
- "Summarize recent AI industry updates"
- "Daily AI industry brief"

## Key Output Sections

1. **Topic Overview** - High-level summary of major AI trends today
2. **Key Events** - List of significant AI industry events
3. **Potential Impact** - Short-term effects of key events
4. **Information Sources** - List of public web sources used

## Commands

### Run Skill (Daily Summary)
```bash
openclaw skill industry-news-summary run
```

### Raw Command
```bash
# Uses web_search to get today's AI news, then formats
web_search --query "today's AI industry news" --count 5 | jq '[.[] | {topic_overview: "Today\'s AI news includes advancements in LLMs and computer vision", key_events: [] as $events, potential_impact: [], sources: [] as $sources} | .key_events += [{"title": .title, "source": .url}]]'
```

## Implementation Notes
- Uses the `web_search` tool (no API key required)
- Default query: "today's AI industry news"
- Limits results to top 5 to keep summary concise
- Structured output requires all 4 mandatory sections
- Caches summary to `memory/YYYY-MM-DD-ai-summary.md` for future reference

## Quick Test
```bash
# Generate a sample summary
web_search --query "today's AI industry news" --count 3 | \
jq '{
  "topic_overview": "Today's AI industry news includes LLM product launches, computer vision research breakthroughs, and regulatory updates.",
  "key_events": [
    {"title": "Major LLM Provider Updates Pricing Model", "source": "[1]"}
  ],
  "potential_impact": "Pricing changes may impact small businesses' AI adoption.",
  "information_sources": [
    "TechCrunch",
    "VentureBeat"
  ]
}'
