# Matic Trades — OpenClaw skill

Skill pack for [ClawHub](https://clawhub.ai) / OpenClaw: **toolbox `AI_PICK`** (prompt-only; no required `context`), **data `SMART_SEARCH`**, and **agent charting** against the Matic Trades API.

## Contents

| File | Purpose |
|------|---------|
| `SKILL.md` | Agent instructions (required for ClawHub) |
| `scripts/matic.py` | CLI: `toolbox`, `data`, `chart` subcommands |
| `references/api.md` | JSON shapes for advanced use |

## Setup

1. Get an API key from [matictrades.com](https://matictrades.com) (account → API keys).

2. Set environment variables (shell profile or OpenClaw environment):

   ```bash
   export MATIC_API_KEY="your_key_here"
   # Optional — override if your API is on a different host:
   # export MATIC_TRADES_API_BASE="https://api.matictrades.com/api/v1"
   # export MATIC_TRADES_API_BASE="https://matictrades.com/api/v1"
   ```

3. **Install the skill**

   - **ClawHub:** Zip this folder (so `SKILL.md` is at zip root or under one folder—follow ClawHub upload UI), or use **Publish → choose folder** with `matic-trades` as the folder containing `SKILL.md`.
   - **Manual:** Copy the `matic-trades` folder into your OpenClaw workspace skills directory, e.g. `~/.openclaw/workspace/skills/matic-trades/` (path may vary; see [OpenClaw skills docs](https://docs.openclaw.ai/tools/skills)).

4. Restart the agent / run `/new` so the skill loads.

5. Test:

   ```bash
   cd matic-trades
   python3 scripts/matic.py data --prompt "price of bitcoin"
   python3 scripts/matic.py toolbox --prompt "Summarize NVDA sentiment and key levels"
   python3 scripts/matic.py chart --prompt "Analyze NVDA" --images url
   ```

## ClawHub publish checklist

- [ ] `SKILL.md` present with YAML frontmatter (`name`, `description`)
- [ ] MIT-0 acceptance on ClawHub
- [ ] Slug suggestion: `matic-trades`
- [ ] Tags: `latest`, `trading`, `finance`, `charts` (as allowed)

## Support

Product: [matictrades.com](https://matictrades.com) — docs and dashboard for keys, quotas, and billing.
