---
name: openclaw-api-control
description: Control a hosted OpenClaw instance through the OpenClaw as a Service API. Use when the user asks to talk to OpenClaw over API, send a folder or file to OpenClaw, read or write files in the OpenClaw workspace, run commands on OpenClaw, list or create hosted OpenClaw instances, or wire another agent to OpenClaw using an API key.
version: 0.1.1
license: MIT-0
author: fstandhartinger
env:
  - name: OPENCLAW_API_KEY
    required: true
    description: Bearer API key created from the OpenClaw account page. Scoped to the authenticated user's instances.
  - name: OPENCLAW_API_BASE_URL
    required: false
    default: https://openclaw-as-a-service.com/api
    description: Base URL of the OpenClaw as a Service API. Defaults to the production endpoint.
  - name: OPENCLAW_INSTANCE_ID
    required: false
    description: Target instance ID. When omitted, the skill auto-discovers the first ready instance owned by the API key holder.
security:
  network: outbound-only
  data-access: |
    This skill reads local files when the user explicitly requests an upload
    (e.g. "send this folder to OpenClaw") and transmits them to the user's
    own authenticated OpenClaw instance via HTTPS. No data is sent without
    an explicit user command. All API calls require a user-provided bearer
    token (OPENCLAW_API_KEY) and operate only on instances owned by that user.
---

# OpenClaw API Control

## Overview

Use the hosted OpenClaw API instead of the browser UI when an agent should operate an existing OpenClaw instance directly.

Required environment variables:

- `OPENCLAW_API_KEY`
- `OPENCLAW_API_BASE_URL`

Optional environment variables:

- `OPENCLAW_INSTANCE_ID`

Defaults:

- If `OPENCLAW_API_BASE_URL` is missing, use `https://openclaw-as-a-service.com/api`
- If `OPENCLAW_INSTANCE_ID` is missing, discover a ready instance automatically

## When To Use

- “Send this folder to my OpenClaw”
- “Upload these files into the OpenClaw workspace”
- “Ask my OpenClaw to continue this task”
- “Run this command on my hosted OpenClaw”
- “Read `/workspace/...` from OpenClaw”
- “Create an OpenClaw instance through the API”

## Workflow

1. Verify `OPENCLAW_API_KEY` is present.
2. Use `scripts/openclaw_api_client.mjs root` or `instances list` to confirm connectivity.
3. Resolve the target instance:
   - Prefer `OPENCLAW_INSTANCE_ID`
   - Otherwise pick the first `ready` instance from `instances list`
4. Choose the right action:
   - Chat: `chat send`
   - Recent history: `chat tail`
   - Files or folders: `files read`, `files write`, `files upload-tree`
   - Commands: `terminal exec`
5. Report the exact API action and result back to the user.

## Commands

### Discover API root

```bash
node scripts/openclaw_api_client.mjs root
```

### List instances

```bash
node scripts/openclaw_api_client.mjs instances list
```

### Create an instance

```bash
node scripts/openclaw_api_client.mjs instances create --invite-code YOUR_CODE
```

### Send a chat message

```bash
node scripts/openclaw_api_client.mjs chat send --message "Continue the task in /workspace"
```

### Stream a chat message

```bash
node scripts/openclaw_api_client.mjs chat send --stream --message "Narrate each step while you work"
```

### Upload a folder into `/workspace`

```bash
node scripts/openclaw_api_client.mjs files upload-tree --src ./my-project --dest /workspace/my-project
```

### Read a file

```bash
node scripts/openclaw_api_client.mjs files read --path /workspace/README.md
```

### Run a command

```bash
node scripts/openclaw_api_client.mjs terminal exec --command "pwd && ls -la /workspace"
```

## Notes

- `files upload-tree` only uploads text-like files and skips likely binary files.
- `chat tail` automatically reuses the latest chat session when no session id is supplied.
- The helper prints JSON for machine-friendly reuse.

## Resources

- `scripts/openclaw_api_client.mjs` - Minimal Node client for OpenClaw API operations
