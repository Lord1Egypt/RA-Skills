# Learnings Skill

Continuous learning system. Every failure, correction, and pattern gets logged so the same mistakes aren't repeated. Uses its own MeiliSearch index for fast recall.

## What Gets Logged

| Category | Description |
|----------|-------------|
| `failure` | Script/command errors |
| `correction` | Fixes applied after mistakes |
| `approach` | Right ways to do things |
| `version_rule` | How versions should increment |
| `preference` | User preferences discovered |
| `recurring_failure` | Same thing failing repeatedly |
| `rule` | Explicit "don't do X" rules |
| `learning` | General lessons learned |

## Files

- `LEARNINGS.md` — Human-readable summary (auto-generated)
- `scripts/setup_index.sh` — Create/configure MeiliSearch index
- `scripts/log_learning.sh` — Log a new learning entry
- `scripts/search_learnings.sh` — Search past learnings before acting
- `scripts/auto_extract.sh` — Auto-extract learnings from daily notes
- `scripts/distill_learnings.sh` — Summarize raw logs into LEARNINGS.md

## Install

```bash
git clone https://github.com/enjuguna/learnings-skill.git
cp -r learnings-skill ~/.openclaw/workspace/skills/learnings
bash scripts/setup_index.sh
```

Or from ClawHub: `openclaw skills install learnings`

## Usage

```bash
bash scripts/log_learning.sh --category failure --what "description" --fix "solution" --importance 0.9
bash scripts/search_learnings.sh "github push" 5
bash scripts/auto_extract.sh --days 7
bash scripts/distill_learnings.sh
```

## License

MIT
