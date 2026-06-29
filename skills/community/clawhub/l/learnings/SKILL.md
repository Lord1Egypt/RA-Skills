---
name: learnings
description: Continuous learning from failures, corrections, and patterns. Logs mistakes to prevent repetition. Own MeiliSearch index. Learns version rules, approach preferences, and behavioral corrections.
---

# Learnings Skill

Continuous learning system. Every failure, correction, and pattern gets logged so the same mistakes aren't repeated. Uses its own MeiliSearch index for fast recall.

## Security Model

- **Credentials**: MeiliSearch key is loaded from `~/.openclaw/workspace/.env` — never hardcoded in scripts
- **Sensitive data filtering**: Auto-extraction skips content containing tokens, passwords, API keys, and credentials
- **Safe defaults**: Distillation and auto-extract default to `--dry-run`; use `--apply` to write
- **Secure temp files**: All temp files use `mktemp` with `chmod 600` and are cleaned up on exit

## Capabilities (declared)

- **Read**: `memory/*.md` (daily notes, for auto-extraction)
- **Write**: MeiliSearch `learnings` index, `LEARNINGS.md` (distillation only with `--apply`)
- **Execute**: `curl` to localhost MeiliSearch, `python3` for document processing

## What Gets Logged

| Category | Description | Example |
|----------|-------------|---------|
| `failure` | Script/command errors | "npm install fails with permission error" |
| `correction` | Fix applied after a mistake | "Use --prefix flag for global installs" |
| `approach` | Right way to do something | "Use full-text search over vector DB for local memory" |
| `version_rule` | How versions should increment | "1.1.0 → 1.2.0 for new features" |
| `preference` | User preferences discovered | "Prefers local/no-cloud solutions" |
| `recurring_failure` | Same thing failing repeatedly | "Auth token expires on every deploy" |
| `rule` | Explicit "don't do X" rules | "Don't commit secrets to repositories" |
| `learning` | General lessons learned | "Always check file exists before copying" |

## Configuration

Requires `~/.openclaw/workspace/.env`:

```bash
MEILI_HOST=http://127.0.0.1:7700
MEILI_KEY=your-master-key-here
```

## Files

- `LEARNINGS.md` — Human-readable summary (auto-generated, use `--apply` to write)
- `scripts/setup_index.sh` — Create/configure MeiliSearch index
- `scripts/log_learning.sh` — Log a new learning entry
- `scripts/search_learnings.sh` — Search past learnings before acting
- `scripts/auto_extract.sh` — Auto-extract learnings from daily notes
- `scripts/distill_learnings.sh` — Summarize raw logs into LEARNINGS.md

## Usage

```bash
# Log a learning
bash scripts/log_learning.sh \
  --category failure \
  --what "deployment fails with auth token expiry" \
  --fix "Refresh token before each deploy" \
  --importance 0.9 \
  --tags "deploy,auth,token"

# Search before acting
bash scripts/search_learnings.sh "github push" 5

# Auto-extract from daily notes (dry-run by default)
bash scripts/auto_extract.sh --days 7 --apply

# Distill into readable summary (dry-run by default)
bash scripts/distill_learnings.sh --apply
```

## How It Integrates

Before taking any action, I search the learnings index:
1. Search for the action/context
2. If a past learning exists, apply the fix first
3. If the action fails, log it immediately
4. If you correct me, log it as a high-priority correction

## Version Rules (Learned)

- Increment **minor** (1.1.0 → 1.2.0) for new features
- Increment **major** (1.0.0 → 2.0.0) for breaking changes
- Avoid patch-level bumps (1.1.0 → 1.1.1) unless it's an actual bug fix
