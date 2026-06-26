---
name: openclaw-upgrader
description: Upgrade OpenClaw to a specific version or latest using a cross-platform, Codex-supervised flow. Use when the user asks to upgrade or update OpenClaw. OpenClaw should do lightweight pre-upgrade preparation itself, then hand the full upgrade, restart, recovery, service-definition refresh, and verification workflow to Codex with a strong prompt.
---

# OpenClaw Upgrader

Use this skill for **cross-platform, same-host OpenClaw upgrades**. Keep the skill focused on one job:

1. OpenClaw does the minimal safe preparation itself
2. A local ACP/CLI coding agent (Codex or Claude Code) executes the full upgrade and recovery workflow on the same host
3. Success means the upgraded OpenClaw runtime is usable again, not merely that package installation finished

## Core contract

Do not treat this as a shell script wrapper skill. Treat it as a **same-host ACP/CLI delegation skill**.

This skill is for upgrading the OpenClaw installation on the **same host** where the delegated coding agent runs. It is cross-platform across host OS/service models, but it is not a generic remote-host orchestration skill.

Concurrency contract:
- On a given host, allow at most **one active openclaw-upgrader run at a time**.
- If a second run is requested while one is active, do not run them concurrently.
- The caller must either reject re-entry immediately or queue it explicitly.
- Prefer immediate rejection by default unless the caller has a real queueing mechanism.

OpenClaw should do only lightweight preparation before delegation:

- detect current version
- identify likely package manager / install method if easy to determine
- back up the config
- collect relevant environment facts for Codex
- formulate a strong Codex prompt

Use `scripts/collect-upgrade-context.sh` to gather a machine-readable context snapshot before delegation. That script must reject re-entry before agent preflights and may claim the host-level active-run lock on behalf of the outer upgrader flow. Use `scripts/run-upgrade-delegation.sh` as the outer runner scaffold so the lock is released only when the upgrader flow reaches a terminal path. Read `references/review-checklist.md` when composing or reviewing the Codex handoff.

After that, hand off the full upgrade workflow to a local coding agent: prefer Codex; use Claude Code if Codex is unavailable or unsuitable.

## What success means

An upgrade is successful only if all of these are true:

1. OpenClaw version is at the requested target, or already latest/target
2. The correct OpenClaw Gateway/service instance is running again under the host's service model
3. The correct configured/local Gateway endpoint is reachable again
4. Authentication-aware probing shows the endpoint is live, even if it is protected
5. OpenClaw can serve the intended local clients again
6. No required post-upgrade recovery step remains pending

If package installation succeeded but the runtime did not recover, report **failure**, not success.

## Cross-platform rule

Do not hardcode macOS-specific assumptions into the skill contract.

Examples:
- Do not require `LaunchAgent` in the generic rules
- Do not hardcode `127.0.0.1:18789` as the only valid endpoint
- Do not assume only one service manager exists

Instead, require Codex to verify the appropriate host-specific service model and the actual configured/local endpoint.

Examples of host-specific service models Codex may need to handle:
- macOS LaunchAgent / launchctl
- Linux systemd / service managers
- containerized or manually supervised installs
- other local supervisor arrangements

## What OpenClaw should do before delegation

Do these directly before spawning the delegated agent:

1. Enforce the single-active-run lock for this host before any agent probe, preflight, or other side-effecting preparation
2. Detect current version
3. Back up config
4. Check agent availability and delegation preconditions
5. Record key runtime facts, if cheaply available
6. Pass those facts into the delegated-agent task

The run lock must cover the entire active upgrader lifecycle, not just context collection. `scripts/collect-upgrade-context.sh` may claim the host-level run lock and emit lock metadata, but the caller/outer runner must retain that lock until the delegated upgrade run reaches a terminal state and then release it deliberately. `scripts/run-upgrade-delegation.sh` is the default outer-runner scaffold for this purpose and must remain responsible for terminal lock release.

If delegation cannot begin, OpenClaw itself must write a structured pre-delegation failure result. Do not leave blocked delegation as an implicit or unstructured failure.
If another upgrader run is already active on this host, reject re-entry or explicitly queue it; do not allow concurrent execution.

Useful facts to pass:
- current version
- requested target version
- install method clues (`npm`, `pnpm`, `yarn`, package manager, custom)
- config path
- state dir / profile context if present (`OPENCLAW_STATE_DIR`, `OPENCLAW_PROFILE`)
- expected gateway/service command(s)
- actual service label / unit / task name, if known
- known local endpoint, if known
- endpoint auth mode, if known
- token/password source or auth expectation, if known
- OS / platform
- any recent failure mode already observed by the user
- Codex installed/auth/preflight status
- Claude Code installed/auth/preflight status
- selected agent, if any
- delegation block reason, if delegation cannot start

