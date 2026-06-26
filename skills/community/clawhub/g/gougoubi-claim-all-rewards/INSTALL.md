# Install

## Local install

```bash
cp -R skills/gougoubi-claim-all-rewards "$CODEX_HOME/skills/"
```

## GitHub install

```bash
~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/gougoubi-claim-all-rewards
```

## Verify

```bash
ls -la "$CODEX_HOME/skills/gougoubi-claim-all-rewards"
```

## Post-install check

If the local project scripts are available, verify the public entrypoints first:

```bash
node scripts/pbft-claim-rewards-profile-method.mjs --help
node scripts/pbft-claim-rewards-profile-method.mjs --dry-run
node scripts/pbft-claim-rewards-quick.mjs --dry-run
```

Restart the agent runtime after installation.
