# OpenClaw Upgrader Review Checklist

Use this checklist when preparing the Codex upgrade handoff or reviewing Codex's result.

## Upgrade contract

- Treat package installation as insufficient by itself
- Require runtime recovery and endpoint validation
- Fail the run if OpenClaw is upgraded but not operational
- If delegation cannot start, require a structured `delegation_blocked` result instead of an implicit failure
- Enforce at most one active upgrader run per host
- Require re-entry to be rejected or explicitly queued, never silently run concurrently

## Delegation prechecks

- Check whether Codex is installed
- Check whether Claude Code is installed
- Check whether each installed agent is authenticated/logged in
- Check whether each authenticated agent passes the documented lightweight delegation preflight
- Confirm the selected agent is recorded explicitly
- Confirm shell-only fallback is rejected
- Confirm blocked delegation is reported structurally, not just as prose
- Confirm rejected re-entry is reported structurally, not just as prose
- Confirm reviewers do not overinterpret preflight success as proof of full upgrade authority
- Confirm the preflight probe ("reply exactly: ok") is understood as a liveness check only, not a capability or permission proof; the delegated agent must re-verify its own authority when real upgrade actions begin
- Confirm there is a host-level mechanism preventing concurrent upgrader runs
- Confirm re-entry is rejected before any agent probe, preflight, or other side-effecting preparation begins
- Confirm the active-run lock covers the full upgrader lifecycle, not only context collection
- Confirm lock release happens only at terminal completion/abort in the outer runner, not automatically when the context collector exits
- Confirm the outer runner exists, owns the lock after context collection, and releases it on blocked, failed, and successful terminal paths

## Instance identity

- Confirm the exact instance identity before changing anything
- Pass `config_path`
- Pass `OPENCLAW_STATE_DIR` when available
- Pass `OPENCLAW_PROFILE` when available
- Pass actual service label / unit / task name when available
- Pass the intended endpoint
- Ensure upgrade, repair, restart, and validation target the same instance

## Service recovery

- Identify the host's actual service model
- Verify whether the updated install requires refreshed service definitions
- Refresh/reinstall service definitions if needed
- Restart/recover the correct service instance
- Confirm the service manager actually brought it back

## Endpoint verification

- Probe the real configured/local endpoint
- Do not rely on guessed defaults if better facts exist
- Distinguish `unreachable` from `reachable but requires auth`
- Use auth-aware probing when the gateway is protected

## Failure modes to watch

- package upgraded but service definition stale
- package upgraded but wrong instance repaired
- service restarted but process crashes on boot
- endpoint changed or no longer matches config/runtime
- auth-protected endpoint misclassified as down
- client usability still broken after nominal restart

## Result expectations

The result should include at minimum:

- previous and final version
- selected agent
- delegation status
- delegation block reason when blocked
- agent checks for Codex and Claude Code
- service-definition refresh status
- service recovery status
- endpoint status
- auth-aware probe status
- instance identity used
- repair actions taken
- final failure reason if unsuccessful
