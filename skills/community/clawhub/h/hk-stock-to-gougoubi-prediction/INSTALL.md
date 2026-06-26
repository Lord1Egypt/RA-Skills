# Install via CLI

## Option A: install from this local repo

Run from repo root:

```bash
bash scripts/install-hk-stock-to-gougoubi-prediction-skill.sh
```

This copies:

- `skills/hk-stock-to-gougoubi-prediction/SKILL.md`

to:

- `~/.codex/skills/hk-stock-to-gougoubi-prediction/SKILL.md`

## Option B: install from GitHub

```bash
~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/hk-stock-to-gougoubi-prediction
```

## Verify

```bash
ls -la ~/.codex/skills/hk-stock-to-gougoubi-prediction
```

## Final step

Restart Codex/Cursor agent runtime to load the new skill.
