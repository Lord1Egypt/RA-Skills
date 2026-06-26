# Install

## Local install

```bash
cp -R skills/gougoubi-market-orchestrator "$CODEX_HOME/skills/"
```

## GitHub install

```bash
~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/gougoubi-market-orchestrator
```

## Verify

```bash
ls -la "$CODEX_HOME/skills/gougoubi-market-orchestrator"
```

## Post-install check

Open `SKILL.md` and confirm the downstream skill names exist in the installed skills directory.

Restart the agent runtime after installation.
