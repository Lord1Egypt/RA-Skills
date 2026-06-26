# openclaw-gov command reference

Pin: **v0.5.5**. Pass `--root PATH` on every command when not using default resolution.

| Command | Mutates files? | Description |
|---------|----------------|-------------|
| `doctor` | No | Check OpenClaw home, config, remote, inject list |
| `doctor --validate-config` | No | Doctor + semantic config validation |
| `config validate` | No | Validate `governance.config.yaml` |
| `init` | Yes | Scaffold governance root from templates |
| `init --adopt PATH` | Yes | Init + adopt from existing root |
| `adopt --from PATH` | Yes | Adopt source root (source authoritative by default) |
| `adopt --keep-target-config` | Yes | Adopt; target config wins on conflict |
| `discover` | No | Read-only console summary |
| `discover --inventory` | Yes (inventory only) | Write `workflows/discovered-inventory.json` |
| `discover --json` | No | JSON on stdout; human report on stderr |
| `discover --staged` | Yes (inventory + candidates) | No registry mutation |
| `discover --promote` | Yes | Apply staged merge when semantic diff |
| `discover --promote --allowlist PATH` | Yes | Promote listed workflow ids only |
| `discover --write` | Yes | Registry + runbook stubs (legacy/greenfield) |
| `discover --include-runtime-metrics` | Yes | Volatile timings file (gitignored) |
| `check` | No | Validate registry ↔ runbooks ↔ README |
| `regen --write` | Yes | Refresh README summary + RACI markers |
| `regen --check` | No | CI drift check |
| `inject-agents --write` | Yes | Add governance block to AGENTS.md |
| `inject-agents --write --prune` | Yes | Inject allowlist + remove stanza elsewhere |
| `inject-agents --agent ID --write` | Yes | Single agent override |
| `ship start --branch NAME` | Yes (git branch) | Create/checkout named feature branch from main |
| `ship commit --no-push` | Yes (git commit) | Validate, stage, Conventional Commit; stop after commit |
| `ship commit --push` | Yes | Commit + push + open PR (single step; do not run plain commit first) |

Root precedence: `--root` > `OPENCLAW_GOVERNANCE_ROOT` > nearest `governance.config.yaml` > `~/.openclaw/governance`.
