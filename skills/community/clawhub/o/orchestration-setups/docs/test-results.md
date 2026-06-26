# Test Results

## Goal
Check whether the documented orchestration backends are actually runnable from the current environment.

## 2026-04-21 smoke tests

### 1. OpenClaw subagent
**Status:** PASS

What was tested:
- spawned a simple `runtime="subagent"` worker
- asked it to write `test-artifacts/openclaw-subagent-ok.txt`

Result:
- worker completed successfully
- file creation succeeded

### 2. ACP Claude Code
**Status:** PASS (after ACPX permission policy fix)

What was tested:
- spawned a simple `runtime="acp"`, `agentId="claude"` worker
- asked it to write a control file under `test-artifacts/`

Result:
- initial attempt failed with: **Permission prompt unavailable in non-interactive mode**
- fixed by setting ACPX runtime policy to:
  - `permissionMode: "approve-all"`
  - `nonInteractivePermissions: "deny"`
- after gateway restart, Claude Code ACP completed successfully

Interpretation:
- Claude Code ACP is now usable for unattended smoke-test level runs in this environment

### 3. ACP Codex
**Status:** PASS (after OpenAI key injection)

What was tested:
- spawned a simple `runtime="acp"`, `agentId="codex"` worker
- asked it to write a control file under `test-artifacts/`

Result:
- initial attempt failed with: **Authentication required**
- fixed by injecting `OPENAI_API_KEY` into the `openclaw-gateway.service` environment from the existing OpenClaw auth profile
- after gateway restart, Codex ACP completed successfully

Interpretation:
- Codex ACP is now usable for unattended smoke-test level runs in this environment

## Current practical conclusion

What works right now:
- OpenClaw subagents
- ACP Claude Code
- ACP Codex

## Recommendation

Keep the repo architecture Claude Code first.
Claude Code ACP and Codex ACP are now both validated for basic unattended runs here.
Use Claude Code as the default builder/reviewer backend, and Codex as a secondary builder/fixer where useful.
