# Orchestration V1

Minimal OpenClaw-native control plane for multi-agent workflows.

> Note: this document is preserved as a **runtime reference** from the original V1 implementation. It describes the original file-native runtime shape and may mention helper scripts that are not bundled directly inside this public folder.

## Layout
- `agents/` agent archetypes and contracts
- `workflows/` reusable workflow state machines
- `runs/` durable run state
- `templates/` handoff/review/checkpoint/temporary-context templates
- `scripts/orchestration/` runtime helpers
- `COMMUNICATION.md` communication model (stable context, handoff, temporary context)
- `PROJECT_BUILDER_WORKTREE.md` git/worktree protocol for project-builder
- `OPENCLAW_LAUNCHER.md` launcher protocol from launch manifests to real subagent spawns

## Typical flow
1. Create a run
2. Dispatch the current phase
3. Execute work with a sub-agent using the generated handoff packet
4. Mark the phase complete, or apply a structured review to route retries
5. Use watchdog/status for recovery and monitoring

## Commands
```bash
python3 scripts/orchestration/run_workflow.py project-builder --goal "Build X" --project-root /path/to/repo
python3 scripts/orchestration/prepare_project_builder.py <run-id> --project-root /path/to/repo --slot main --bootstrap-context
python3 scripts/orchestration/dispatch_step.py <run-id> --targets backend,frontend
python3 scripts/orchestration/complete_step.py <run-id> --summary "Spec done" --artifact spec=shared/specs/x.md
python3 scripts/orchestration/apply_review.py <run-id> agent/orchestration/runs/<run-id>/reviews/review-round1.md
python3 scripts/orchestration/escalate_run.py <run-id> --severity high --reason "..." --target human --next-action "..."
python3 scripts/orchestration/list_pending_launches.py
python3 scripts/orchestration/launcher_preflight.py
python3 scripts/orchestration/mark_launch.py <manifest-path> <session-key>
python3 scripts/orchestration/publish_worktree_branch.py <run-id> --slot main
python3 scripts/orchestration/status.py
python3 scripts/orchestration/watchdog.py --stale-minutes 45
```

## Notes
- Dispatch currently generates handoff packets and updates durable run state.
- Actual sub-agent spawning remains OpenClaw-native from the orchestrator session.
- Run `launcher_preflight.py` before launching manifests. If it reports gateway pressure, do not trust an erroring `sessions_spawn` result as a real launch.
- Stable project context should live in `README.md` + `CLAUDE.md` at the repo/worktree root when available.
- Rich temporary shared context lives under `runs/<run-id>/working-memory/`.
- This keeps V1 robust without coupling local scripts to a specific external runtime.
