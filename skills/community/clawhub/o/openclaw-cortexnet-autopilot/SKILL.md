---
name: openclaw-cortexnet-autopilot
description: Deploy, diagnose, and operate an unattended GitHub-repo optimization loop for OpenClaw with multi-CLI failover, layered timeout controls, report-only audit gates, fallback report generation, and dev-branch auto commit/push. Use when users ask to set up, run, harden, troubleshoot, or scale OpenClaw automation for Codex CLI, Claude Code CLI, Gemini CLI, and optional Open Code CLI across any repository and custom requirement.
---

# OpenClaw Repo Autopilot

Deploy and run a production-style autopilot for any GitHub repository.

Use bundled scripts and templates instead of rebuilding orchestrators from scratch.

## Core Workflow
1. Deploy templates.
2. Diagnose environment and CLI availability.
3. Patch config for the actual host.
4. Run one round (`--once`) and inspect logs.
5. Run unattended mode.

## Deploy
Use this when the user asks to initialize a new workspace.

Fastest path (wrapper):

```bash
python3 scripts/setup_autopilot.py \
  --output-dir /path/to/workdir \
  --repo-url https://github.com/<owner>/<repo>.git \
  --config-profile production \
  --token "<github_token>" \
  --run-doctor \
  --run-once \
  --force
```

```bash
python3 scripts/deploy_autopilot.py \
  --output-dir /path/to/workdir \
  --config-profile production \
  --repo-url https://github.com/<owner>/<repo>.git \
  --project-name "<project-name>" \
  --caller-name "你的自动化系统名" \
  --task-requirement "按你的目标执行迭代需求（可以是性能、功能、重构或修复）" \
  --git-user-name ai \
  --git-user-email ai@local \
  --require-code-changes \
  --branch dev \
  --init-env \
  --auto-disable-missing-clis \
  --doctor-after-deploy \
  --print-diagnose-cmd
```

Notes:
- `--config-profile production` uses production baseline (includes `require_code_changes=true`) and then applies CLI args overrides.
- production profile also enables stronger substance gates by default: `require_non_doc_code_changes=true`, `minimum_non_doc_files_changed=2`, `minimum_non_doc_lines_changed=30`.
- `--auto-disable-missing-clis` prevents immediate failures on hosts without `claude`, `open-code`, or `gemini`.
- `--init-env` creates `.env` from `.env.example` when missing.
- `--task-requirement` is injected into runtime prompt and can be any concrete user requirement.
- `--caller-name` controls how the orchestrator is referenced inside CLI prompts; avoid hardcoding caller identity.
- `--repo-url` should always be set to a real repo URL. Placeholder values will fail doctor/runtime checks.
- `--doctor-after-deploy` runs doctor immediately and returns non-zero on health failure.
- `--cli-order` lets you customize priority order.
- `--only-cli` restricts execution to specific CLI(s).
- `--interactive-cli` enters selected CLI interactive session mode for one task.
- `--interactive-max-turns` controls max redo turns in interactive session mode.
- Codex interactive mode auto-loads the round prompt as initial context and uses `--no-alt-screen` for better terminal compatibility.
- `--require-code-changes` enables a hard gate: `no_changes` is treated as audit failure and will trigger redo/switch logic.
- Init phase is enabled by default: each CLI runs a one-time repository initialization before real task execution.
- Init behavior now explicitly asks CLI to run `/init` first (or perform equivalent initialization if slash command is unsupported).
- Codex defaults to `init_required_paths=[".codex"]`; if `.codex` is not created, init is treated as failed.
- Runtime keeps `.codex/` (and other configured init directories) during `git clean`, and excludes them from commits.
- `--disable-init-phase` turns off init phase; `--force-reinit` forces init to run again.

## Diagnose Before First Run
Use this before `--once` and after any host/toolchain change.

```bash
python3 scripts/doctor_autopilot.py --config openclaw_config.json
```

For token validation:

