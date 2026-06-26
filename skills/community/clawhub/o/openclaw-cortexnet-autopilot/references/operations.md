# Operations Playbook

## Quick Checklist
1. Deploy files with `deploy_autopilot.py`.
2. Fill `.env` with `GITHUB_TOKEN`.
3. Run `doctor_autopilot.py`.
4. Run single round with `--once`.
5. Confirm `first_round_report.md` and `round_reports.jsonl`.
6. Start long-running loop.

## One-Command Provisioning
If you want deploy + optional doctor/once in one step:

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

## Install Skill Into Codex
Use this when distributing to other machines:

```bash
python3 scripts/install_skill.py --force
```

## Recommended Deploy Command
```bash
python3 scripts/deploy_autopilot.py \
  --output-dir /path/to/workdir \
  --config-profile production \
  --repo-url https://github.com/<owner>/<repo>.git \
  --project-name "<project-name>" \
  --caller-name "你的自动化系统名" \
  --task-requirement "输入本轮希望自动完成的具体优化/功能需求" \
  --cli-order codex,gemini,open-code,claude \
  --require-code-changes \
  --force-reinit \
  --git-user-name ai \
  --git-user-email ai@local \
  --branch dev \
  --init-env \
  --auto-disable-missing-clis \
  --doctor-after-deploy
```

## Config Tuning Surface
Edit `openclaw_config.json` for routine tuning.

Profile note:
- `--config-profile default`: balanced starter baseline.
- `--config-profile production`: stricter baseline (`require_code_changes=true`) for unattended long-running loops.

High-impact keys:
- `cli_tools[].command`: host-specific CLI invocation.
- `cli_tools[].interactive_command`: interactive session command (Codex default injects prompt context).
- `cli_tools[].init_command`: one-time init-phase command for project context initialization.
- `cli_tools[].init_required_paths`: required init artifacts. Example: Codex defaults to `[".codex"]`; missing artifact means init failure and tool switch.
- `cli_tools[].enabled`: quickly disable unstable tool.
- CLI order in `cli_tools[]`: execution priority from top to bottom.
- `project_name`: project label injected into prompt and commit message.
- `task_requirement`: per-round concrete requirement injected into prompt.
- `caller_name`: caller identity injected into prompts (avoid hardcoded orchestrator name).
- `init_slash_command`: slash init command text used in init prompts (default `/init`).
- `git_identity.*`: committer identity used for push.
- `commit_message_template`: supports `{project}`, `{core}`, `{rate}`, `{changes}` placeholders.
- `timeouts.idle_seconds`: no-output threshold.
- `timeouts.progress_probe_after_seconds`: long-run probe trigger.
- `timeouts.progress_probe_wait_seconds`: wait after probe.
- `timeouts.max_runtime_seconds`: hard cap.
- `init_phase.enabled`: whether to run one-time CLI init before task execution.
- `init_phase.force_reinit`: force re-run init even when marker exists.
- `init_phase.idle_seconds`: no-output threshold during init.
- `init_phase.max_runtime_seconds`: hard cap during init.
- `report_min_pass_rate`: audit threshold.
- `require_code_changes`: when true, `no_changes` result is treated as failed and enters redo/switch flow.
- `require_non_doc_code_changes`: when true, docs-only changes are treated as failed and enters redo/switch flow.
- `minimum_non_doc_files_changed`: minimum count of changed non-doc files required for approval.
- `minimum_non_doc_lines_changed`: minimum changed non-doc lines (add+del) required for approval.
- runtime remote sync: before each CLI attempt, runtime fetches and hard-resets to remote latest branch.
- `preserve_untracked_paths`: paths excluded from `git clean` so init artifacts survive refresh rounds.
- `never_commit_paths`: paths forcibly unstaged before commit, preventing local CLI metadata from being pushed.
- `fallback_report.*`: missing-report recovery behavior.

## Fallback Report Guidance
Use fallback report when CLI is operational but unreliable at writing report JSON.

Recommended defaults:
- `fallback_report.enabled = true`
- `fallback_report.run_tests_on_missing_report = true`
- `fallback_report.test_command_candidates` includes `python -m pytest -q` first

Disable fallback only when strict "CLI must self-report" behavior is required.

## Log Files and Meaning
- `logs/openclaw_runner.log`: event timeline (JSONL)
- `logs/round_reports.jsonl`: one summary per round
- `logs/first_round_report.md`: first round human-readable summary
- `logs/runner.stdout.log`: launcher stdout/stderr aggregation
- `logs/PAUSED_REASON.txt`: latest pause reason snapshot for watchdog/monitoring

Quick summary command:

```bash
python3 scripts/log_summary.py --log-dir /path/to/workdir/logs
python3 scripts/log_summary.py --log-dir /path/to/workdir/logs --tail-rounds 10
```

## Contributor Validation
Run an offline smoke test before publishing changes:

```bash
python3 scripts/smoke_test_deploy.py
```

## Token Env Override
Use custom token env name when needed:

```bash
python3 openclaw_autopilot.py --config openclaw_config.json --token-env MY_GITHUB_TOKEN --once
```

## Runtime CLI Selection
Customize priority order for one run:

```bash
python3 openclaw_autopilot.py --config openclaw_config.json --cli-order codex,gemini,open-code,claude --once
```

Run only one CLI:

```bash
python3 openclaw_autopilot.py --config openclaw_config.json --only-cli claude --once
```

Run interactive session mode (single task, multi-turn redo supported):

```bash
python3 openclaw_autopilot.py --config openclaw_config.json --interactive-cli codex --interactive-max-turns 5
```

Notes:
- Codex interactive command defaults to `--no-alt-screen` to reduce terminal/TUI incompatibilities.
- The round prompt is injected as Codex initial user message, so the interactive session has task context from turn 1.
- If interactive startup fails and no report is produced, OpenClaw auto-falls back to the same CLI non-interactive command in that turn.
- Init prompt asks CLI to run `/init` first; if slash commands are unsupported, CLI should do equivalent context initialization.
- Init markers are persisted under `logs/init_state/<repo>/`, so init runs once per CLI/repo unless forced.
- Runtime keeps `.codex/` and other configured init directories during workspace clean; these paths are also excluded from commits by default.

## Safe Rollout Pattern
1. Run `--once` until one successful round appears.
2. Confirm no unexpected files are being committed.
3. Start unattended mode.
4. Monitor first 3 rounds before leaving unattended.

## Suggested Routine Ops
- Daily: inspect newest `round_reports.jsonl` entries.
- On CLI update: rerun `doctor_autopilot.py` and one `--once` round.
- On policy change: modify config first, avoid direct orchestrator edits unless required.
