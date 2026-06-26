# 🔎 Perplexity Search — OpenClaw Skill

Search the web with the **Perplexity Sonar API** from inside OpenClaw. Get grounded, cited, real-time answers without leaving your agent session.

## What this skill does

- Sends your query to Perplexity's `sonar` or `sonar-pro` models
- Returns a structured markdown report: **Answer → Citations → Search Results → Related Questions**
- Works with zero external Python packages (pure standard library)
- Auto-invoked by the agent on web-search intent — no slash command needed

## Requirements

| Requirement | Value |
|-------------|-------|
| Binary | `python3` (3.8+) |
| Environment variable | `PERPLEXITY_API_KEY` |
| External endpoint | `https://api.perplexity.ai/chat/completions` |

## Install

```bash
clawhub install perplexity-search
```

Then add your API key to `~/.openclaw/.env`:

```bash
PERPLEXITY_API_KEY=pplx-your-key-here
```

Get a key at → https://www.perplexity.ai/settings/api

Restart OpenClaw (or start a new session) to activate the skill.

## Usage

The agent invokes this skill automatically when you ask about anything web-related:

> "What's the latest on GPT-5?"  
> "Search for the best LMS platforms for distance education"  
> "Find the current Perplexity API pricing"

Or reference it explicitly:

> "Use Perplexity to find recent news about AI agents"

## Manual test (outside OpenClaw)

```bash
python3 skills/perplexity-search/scripts/perplexity_search.py \
  --query "OpenClaw latest features"
```

## Skill folder layout

```
perplexity-search/
├── SKILL.md               ← Agent instructions + frontmatter
└── scripts/
    └── perplexity_search.py  ← Python search script (no dependencies)
```

## Security

- Only `PERPLEXITY_API_KEY` is accessed from the environment.
- The key is never printed, logged, or passed as a command-line argument.
- The only external call is to `https://api.perplexity.ai/chat/completions`.
- No local files are read or written.

---

Licensed MIT-0 · Published to ClawHub
