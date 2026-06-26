# OpenClaw Meross Skill

Local OpenClaw skill for Meross cloud plugs (`switch`) via `meross-cloud`.

## Scope

- Controls Meross cloud devices with `switch` capability only.
- Supports: registry bootstrap, device listing, state read, switch on/off, cloud discovery.
- Uses local registry file `devices.json` in skill root.

## Prerequisites

- Node.js >= 18
- npm
- Meross cloud account

## Required Setup

Run in skill root:

```bash
npm install
npm run build
```

Set runtime environment:

```bash
export MEROSS_EMAIL='user@example.com'
export MEROSS_PASSWORD='***'
export MEROSS_REGION='eu' # optional
```

Registry metadata may miss env/install hints. Treat setup above as mandatory.

## Quick Start

```bash
node dist/cli.js setup-once '{}'
node dist/cli.js list-devices '{}'
node dist/cli.js get-state '{"deviceId":"plug_abc"}'
node dist/cli.js set-device '{"deviceId":"plug_abc","capability":"switch","value":"off","confirmation":{"userConfirmed":true,"deviceId":"plug_abc","capability":"switch","value":"off"}}'
node dist/cli.js discover-cloud-devices '{}'
```

`set-device` fails unless the caller includes an explicit confirmation object that exactly matches the resolved target and requested switch value.

## `devices.json`

- Written by `setup-once`; discovered devices replace prior set.
- Contains device identifiers and aliases; keep file access controlled.
- `setup-once` writes registry data with owner-only permissions where the OS supports `chmod`.
- Never store account credentials in project files.

## CLI Contract

- Success: JSON on `stdout`
- Failure: JSON on `stderr`, exit code `1`
- Switch writes may fail with `CONFIRMATION_REQUIRED` until the exact target/action has user approval.

If source/dependency trust is unclear, use isolated runtime and test credentials.
