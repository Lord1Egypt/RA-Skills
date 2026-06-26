# Install

## Local install

```bash
cp -R skills/gougoubi-submit-real-results "$CODEX_HOME/skills/"
```

## GitHub install

```bash
~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path skills/gougoubi-submit-real-results
```

## Verify

```bash
ls -la "$CODEX_HOME/skills/gougoubi-submit-real-results"
```

## Post-install check

If the local project scripts are available, verify the public entrypoints first:

```bash
node scripts/pbft-submit-results-from-skills-once.mjs --help
node scripts/pbft-submit-all-condition-results.mjs --help
node scripts/pbft-submit-all-condition-results.mjs <proposalAddress> --result yes --dry-run
```

Restart the agent runtime after installation.
