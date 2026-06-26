<img width="1280" height="480" alt="Inference Optimizer" src="./social-preview.png" />

# /inference-optimizer

Production-oriented OpenClaw skill for auditing runtime health, cleaning stale session state, and applying safer inference tuning with approval.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

## What it does

`inference-optimizer` does not start with token tuning guesses. It checks the runtime first, then recommends cleanup or tuning only after the obvious operational failures are ruled out.

Audit order:

1. Gateway ownership and duplicate supervisors
2. Restart loops and failed services
3. Resolved `openclaw` binary path and install type
4. Updater status and allowlist coverage for the resolved path
5. Plugin provenance and unused local extensions
6. Context pressure, stale sessions, cache-trace, pruning, and concurrency

Core commands:

```text
/preflight
/audit
/optimize
purge sessions
```

## Install

```bash
clawhub install inference-optimizer
```

Manual install:

```bash
git clone https://github.com/vitalyis/inference-optimizer.git ~/clawd/skills/inference-optimizer
bash ~/clawd/skills/inference-optimizer/scripts/setup.sh
bash ~/clawd/skills/inference-optimizer/scripts/setup.sh --apply
```

## Usage

```text
/preflight              # backup + audit + setup preview
/audit                  # analyze-only runtime audit
/optimize               # audit, then propose approved actions
purge sessions          # archive stale sessions after approval
```

Operational checks:

- Treat warnings as signals, not proof.
- If updater output is partial or truncated, verify installed version, service status, and logs before claiming root cause.
- Resolve the real executable path before changing the allowlist.
- Use `bash scripts/verify.sh` after install; it now fails on legacy `skills/public` and repo-local workspace wiring.

For script details and safety constraints, see [SECURITY.md](SECURITY.md).

## Update

```bash
cd ~/clawd/skills/inference-optimizer && git pull
```

If installed elsewhere, pull from that skill directory instead.

## Uninstall

```bash
rm -rf ~/clawd/skills/inference-optimizer
```

## Safety

- `/audit` is analyze-only and should not mutate workspace files.
- `purge-stale-sessions.sh` archives by default. Use `--delete` only for intentional immediate removal.
- `setup.sh` previews by default. Use `--apply` only after reviewing changes.
- For allowlists, prefer exact executable paths or bounded NVM wildcards such as `/home/ubuntu/.nvm/versions/node/*/bin/openclaw *`.
- Do not rely on basename-only allowlist entries like `openclaw`.

Additional background and remediation notes live in [SECURITY.md](SECURITY.md).

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for workflow and release-note expectations.

## License

MIT
