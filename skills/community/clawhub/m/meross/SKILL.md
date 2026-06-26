---
name: meross
description: Control Meross cloud plugs via local CLI commands. Use for discovery, state checks, and switch on/off actions.
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["MEROSS_EMAIL", "MEROSS_PASSWORD"] },
        "primaryEnv": "MEROSS_PASSWORD",
      },
  }
---

# Meross Skill (CLI)

Use local `node dist/cli.js` only.
Do not use plugin APIs.
Do not invent device mappings.

## Hard Gates

- Require `MEROSS_EMAIL` and `MEROSS_PASSWORD` before cloud commands.
- `MEROSS_REGION` is optional.
- In new/runtime-reset environments, ensure build exists: `npm install && npm run build`.
- If registry metadata conflicts with runtime behavior, trust runtime behavior.
- Never write credentials to `devices.json` or other files.
- Before every `set-device` command, show exact `deviceId`, capability, and value to the user and get explicit confirmation.

## Device Resolution Rules

- Resolve target by exact `deviceId` first.
- Fallback to alias from `devices.json`.
- If multiple matches or no match: stop and return ambiguity/missing-target guidance.
- Only `switch` capability is valid.

## Registry Rules

- Registry path: local `devices.json` in skill root.
- Refresh registry with:

```bash
node dist/cli.js setup-once '{}'
```

- `setup-once` rewrites device set to normalized entries:
  - `deviceId=plug_<normalized_uuid>`
  - `channel=0`
  - `capabilities=["switch"]`

## Command Interface

```bash
node dist/cli.js <command> '<json-input>'
```

Supported commands:

1. `list-devices`
2. `get-state`
3. `set-device`
4. `discover-cloud-devices`
5. `setup-once`

Core patterns:

```bash
node dist/cli.js list-devices '{}'
node dist/cli.js get-state '{"deviceId":"plug_abc"}'
node dist/cli.js set-device '{"deviceId":"plug_abc","capability":"switch","value":"on","confirmation":{"userConfirmed":true,"deviceId":"plug_abc","capability":"switch","value":"on"}}'
node dist/cli.js set-device '{"deviceId":"plug_abc","capability":"switch","value":"off","confirmation":{"userConfirmed":true,"deviceId":"plug_abc","capability":"switch","value":"off"}}'
node dist/cli.js discover-cloud-devices '{}'
node dist/cli.js setup-once '{}'
```

## Delayed Actions

For delayed switch commands:

- Show exact `deviceId`, capability, value, and absolute user-timezone timestamp before scheduling.
- Schedule only after explicit user confirmation.
- Include the same `confirmation` object in the scheduled `set-device` payload.
- Tell the user how to list and cancel the pending one-shot job before ending the turn.

## Error Contract

- Success: JSON on `stdout`
- Failure: JSON on `stderr`, non-zero exit
- Relevant error codes: `DEVICE_NOT_FOUND`, `DEVICE_OFFLINE`, `AUTH_FAILED`, `MEROSS_API_ERROR`, `INVALID_INPUT`, `REGISTRY_ERROR`, `AMBIGUOUS_DEVICE`, `CONFIRMATION_REQUIRED`, `INTERNAL_ERROR`
