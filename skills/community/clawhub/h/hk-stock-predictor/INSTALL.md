# Install via CLI

## Option A: install from this local repo

Run from repo root:

```bash
bash scripts/install-hk-stock-predictor-skill.sh
```

This copies:

- `skills/hk-stock-predictor/SKILL.md`

to:

- `~/.codex/skills/hk-stock-predictor/SKILL.md`

## Option B: install from GitHub

```bash
~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/hk-stock-predictor
```

## Verify

```bash
ls -la ~/.codex/skills/hk-stock-predictor
```

## Final step

Restart Codex/Cursor agent runtime to load the new skill.
