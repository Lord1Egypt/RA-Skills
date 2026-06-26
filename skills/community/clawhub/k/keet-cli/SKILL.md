---
name: keet-cli
description: Safely operate and improve the Keet CLI project and Keet ↔ OpenClaw bridge. Use for read-only inspection, debugging, documentation, release checks, bridge supervision, and explicitly approved messaging workflows. Requires explicit user confirmation before any outbound message, invite action, chat creation, long-running bridge/daemon start, or Git push.
---

# Keet CLI

## Overview

Use this skill when operating or improving the `keet-cli` project for Keet Messenger and Keet ↔ OpenClaw bridge workflows.

Default to read-only inspection. Treat all live Keet profile data and private chat content as sensitive. Do not expose secrets, recovery material, private messages, invite/profile codes, or generated bridge state.

Project source to verify before use: `https://github.com/projectreturn/Keet-cli`.

## Required safety gates

Before any external or state-changing action, get explicit user confirmation for:

- exact Keet profile/storage path,
- exact target chat or room,
- exact outgoing message/action,
- whether a long-running process may remain active,
- exact Git repository, branch, and commit diff before pushing.

Never join invites, create chats, route additional chats, print recovery/account material, or push code unless the user explicitly asked for that exact action.

## Quick workflow

1. Locate the project repository. Common default: `/openclaw/workspace/keet-cli`.
2. Verify provenance and local state before using it:

```bash
git remote -v
git status --short --branch
npm run lint
node src/cli.js --help
```

3. Prefer read-only commands first.
4. Confirm the required safety gates before any send, bridge, daemon, invite, chat, or Git push action.
5. After edits, run `npm run lint` and inspect `git diff` before reporting completion.

## Read-only commands

Run from the repo root unless the user specifies another checkout.

```bash
npm run lint
node src/cli.js --help
node src/cli.js inspect
node src/cli.js rooms
node src/cli.js messages --limit 10
node src/cli.js tui
```

Override Keet storage only when the user provides or confirms the path:

```bash
KEET_APP_STORAGE=/confirmed/path/to/app-storage node src/cli.js inspect
```

## State-changing commands

Only run these after explicit confirmation of profile, target chat, and exact action:

```bash
node src/cli.js send 'confirmed message text'
node src/cli.js send-file --caption 'confirmed caption' /confirmed/file/path
node src/cli.js bridge
node src/cli.js daemon --socket .keet-cli.sock
node src/cli.js daemon-send --socket .keet-cli.sock current
node src/cli.js watch --interval 2000
```

For `send-file`, confirm the file path, target chat, and caption before sending. For `watch`, `daemon`, supervisor, or bridge modes, tell the user whether the process will keep running and how to stop it.

## Sensitive data rules

- Treat Keet profile storage, account/recovery material, private keys, tokens, invite/profile codes, bridge state, and logs with private messages as sensitive.
- Do not commit live Keet profile storage, generated state files, logs, screenshots of private chats, or copied private messages.
- Avoid printing message contents unless the user asked to inspect those exact messages.
- Redact secrets and private message content in summaries and errors.
- In shared/group contexts, do not reveal user-specific chat names, keys, paths, message contents, or operational details.

## Storage lock model

Keet Desktop and `keet-cli` should not use the same live storage concurrently. Keet protects the database with a device-file/FD lock.

If commands fail due to locking:

1. Check whether Keet Desktop or another `keet-cli` process is already using the profile.
2. Prefer one explicitly approved long-running owner process via `daemon --socket .keet-cli.sock` and route CLI/bridge actions through `daemon-send` instead of spawning competing sessions.
3. Do not kill user processes unless explicitly approved.

## TUI mode

Use TUI mode for interactive local inspection only after confirming that no other live Keet owner process is using the same storage:

```bash
node src/cli.js tui
```

The TUI can list rooms, select a room, view recent messages, and send messages. Sending is state-changing: confirm the target chat and exact message first.

## Daemon / REPL mode

Use daemon mode only when repeated reads/sends are needed and the user approved a long-running process:

```bash
node src/cli.js daemon --room ROOM_ID --socket .keet-cli.sock
```

Common REPL commands:

```text
/status
/messages 10
/send confirmed message text
/send-md **confirmed** _markdown_
/send-file /confirmed/file/path confirmed caption
/rooms
/current
/use ROOM_ID
/quit
```

Socket automation uses one JSON command per call:

```bash
node src/cli.js daemon-send --socket .keet-cli.sock status
node src/cli.js daemon-send --socket .keet-cli.sock send '{"text":"confirmed message","format":"plain"}'
node src/cli.js daemon-send --socket .keet-cli.sock send-file '{"filePath":"/confirmed/file/path","caption":"confirmed caption"}'
```

`send` and `send-file` try the default daemon socket first when present, then fall back to a direct Core session. Set `KEET_CLI_NO_DAEMON=1` to force direct mode, or `KEET_CLI_DAEMON_STRICT=1` to fail instead of falling back.

This avoids conflicts between separate `watch`, `send`, and `send-file` processes.

## Watch mode

Use watch mode only after the user confirms the profile and chat scope:

```bash
node src/cli.js watch --interval 2000
```

By default it should ignore local/self messages. Use `--include-local` only when explicitly needed for debugging.

## Keet ↔ OpenClaw bridge

Run the bridge in foreground for debugging first:

```bash
node src/cli.js bridge
node src/cli.js bridge --daemon-socket .keet-cli.sock --config bridge.config.json
```

Use supervisor/container modes only after the user confirms a persistent process is wanted.

Prefer `--daemon-socket` when a daemon owns the Keet profile. In that mode the bridge reuses the daemon instead of opening its own Core sidecar.

A safe bridge must:

- keep multi-room routing disabled by default,
- forward only explicitly approved chat(s) from a config allowlist,
- report invites/membership events without auto-joining or acting on them,
- fail closed when the target chat is ambiguous,
- ignore its own/local echo messages unless debugging requires them,
- persist enough state to avoid duplicate replies and the selected model mode,
- handle Keet audio messages locally when configured: download only from Keet's local file link, transcribe with local Whisper, and forward the transcript instead of raw audio,
- support explicit model switching commands such as `lokal`, `online`, and `modell status`,
- avoid logging private message contents or secrets,
- stop or provide a stop command when the task is complete.

## Release checklist

Before release or publishing:

```bash
npm run lint
git status --short --branch
git diff --stat
git log --oneline -5
```

Before any Git push, confirm the repository, branch, diff, and credential/identity that will be used. Do not embed private key paths or print private keys in public skill content.
