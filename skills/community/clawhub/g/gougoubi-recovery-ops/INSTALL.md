# Install

## Local install

```bash
cp -R skills/gougoubi-recovery-ops "$CODEX_HOME/skills/"
```

## GitHub install

```bash
~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/gougoubi-recovery-ops
```

## Verify

```bash
ls -la "$CODEX_HOME/skills/gougoubi-recovery-ops"
```

## Post-install check

Open `SKILL.md` and confirm the referenced recovery scripts exist in the local project checkout before using this skill.

Restart the agent runtime after installation.
