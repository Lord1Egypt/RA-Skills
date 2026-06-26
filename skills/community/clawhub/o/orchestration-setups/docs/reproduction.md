# Reproducing the Setup

This package is meant to give another user and another agent the same orchestration shape without inheriting any private local setup.

## Goal

Reproduce this operating model:
- **OpenClaw main session** as control plane
- **Claude Code ACP** as default execution backend
- **Codex ACP** as secondary execution/fixer backend
- **File-native state** for handoffs, rolling summaries, checkpoints, and reviews

## Required pieces

### 1. OpenClaw gateway
A working OpenClaw installation with gateway access.

### 2. ACPX / ACP harnesses
You need the ACPX plugin and the backends you want to use.

Validated harness aliases in this setup:
- `claude`
- `codex`

### 3. Claude Code ACP unattended policy
For unattended Claude Code ACP runs, the gateway-side ACPX plugin should use:

```json
{
  "plugins": {
    "entries": {
      "acpx": {
        "enabled": true,
        "config": {
          "permissionMode": "approve-all",
          "nonInteractivePermissions": "deny"
        }
      }
    }
  }
}
```

This avoids failing on impossible interactive approval prompts while still denying non-interactive permission requests cleanly.

### 4. Codex ACP authentication
Codex ACP needs an OpenAI API key exposed to the gateway service environment.

Example systemd user drop-in:

```ini
[Service]
Environment="OPENAI_API_KEY=<your-openai-api-key>"
```

After changing the service environment:
1. `systemctl --user daemon-reload`
2. restart the OpenClaw gateway
3. rerun a smoke test

### 5. Rolling worker context
Long-running workers should maintain a rolling summary file that captures:
- what they have done
- what they are doing now
- what they learned / what matters next

This is required for context rollover, worker replacement, and graceful recovery under context pressure.

## Minimal smoke tests

### Claude Code ACP
Spawn a tiny worker that writes one `ok` file.
If it completes, the unattended policy is functioning.

### Codex ACP
Spawn a tiny worker that writes one `ok` file.
If it completes, the API key wiring is functioning.

## What this package does not include

- your secrets
- your service files
- your local gateway path layout
- your personal project/task data

It contains only the reusable orchestration pattern, docs, workflow packs, and skill instructions.
