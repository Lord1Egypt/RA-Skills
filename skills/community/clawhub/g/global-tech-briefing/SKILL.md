---
name: global-tech-briefing
description: "Create a structured global tech news briefing by running web searches for top tech trends, company announcements, and AI/quantum headlines. Returns a summary with key takeaways, not raw search results. No API key needed for core searches."
homepage: https://brave.com/search/api
metadata:
  {
    "openclaw":
      {
        "emoji": "🌐",
        "requires": { "bins": ["node", "web_search"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "packages": [],
              "bins": ["node"],
              "label": "Node.js required for script execution",
            },
          ],
      },
  }
---

# Global Tech Briefing Skill

Create a structured global tech news briefing by running web searches for top tech trends, company announcements, and AI/quantum headlines. Returns a summary with key takeaways, not raw search results.

## When to Use

✅ **USE this skill when:**

- "What's the latest in tech?"
- "Global tech briefing for today"
- "Top tech trends or announcements"
- "Quick tech news summary"

## When NOT to Use

❌ **DON'T use this skill when:**

- Detailed technical reviews → use specialized tech review sites
- Historical tech news → use archives
- Hyper-local tech events → use local tech blogs

## Commands

### Get Briefing

Execute the main script (scripts/get-briefing.js) with optional date for the briefing.

```bash
# Today's briefing
node /usr/lib/node_modules/openclaw/skills/global-tech-briefing/scripts/get-briefing.js

# Specific date briefing (YYYY-MM-DD)
node /usr/lib/node_modules/openclaw/skills/global-tech-briefing/scripts/get-briefing.js 2026-07-10
```

## Briefing Structure

**[Global Tech Briefing: {{date}}]
Key Trends:
  - {{trend1}} (e.g., AI funding rounds)
  - {{trend2}} (e.g., quantum computing announcements)
  - {{trend3}} (e.g., chip manufacturing news)
Company News:
  - {{company1}} (e.g., Big Tech earnings)
  - {{company2}} (e.g., startup launches)
Key Takeaways:
  - {{takeaway1}}
  - {{takeaway2}}**

## Notes

- Uses web_search to get up-to-date results
- Summarizes into structured sections
- Supports custom dates for historical checks