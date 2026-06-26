# Troubleshooting

## Symptom: Codex exits immediately with reasoning effort error
Signature example:
- `unknown variant xhigh` in `model_reasoning_effort`

Fix:
- force valid value in command, e.g. `-c model_reasoning_effort=high`.
- for unattended execution, prefer explicit command form:
  `codex exec -s workspace-write -c approval_policy=never -c model_reasoning_effort=high ...`

## Symptom: Gemini terminated by idle timeout
Signature example:
- long gap after initial `stream-json` messages
- event `reason=idle_timeout`

Fix options:
- increase `timeouts.idle_seconds` (for slower tool phases)
- keep `-o stream-json`
- prefer Codex as primary, Gemini as fallback

## Symptom: Token check fails
Signature example:
- event `token.verify ok=false` with `http_401`

Fix:
- replace/rotate token
- ensure `.env` exports `GITHUB_TOKEN`
- rerun doctor with `--check-github-token`

## Symptom: No report produced
Signature example:
- `report.missing`

Fix:
- keep fallback report enabled
- ensure fallback test command candidates work in this repo
- if strict self-reporting is required, enforce via prompt and increase timeout budget

## Symptom: Init phase repeats every round
Signature example:
- frequent `cli.init.start` even after successful init

Fix:
- ensure `init_phase.force_reinit=false`
- keep log directory persistent (init markers are saved under `logs/init_state/...`)

## Symptom: CLI does not actually run `/init`
Signature example:
- init logs exist, but CLI output indicates unknown slash command

Fix:
- keep `init_slash_command` as `/init` for CLIs that support it
- for CLIs without slash-command support, rely on the fallback instruction in init prompt (equivalent repository scan/context setup)
- if needed, customize each `cli_tools[].init_command` to the tool's native initialization entrypoint

## Symptom: Init reports success but `.codex` (or required init directory) is missing
Signature example:
- `cli.init.failed` with `reason=required_artifacts_missing`
- Codex round repeatedly switches before task stage

Fix:
- ensure tool config includes correct `cli_tools[].init_required_paths` (Codex default should include `.codex`)
- verify `cli_tools[].init_command` really triggers CLI `/init` behavior for your installed version
- keep `preserve_untracked_paths` including `.codex/` so refresh clean does not delete init artifacts
- if your CLI writes a different folder name, update `init_required_paths` and `preserve_untracked_paths` accordingly

## Symptom: CLI fails before entering task (init failed)
Signature example:
- `cli.init.failed` in event log

Fix:
- verify `cli_tools[].init_command` is valid for this host/CLI version
- increase `init_phase.idle_seconds` / `init_phase.max_runtime_seconds`
- if this CLI has no reliable init path, set `init_phase.enabled=false` or disable that CLI

## Symptom: Commit fails with no staged changes
Signature example:
- `commit_failed` after fallback-generated files only

Fix:
- verify orchestrator excludes `.openclaw` runtime artifacts from staging
- determine commit necessity from staged diff (`git diff --cached --name-only`)

## Symptom: Round keeps retrying because no code changes are produced
Signature example:
- `audit.fail` with `gate=require_code_changes`

Fix:
- relax gate by setting `require_code_changes=false` when the repository is already in optimal state
- or make `task_requirement` more concrete so the CLI can produce deterministic file changes

## Symptom: Round keeps retrying because only docs changed
Signature example:
- `audit.fail` with `gate=require_non_doc_code_changes`

Fix:
- keep `require_non_doc_code_changes=true` for production quality, but make `task_requirement` explicitly target code modules and acceptance tests
- if this round is intentionally docs-only, set `require_non_doc_code_changes=false` for that run

## Symptom: Round keeps retrying because code changes are too small
Signature example:
- `audit.fail` with `gate=substantive_change_threshold`

Fix:
- increase the specificity and scope of `task_requirement` (target concrete modules and expected measurable outcomes)
- lower `minimum_non_doc_files_changed` or `minimum_non_doc_lines_changed` only when repository size or task scope truly does not support larger changes
- if the repository is already near-optimal, temporarily relax thresholds for that round and restore afterward

## Symptom: All CLIs unavailable
Signature example:
- `cli.available_set` is empty or only disabled tools

Fix:
- run doctor to detect missing binaries
- adjust `cli_tools[].command` per host (codex/claude/gemini/open-code)
- disable missing tools explicitly

## Symptom: Push failure
Signature example:
- `git.push ok=false`

Fix:
- verify token write permission for target repo/branch
- verify remote URL and branch protection policy
- rerun single round after permissions are fixed

## Symptom: Missing or wrong token env var
Signature example:
- runtime prints `缺少 GitHub Token 环境变量`

Fix:
- export expected env var name before run
- or run with `--token-env YOUR_ENV_NAME`

## Symptom: CLI override has no effect
Signature example:
- runtime log has `cli.only.unknown` or `cli.order.unknown`

Fix:
- use supported aliases: `codex`, `gemini`, `open-code`, `claude`
- or use exact configured names: `Codex CLI`, `Gemini CLI`, `Open Code CLI`, `Claude Code CLI`

## Symptom: Process paused and exited
Signature example:
- runtime prints `[PAUSED] ...`

Fix:
- inspect `logs/PAUSED_REASON.txt` for latest structured pause reason
- inspect `logs/openclaw_runner.log` around the same timestamp for detailed events

## Symptom: Interactive CLI mode does not start expected tool
Signature example:
- pause reason includes `未找到指定CLI`

Fix:
- ensure CLI exists in current `cli_tools` and is enabled
- use aliases: `codex`, `gemini`, `open-code`, `claude`
- if combined with `--only-cli`, ensure target CLI is included

## Symptom: Codex interactive mode shows unstable full-screen behavior
Signature example:
- terminal cannot keep scrollback
- visible control characters / difficult input handling

Fix:
- use `--no-alt-screen` in `cli_tools[].interactive_command`
- keep Codex interactive command as template default:
  `codex --no-alt-screen -c model_reasoning_effort=high -C {repo_dir} "$(cat {prompt_path})"`
- if startup still fails, confirm log event `cli.interactive.fallback_noninteractive` appears (OpenClaw will continue with non-interactive mode automatically)

## Symptom: repo_url is placeholder or invalid
Signature example:
- `config.repo_url.valid` is error in doctor
- runtime prints `repo_url 仍是占位值`

Fix:
- set a real GitHub repo URL in `openclaw_config.json`, e.g. `https://github.com/<owner>/<repo>.git`
- or deploy with `--repo-url ...` to override template defaults
