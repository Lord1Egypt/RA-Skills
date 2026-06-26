# Install

## Local install

```bash
cp -R skills/gougoubi-create-condition "$CODEX_HOME/skills/"
```

## GitHub install

```bash
~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/gougoubi-create-condition
```

## Verify

```bash
ls -la "$CODEX_HOME/skills/gougoubi-create-condition"
```

## Post-install check

Open `SKILL.md` and confirm the minimal input contract matches your automation or agent wrapper.

Restart the agent runtime after installation.
