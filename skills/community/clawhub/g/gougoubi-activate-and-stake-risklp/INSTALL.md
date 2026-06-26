# Install

## Local install

```bash
cp -R skills/gougoubi-activate-and-stake-risklp "$CODEX_HOME/skills/"
```

## GitHub install

```bash
~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/gougoubi-activate-and-stake-risklp
```

## Verify

```bash
ls -la "$CODEX_HOME/skills/gougoubi-activate-and-stake-risklp"
```

## Post-install check

If the local project scripts are available, verify the public entrypoint first:

```bash
node scripts/pbft-activate-and-add-risklp.mjs --help
node scripts/pbft-activate-and-add-risklp.mjs <proposalAddress> 100 --dry-run
```

Restart the agent runtime after installation.
