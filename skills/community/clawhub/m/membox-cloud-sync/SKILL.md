---
name: membox-cloud-sync
description: Private zero-knowledge encrypted cross-device memory sync, backup, and recovery for OpenClaw. Helps agents install Membox, pair devices, securely sync `MEMORY.md` and `memory/YYYY-MM-DD.md`, and restore encrypted memory while keeping plaintext, passphrases, AMK, and recovery codes local-only.
---

# Membox Cloud Sync

Use this skill for private, zero-knowledge, encrypted cross-device Membox-backed memory sync, backup, and recovery flows.

## Load Only What You Need

- Read [references/workflows.md](references/workflows.md) first for the end-to-end operating model.
- Read [references/distribution.md](references/distribution.md) when the task is about installing the plugin, installing the skill, ClawHub distribution, or the "user says one sentence and the agent does the rest" flow.
- Read [references/api-surface.md](references/api-surface.md) when you need exact HTTP endpoints, payloads, or response fields.
- Read [references/scheduling.md](references/scheduling.md) when the user wants daily checks, periodic uploads, or local restore orchestration.
- When the user needs the plugin + skill installed together:
  - preferred published path: run `openclaw plugins install @membox-cloud/membox` and then `clawhub install membox-cloud-sync`

## Non-Negotiable Rules

1. Install the plugin before using Membox tools. If `membox_*` tools are unavailable, install `@membox-cloud/membox` first.
2. If the plugin or skill was installed during the current OpenClaw conversation and the `membox_*` tools still do not exist, start a new OpenClaw session or next run before continuing.
3. Log in first. Do not start sync, polling, upload, restore, revoke, or scheduling work until the agent has a valid Membox session or device grant flow in progress.
4. Prefer the plugin tool path over raw HTTP when the plugin is installed:
   - `membox_status`
   - `membox_sync`
   - `membox_setup_start`
   - `membox_setup_poll`
   - `membox_setup_finish`
   - `membox_unlock`
   - `membox_unlock_secret_enable`
   - `membox_unlock_secret_disable`
   - `membox_pull`
   - `membox_restore`
   - `membox_grants_approve_pending`
5. Treat local memory files as the source of truth. By default, only sync `MEMORY.md` and `memory/YYYY-MM-DD.md`.
6. Never send plaintext memory, passphrases, `URK`, `AMK`, recovery codes, or decrypted recovery bundles to the server or the model.
7. On each memory change, sync only the changed file object instead of re-uploading the whole workspace.
8. Restore is a two-step operation: recover decryption capability first, then pull encrypted object changes and write the resulting files back locally.
9. For tool-driven setup, keep passphrases and recovery codes in local private files and use the OpenClaw plugin tools to read them from disk instead of pasting them inline.
10. Browser identity confirmation is required for third-party login, but it is not the only user-controlled boundary. The agent must not invent a vault passphrase, silently store recovery material, or enable managed unlock without explicit user consent.
11. `membox_sync`, `membox_pull`, and `membox_grants_approve_pending` require the vault to already be unlocked or explicitly opted into managed unlock. Browser authorization alone is not enough for unattended memory operations.
12. On Unix-like systems, keep the secret directory private (for example `chmod 700 .membox-secrets`) and secret-bearing files private (for example `chmod 600 .membox-secrets/*`), because the plugin rejects group- or world-readable secret files.
13. Distinguish clearly between inferred state, planned actions, executed actions, and verified state. Do not claim the plugin or skill is installed, the environment is ready, the account is paired, or the latest version is present unless the current run actually checked and confirmed it.
14. Never ask the user to paste a vault passphrase, recovery code, or recovery bundle into the chat transcript. If a secret must exist locally, instruct the user to place it in a private local file, or create that file locally only if the current runtime has file-write capability and the user explicitly opted in.

## Default Service Target

- Default web origin: `https://membox.cloud`
- Default API base: `https://membox.cloud/api/v1`
- Advanced users may override the service base explicitly for self-hosted deployments.

## Core Behavior

### 1. Login and Pairing

- Prefer the plugin Device Code flow for agent-driven setup:
  - call `membox_setup_start`
  - send `verification_uri_complete` back to IM as a clickable link
  - user opens the link on phone or another trusted browser
  - if the browser already has a valid Membox session, device authorization may complete automatically
  - otherwise the user completes GitHub, Google, or email login there
  - poll `membox_setup_poll` until it returns `authorized`
  - finish locally with `membox_setup_finish`
- If the plugin is not yet installed, install it first and only fall back to raw HTTP for debugging or low-level verification.
- Before telling the user that installation, readiness, or pairing is complete, verify it with actual command or tool results in the current run.
- If the plugin or skill was just installed and the tool registry still does not show `membox_*` tools, continue in a fresh OpenClaw session or next run.
- If the user is already in a browser login flow, continue from the existing web session and confirm the pending device instead of starting a second login.
- On headless or VPS machines, do not pretend the login can be completed locally. Tell the user to open the full verification URL on any trusted browser.
- For first-device setup, require a local `passphrase_file` and `recovery_code_output_file`. Keep both machine-local and out of the model transcript.
- Prefer a private local directory such as `.membox-secrets/` for those paths.
- If the user wants help generating a passphrase, generate it into a local private file only after explicit consent, or ask the user to create the file themselves. Do not reveal the generated passphrase in chat unless the user explicitly asks to see it.

### 2. Change-Triggered Sync

Whenever local memory changes:

- detect which core memory file changed
- encrypt and package only that file locally
- call the Membox sync commit API for that object
- update the local sync cursor or state after a successful commit

If the local file was deleted intentionally, write a tombstone through the delete API instead of silently ignoring the missing file.

If the vault is locked:

- use `membox_unlock` with a local `passphrase_file`
- or require prior explicit opt-in to managed unlock
- do not claim that browser login already unlocked the vault

### 3. Daily Scheduled Check

If the user wants unattended protection, the skill may install a local scheduled task that:

- runs once per day
- checks whether new local memory changes exist
- refreshes the access token if needed
- uploads pending file changes
- optionally checks remote cursor drift and reports if a pull preview is needed

Do not install an unattended schedule by default unless the machine already has an explicit non-interactive unlock path, such as managed unlock.

### 4. Restore

If the user wants to restore memory to a machine:

- log in first
- recover access to encrypted key material through either device grant approval or recovery bundle download
- query remote sync status and changes
- download, decrypt, and materialize the corresponding memory files locally
- never overwrite `MEMORY.md` silently; use preview and conflict-safe writes

If restore relies on a trusted-device grant, the already trusted device must be unlocked before it can approve the new device.

## What This Skill Does Not Do

- It does not replace OpenClaw's local memory backend.
- It does not use the web app to handle plaintext memory.
- It does not assume that login alone is enough to recover data in a zero-knowledge setup.
- It does not assume that browser authorization automatically unlocks future sync, pull, or grant operations.
- It does not sync derived SQLite, QMD caches, or session-memory indexes by default.
- It does not treat an unverified guess as an installed, ready, or up-to-date environment.
