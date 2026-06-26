# Google Trends Skill

An [Agent Skill](https://agentskills.io) for fetching Google Trends data. Works with Claude Code, Codex, OpenClaw, and any agent that supports the Agent Skills standard.

No API key required. Zero external dependencies — uses only Node.js built-ins.

## Installation

**skills.sh:**
```bash
npx skills add terryds/google-trends-skill
```

**ClawHub:**
```bash
npx clawhub@latest install google-trends
```

**Manual:** Copy this repo into your agent's skills directory (e.g. `.claude/skills/` or `.agents/skills/`).

## Commands

| Command | Description |
|---------|-------------|
| `daily-trends` | Get daily trending search topics |
| `realtime-trends` | Get real-time trending topics (last N hours) |
| `autocomplete` | Get autocomplete suggestions for a keyword |
| `explore` | Explore trend data for a keyword |
| `interest-by-region` | Get search interest breakdown by region |
| `related-topics` | Get topics related to a keyword |
| `related-queries` | Get queries related to a keyword |

## Usage

```bash
node scripts/trends.mjs <command> [options]
```

### Examples

```bash
# Daily trending topics in the US
node scripts/trends.mjs daily-trends --geo US

# Real-time trends (last 4 hours)
node scripts/trends.mjs realtime-trends --geo US --hours 4

# Autocomplete suggestions
node scripts/trends.mjs autocomplete "artificial intelligence"

# Explore a keyword
node scripts/trends.mjs explore "machine learning" --geo US --time "now 7-d"

# Interest by region
node scripts/trends.mjs interest-by-region "bitcoin" --geo US --resolution REGION

# Related topics
node scripts/trends.mjs related-topics "python programming" --geo US

# Related queries
node scripts/trends.mjs related-queries "python programming" --geo US
```

All commands output JSON to stdout.

## Options

See [reference.md](reference.md) for the full list of options per command.

## Requirements

- Node.js 18+

## Credits

Based on [trends-js](https://github.com/Shaivpidadi/trends-js) by Shaivpidadi.

## License

MIT
