# last30days Skill

Claude Code skill for researching any topic across Reddit, X, YouTube, and web.
Python scripts with multi-source search aggregation.

## Structure
- `scripts/last30days.py` — main research engine
- `scripts/lib/` — search, enrichment, rendering modules
- `scripts/lib/vendor/bird-search/` — vendored X search client
- `SKILL.md` — skill definition (deployed to ~/.claude/skills/last30days/)

## Commands
```bash
python3 scripts/last30days.py "test query" --emit=compact  # Run research
bash scripts/sync.sh                                        # Deploy to ~/.claude, ~/.agents, ~/.codex
```

## Rules
- `lib/__init__.py` must be bare package marker (comment only, NO eager imports)
- After edits: run `bash scripts/sync.sh` to deploy
- Git remote: origin = public (`mvanhorn/last30days-skill`)

## Beta channel

Experimental changes get tested on `mvanhorn/last30days-skill-private`, which installs as a parallel `/last30days-beta` slash command. Beta-only changes never ship to public without a review PR here. Workflow guide lives at `BETA.md` in the private repo. Plan that established this setup: `docs/plans/2026-04-17-005-feat-beta-skill-from-private-repo-plan.md`.
