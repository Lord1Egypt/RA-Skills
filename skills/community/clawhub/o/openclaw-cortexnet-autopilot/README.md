# OpenClaw CortexNet Autopilot Skill

Production-ready Codex Skill for unattended GitHub repository optimization loops.

This skill provides a full orchestration runtime and templates to run AI coding CLIs in priority order, enforce timeout/switch policies, require test-backed results, and push approved changes to the `dev` branch.

## What It Does

- Orchestrates multiple coding CLIs with failover:
  - `Codex CLI -> Gemini CLI -> Open Code CLI -> Claude Code CLI`
- Runs one-time CLI init phase before task execution:
  - asks CLI to execute `/init` first (or equivalent init behavior)
  - supports required init artifacts (for example, Codex `.codex`)
- Syncs latest remote code before attempts:
  - `fetch + checkout/reset to origin/dev + clean`
- Audits by report outcome (not code review in orchestrator):
  - run status must be success
  - test pass rate must meet threshold
- Commits and pushes with concrete change summary in commit message
- Supports unattended loop mode and one-shot mode

## Substance Gates (to avoid tiny/doc-only updates)

Production profile enables strict quality gates by default:

- `require_code_changes=true`
- `require_non_doc_code_changes=true`
- `minimum_non_doc_files_changed=2`
- `minimum_non_doc_lines_changed=30`

If a round only changes docs or changes are below threshold, it is treated as failed and retried/switched.

## Repository Layout

- `SKILL.md`: skill instructions and runtime contract
- `assets/templates/openclaw_autopilot.py`: orchestrator runtime
- `assets/templates/openclaw_config.json`: default config template
- `assets/templates/openclaw_config.production.json`: stricter production baseline
- `assets/templates/start_openclaw.sh`: unattended launcher
- `scripts/deploy_autopilot.py`: deploy and configure a runnable workspace
- `scripts/doctor_autopilot.py`: environment and config diagnostics
- `scripts/setup_autopilot.py`: one-command workspace setup wrapper
- `scripts/log_summary.py`: summarize run logs quickly
- `scripts/install_skill.py`: install this repo into your local Codex skills directory
- `scripts/smoke_test_deploy.py`: offline smoke test for deploy/runtime templates
- `references/`: operations and troubleshooting playbooks

## Prerequisites

- Python 3.10+
- Git
- At least one available coding CLI in PATH (`codex`, `gemini`, `open-code`, or `claude`)
- GitHub token with repo write permissions

## Fastest Setup (One Command)

```bash
python3 scripts/setup_autopilot.py \
  --output-dir /path/to/workdir \
  --repo-url https://github.com/<owner>/<repo>.git \
  --project-name <project-name> \
  --config-profile production \
  --token '<your_github_token>' \
  --run-doctor \
  --run-once \
  --force
```

Notes:
- `--token` writes token into `/path/to/workdir/.env` as `GITHUB_TOKEN=...`
- remove `--run-once` if you only want provisioning

## Install As Codex Skill

```bash
python3 scripts/install_skill.py --force
```

Optional custom location:

```bash
python3 scripts/install_skill.py --target-root /path/to/codex_home/skills --force
```

## Quick Start (Production)

```bash
python3 scripts/deploy_autopilot.py \
  --output-dir /path/to/workdir \
  --config-profile production \
  --repo-url https://github.com/<owner>/<repo>.git \
  --project-name <project-name> \
  --caller-name <your-orchestrator-name> \
  --branch dev \
  --git-user-name ai \
  --git-user-email ai@local \
  --cli-order codex,gemini,open-code,claude \
  --auto-disable-missing-clis \
  --init-env \
  --force
```

Then run:

```bash
cd /path/to/workdir
source .env
python3 doctor_autopilot.py --config openclaw_config.json
python3 openclaw_autopilot.py --config openclaw_config.json --once
```

Unattended loop:

```bash
./start_openclaw.sh
```

## Useful Runtime Overrides

```bash
# One CLI only
python3 openclaw_autopilot.py --config openclaw_config.json --only-cli codex --once

# Custom priority order
python3 openclaw_autopilot.py --config openclaw_config.json --cli-order gemini,codex --once

# Interactive session mode
python3 openclaw_autopilot.py --config openclaw_config.json --interactive-cli codex --interactive-max-turns 5
```

## Log Inspection

```bash
# Human-readable
python3 scripts/log_summary.py --log-dir /path/to/workdir/logs

# Human-readable with custom latest rounds window
python3 scripts/log_summary.py --log-dir /path/to/workdir/logs --tail-rounds 10

# JSON
python3 scripts/log_summary.py --log-dir /path/to/workdir/logs --json
```

## Contributor Smoke Test

```bash
python3 scripts/smoke_test_deploy.py
```

## Safety Notes

- Target branch is `dev` by default.
- Runtime artifacts (`.openclaw/*`, local CLI metadata dirs like `.codex/`) are excluded from commit.
- Logs include workflow events and audit outcomes; secrets are masked.

## License

MIT. See [LICENSE](./LICENSE).
