# Install

## Local install

```bash
cp -R skills/gougoubi-create-prediction "$CODEX_HOME/skills/"
```

## GitHub install

```bash
~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/gougoubi-create-prediction
```

## Verify

```bash
ls -la "$CODEX_HOME/skills/gougoubi-create-prediction"
```

## Post-install check

If the local project scripts are available, verify the public entrypoint first:

```bash
node scripts/pbft-create-from-polymarket.mjs --help
node scripts/pbft-create-from-polymarket.mjs "<polymarket url>" --dry-run
```

Restart the agent runtime after installation.