```bash
python3 scripts/doctor_autopilot.py --config openclaw_config.json --check-github-token
```

Doctor checks:
- required config keys
- CLI binary existence and version probing
- Codex/Gemini login status hints
- optional GitHub token validity

## Run Modes
One-round validation:

```bash
source .env
python3 openclaw_autopilot.py --config openclaw_config.json --once --token-env GITHUB_TOKEN
```

Unattended loop:

```bash
./start_openclaw.sh
```

## Runtime Contract
Keep these behaviors unless the user explicitly asks to change policy:
- Default CLI priority: Codex CLI -> Gemini CLI -> Open Code CLI -> Claude Code CLI.
- Before every CLI attempt, runtime fetches and resets to remote latest `origin/dev` to avoid drift with external commits.
- Timeout policy:
  - `30s` no output: terminate and switch.
  - `15min` runtime: send progress probe.
  - `5min` no useful probe response: terminate and switch.
  - `30min` hard cap: terminate and switch.
- Loop anomaly: repeated same operation output >3 times -> terminate.
- Audit policy: report-only (`run_status`, `test_pass_rate`, summary fields).
- Approval gate: `run_status` successful and `test_pass_rate >= 90`.
- Optional gate: when `require_code_changes=true`, rounds with no staged code changes are treated as failed and retried/switched.
- Optional gate: when `require_non_doc_code_changes=true`, rounds with docs-only changes are treated as failed and retried/switched.
- Substantive gate: when `minimum_non_doc_files_changed` / `minimum_non_doc_lines_changed` are set, rounds below threshold are treated as failed and retried/switched.
- Init gate: when enabled, CLI must pass one-time init phase (with timeout control) before entering task execution.
- Init artifact gate: required init directories (such as `.codex`) must exist after init or the tool is switched.
- Git policy: commit/push only to `dev`.
- Git identity default: `ai <ai@local>`.
- Commit message includes concrete change summary (`A/M/D + file paths`).
- On paused state, writes `logs/PAUSED_REASON.txt` for external monitors.

Runtime override examples:
```bash
python3 openclaw_autopilot.py --config openclaw_config.json --cli-order codex,gemini,open-code,claude --once
python3 openclaw_autopilot.py --config openclaw_config.json --only-cli gemini --once
python3 openclaw_autopilot.py --config openclaw_config.json --interactive-cli codex --interactive-max-turns 5
```

## Fallback Report Policy
If CLI exits without writing report JSON, autopilot can generate fallback report.

Default fallback behavior:
- run validation command candidates (pytest first)
- infer pass rate from output
- write standard report JSON
- continue audit pipeline using fallback report

Config keys live in `fallback_report` inside `openclaw_config.json`.

## Minimal-Change Tuning Order
When users ask to improve behavior, patch in this order:
1. `openclaw_config.json` thresholds and CLI commands.
2. fallback test command candidates.
3. CLI ordering/enabled flags.
4. only then edit orchestrator logic.

## Bundled Files
- `scripts/deploy_autopilot.py`: deploy templates + apply practical overrides.
- `scripts/doctor_autopilot.py`: host and config diagnostics.
- `scripts/setup_autopilot.py`: one-command setup wrapper for deploy + optional doctor/once run.
- `scripts/log_summary.py`: summarize round and event logs quickly.
- `scripts/install_skill.py`: install this skill repo into local Codex skills directory.
- `scripts/smoke_test_deploy.py`: offline smoke test for deploy/runtime templates.
- `assets/templates/openclaw_autopilot.py`: orchestrator template.
- `assets/templates/openclaw_config.json`: default runtime config.
- `assets/templates/openclaw_config.production.json`: production baseline config.
- `assets/templates/start_openclaw.sh`: unattended launcher.
- `assets/templates/.env.example`: token env template.

## References
Read these only when needed:
- Operational details: [references/operations.md](references/operations.md)
- Failure signatures and fixes: [references/troubleshooting.md](references/troubleshooting.md)