When multiple OpenClaw instances may exist, pass enough identity information that Codex can upgrade, repair, and verify the **same instance**.

## Delegated agent responsibility

The delegated local coding agent (Codex or Claude Code) owns the full upgrade flow after handoff. That includes:

1. Determine the correct upgrade path for this host
2. Execute the upgrade
3. Refresh or reinstall the host-native service definition if the updated install requires it
4. Restart or recover the correct Gateway/service instance
5. Detect broken post-upgrade states
6. Repair them
7. Verify end-to-end usability
8. Write a structured result

## Agent selection and fallback

Before delegation, check whether a supported local coding agent is actually usable.

Preferred order:
1. Codex
2. Claude Code

Check all of the following before selecting an agent:
- CLI is installed and invokable
- CLI is authenticated/logged in
- CLI passes a lightweight, non-destructive delegation-viability preflight on this host

Important: this preflight is a necessary but not sufficient condition. It is only meant to reject obviously unusable agents before delegation. It does not prove that the agent will definitely succeed at package upgrade, service recovery, verification, or file writes during the real run.

Handle these cases explicitly:

### No supported CLI installed

If neither Codex nor Claude Code is installed, stop and report that the skill cannot proceed yet. Do not silently fall back to a shell-only upgrade flow. Write a structured result with status `delegation_blocked`.

### CLI installed but not logged in

If a CLI is installed but not authenticated, stop and report that the selected agent is unavailable until login/auth is completed. If no other supported agent is usable, write a structured result with status `delegation_blocked`.

### CLI logged in but fails delegation preflight

If a CLI is authenticated but fails the lightweight delegation-viability preflight, treat it as unavailable for this task and try the other supported CLI if present. If neither agent passes preflight, stop and report that delegation cannot safely continue, and write a structured result with status `delegation_blocked`.

Do not overclaim what the preflight proves. A passing preflight only means the agent looks viable enough to start delegation; it does not prove that the full upgrade workflow will succeed.

### Both available

Prefer Codex by default. Use Claude Code when Codex is unavailable, unauthenticated, or lacks the needed capabilities.

OpenClaw should record the selected agent explicitly before delegation.

## What the delegated-agent prompt must emphasize

The most important part of this skill is the prompt quality. The prompt to the delegated agent should strongly emphasize these points:

### 1. Treat runtime recovery as part of the upgrade

Tell the delegated agent explicitly:

- The upgrade is not complete when package installation finishes
- The upgrade is only complete when OpenClaw is operational again
- Broken service state after install is a failed upgrade and must be repaired
- If the updated install ships or expects refreshed service definitions, refresh/reinstall them before concluding recovery failed

### 2. Work from the host's real service model

Tell the delegated agent to infer and verify the real service management model on the host instead of assuming macOS or any single supervisor.

Examples:
- inspect how OpenClaw is currently launched
- inspect current service state
- restart/reload using the correct host-native mechanism
- refresh or reinstall the host-native service definition if needed after upgrade
- verify that the service manager actually brought the runtime back

### 3. Verify the real endpoint, not a guessed one

Tell the delegated agent to validate the real configured/local Gateway endpoint.

Do not let Codex stop after a restart command. Require it to verify actual reachability.

Require authentication-aware verification:
- if the endpoint responds and is auth-protected, treat that as reachable service, not dead service
- use the available auth context when appropriate
- distinguish "unreachable" from "reachable but requires auth"
- continue validating real host operations during the delegated run instead of assuming the preflight proved everything

### 4. Distinguish package success from runtime success

Tell the delegated agent to separately evaluate:

- package/install success
- service-definition refresh success
- service recovery success
- endpoint reachability
- authenticated or auth-aware probe success
- client usability
- whether the delegated run actually retained enough permissions/capabilities once real upgrade actions began

If the first passes and the latter fail, overall status must still be failure.

### 5. Prefer diagnosis + repair over blind retries

Tell the delegated agent to inspect the failure mode and repair the actual cause.

Examples of causes:
- service manager failed to reload
- updated install requires refreshed service definition
- unit/agent not loaded
- wrong instance label/unit/task repaired
- process crashed on boot
- config/env regression after upgrade
- port/endpoint mismatch
- stale wrapper / broken launch target
- auth assumptions wrong during endpoint verification

### 6. Keep instance identity stable through the whole run

Tell the delegated agent to identify the exact OpenClaw instance being upgraded and use the same identity for upgrade, repair, restart, and validation.

Useful identity anchors include:
- config path
- `OPENCLAW_STATE_DIR`
- `OPENCLAW_PROFILE`
- service label/unit/task name
- endpoint
- runtime working directory

