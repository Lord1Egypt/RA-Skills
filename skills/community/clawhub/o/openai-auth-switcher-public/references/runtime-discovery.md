# Runtime discovery

## Goal

Avoid machine-specific assumptions such as fixed `/root/.openclaw` paths when distributing the skill publicly.

## Resolution order

Path discovery should follow this order:

1. explicit environment variables
2. common default locations
3. fail with a clear diagnostic message

## Supported environment overrides

- `OPENCLAW_ROOT`
- `OPENCLAW_WORKSPACE`
- `OPENCLAW_AGENT_ROOT`
- `OPENCLAW_SESSION_ROOT`
- `OPENAI_AUTH_SWITCHER_PUBLIC_STATE_DIR` (recommended for keeping public skill runtime state outside the source tree during testing)

## Common defaults to probe

OpenClaw root candidates:

- `~/.openclaw`
- `/root/.openclaw` (only when running as root on a root-owned installation)

Workspace candidates:

- `$OPENCLAW_ROOT/workspace`
- current working directory if it looks like an OpenClaw workspace

## Required runtime files for switch operations

Public runtime checks should look for these before claiming the environment is compatible:

- `agents/main/agent/auth-profiles.json`
- `agents/main/agent/models.json` (optional but useful)
- OpenClaw workspace directory

## Failure behavior

If runtime discovery fails:

- do not guess silently
- do not write fallback data into arbitrary directories
- explain which path was expected and how to override it

## Publishing note

Any script that still requires a hard-coded host path is not ready to be advertised as portable in ClawHub metadata.