Do not allow "upgraded one instance, repaired another" outcomes.

### 7. Leave a machine-readable result

Require the delegated agent to write a structured result file with:
- prior version
- final version
- upgrade status
- service-definition refresh status
- service recovery status
- endpoint reachability status
- auth-aware endpoint probe status
- instance identity used
- key repair actions taken
- final error if unsuccessful
- log location

## Suggested delegated-agent prompt template

Use a prompt roughly like this, adapted to the environment and selected agent:

```text
Upgrade OpenClaw to <TARGET_VERSION> on this host.

You are the delegated local coding agent for this host. You own the full upgrade workflow end to end: package upgrade, service-definition refresh if needed, service recovery, endpoint verification, and post-upgrade validation.

Facts:
- Current version: <CURRENT_VERSION>
- Target version: <TARGET_VERSION>
- OS/platform: <PLATFORM>
- Config path: <CONFIG_PATH>
- Install method clues: <INSTALL_METHOD_HINTS>
- State dir: <STATE_DIR_OR_UNKNOWN>
- Profile: <PROFILE_OR_UNKNOWN>
- Service label/unit/task: <SERVICE_IDENTITY_OR_UNKNOWN>
- Known Gateway endpoint: <KNOWN_ENDPOINT_OR_UNKNOWN>
- Endpoint auth mode: <AUTH_MODE_OR_UNKNOWN>
- Auth source/expectation: <AUTH_SOURCE_OR_UNKNOWN>
- Known recent failure mode: <KNOWN_FAILURE_MODE>
- Config backup already created at: <BACKUP_PATH>

Requirements:
1. Determine the correct host-specific upgrade path
2. Perform the upgrade
3. Refresh or reinstall the host-native service definition if the updated install requires it
4. Recover/restart the correct Gateway instance using the host's actual service model
5. Verify the real configured/local Gateway endpoint is reachable again
6. Use auth-aware probing so "reachable but requires auth" is not misclassified as downtime
7. Verify OpenClaw is operational for the intended local clients again
8. If package install succeeds but runtime recovery fails, treat the overall result as failure and repair it
9. Write a structured result file to ~/.openclaw/.upgrade-result.json

Do not stop at “package upgraded” or “restart issued”. The task is only complete when the intended OpenClaw instance is operational again.

Treat the preflight fields you were given as an initial viability signal, not a proof of full upgrade authority. Re-check permissions/capabilities when the real upgrade actions begin.
```

## Result file

Write structured output to:

```bash
~/.openclaw/.upgrade-result.json
```

Expected shape:

```json
{
  "status": "success | failed | already_latest | in_progress | delegation_blocked | rejected_reentry",
  "start_time": "2026-03-13T20:00:00",
  "end_time": "2026-03-13T20:02:30",
  "previous_version": "2026.3.12",
  "new_version": "2026.3.13",
  "selected_agent": "codex | claude-code | none",
  "delegation_status": "started | blocked | rejected_reentry | queued | not_needed | unknown",
  "delegation_block_reason": "not_installed | not_authenticated | insufficient_capability | active_run_exists | unknown | null",
  "agent_checks": {
    "codex": {
      "installed": true,
      "authenticated": true,
      "preflight_ok": true
    },
    "claude_code": {
      "installed": false,
      "authenticated": false,
      "preflight_ok": false
    }
  },
  "service_definition_status": "refreshed | unchanged | failed | unknown | not_started",
  "service_status": "healthy | unhealthy | unknown | not_started",
  "endpoint_status": "reachable | unreachable | unknown | not_started",
  "auth_probe_status": "ok | auth_required | failed | unknown | not_started",
  "service_model": "launchctl | systemd | manual | container | unknown | not_started",
  "instance_identity": {
    "config_path": "...",
    "state_dir": "...",
    "profile": "...",
    "service_name": "...",
    "endpoint": "..."
  },
  "repair_actions": ["..."],
  "error": "Error message if failed",
  "log_file": "/tmp/openclaw-upgrade-20260313-200000.log"
}
```

## Important notes

1. Keep OpenClaw-side preparation light
2. Delegate the real upgrade workflow to a supported local coding agent
3. Prefer Codex, but support Claude Code as a first-class fallback
4. Refuse shell-only fallback when no suitable coding agent is available
5. Enforce single-active-run semantics on the host; reject or explicitly queue re-entry
6. If delegation cannot begin, OpenClaw must write a structured `delegation_blocked` or `rejected_reentry` result itself
7. Make the delegated-agent prompt strict about recovery and verification
8. Keep the skill cross-platform
9. Never equate package installation with upgrade success
10. Never let the delegated agent repair or verify the wrong OpenClaw instance
11. Never let auth-protected reachability be mistaken for outage
