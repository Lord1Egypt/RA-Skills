# Membox Workflows

## Scope

This skill is for the OpenClaw memory sync layer, not for replacing local memory search.

Default local facts to sync:

- `MEMORY.md`
- `memory/YYYY-MM-DD.md`

Do not include derived caches or indexes by default:

- `~/.openclaw/memory/<agentId>.sqlite`
- QMD sidecars
- downloaded models
- session transcript indexes

## Workflow 1: First-Time Setup

Preferred OpenClaw tool path:

0. If the Membox plugin is missing, install `@membox-cloud/membox` first.
0.5. If the plugin or skill was installed during the current conversation and `membox_*` tools still are not available, start a new OpenClaw session or next run.
0.6. Before saying "installed", "ready", "paired", or "latest", verify that state with actual command or tool output from the current run. If you have not checked yet, say that you have not checked yet.
1. Call `membox_setup_start`.
2. Send the returned `verification_uri_complete` back to the user as a clickable link.
3. If the browser is already signed in to Membox, authorization may finish automatically. Otherwise the user must complete GitHub, Google, or email login first.
4. On headless or VPS machines, instruct the user to open that full URL on another trusted browser or phone.
5. Poll with `membox_setup_poll` until the device becomes authorized.
6. Prepare local private files for:
   - the vault passphrase
   - the recovery code output path
   - on Unix-like systems, prefer a private directory such as `.membox-secrets/`, `chmod 700` the directory, and `chmod 600` secret-bearing files
7. Finish setup with `membox_setup_finish`.
8. If the user explicitly opts in, enable managed unlock at setup time or later with `membox_unlock_secret_enable`.
9. Verify the account and device state with `membox_status`, `GET /devices`, or `GET /sync/status`.

Important boundary:

- browser authorization does not unlock the vault for later memory operations
- if `membox_sync`, `membox_pull`, or `membox_grants_approve_pending` report a locked vault, use `membox_unlock` with a local `passphrase_file` or require prior managed-unlock opt-in
- do not ask the user to paste the passphrase or recovery code into the model transcript
- do not offer to "hold" the passphrase in chat; keep it in a local private file only
- if the user wants a generated passphrase, create it locally only after consent, and do not reveal it in chat unless explicitly requested

Equivalent lower-level HTTP flow:

1. Start with login. No setup is complete until the user is authenticated.
2. Create a device authorization request with `POST /device/start`.
3. Ask the user to open the returned `verification_uri_complete`.
4. Poll `GET /device/poll/{device_code}` until `access_token`, `refresh_token`, and `device_id` are returned.
5. Store the session on the local machine only.
6. Build the initial encrypted file objects locally and upload them through the sync commit API.

## Workflow 2: Incremental Sync After a Memory Change

Trigger this workflow every time one of the default memory files changes.

1. Identify the changed logical path.
2. Map that path to a stable `object_id`.
3. Re-encrypt and package the file locally.
4. Submit the new object version with `POST /sync/objects/commit`.
5. Record the newest cursor from the sync response or follow-up `GET /sync/status`.

Operational rule:

- Sync the changed file object only.
- Do not re-upload unrelated files.
- If a file was removed deliberately, call `DELETE /sync/objects/{object_id}`.
- If the vault is locked, unlock it from a local `passphrase_file` or require explicit managed-unlock opt-in before attempting unattended sync.

## Workflow 3: Startup or Manual Pull

Use this when the device starts, when the user asks for `pull`, or when daily checks detect remote drift.

1. Log in or refresh tokens first.
2. Fetch `GET /sync/status`.
3. Compare the remote cursor with the last local cursor.
4. If remote is ahead, fetch `GET /sync/changes?cursor={cursor}`.
5. Download the referenced encrypted objects.
6. Decrypt locally and compute the preview locally.
7. Apply safe writes:
   - never silently overwrite `MEMORY.md`
   - prefer conflict copies when merge safety is unclear

If pull fails because the vault is locked:

- use `membox_unlock` with a local `passphrase_file`
- or stop and ask for explicit managed-unlock opt-in before scheduling unattended pulls

## Workflow 4: Daily Scheduled Upload Check

Recommended policy:

- run once every 24 hours
- check local file mtimes or a local change journal
- refresh the session if needed
- upload pending commits
- optionally run a remote status check

The scheduler should be local to the user's machine. This skill describes the behavior; the concrete mechanism can be `cron`, `launchd`, `systemd --user`, or another local scheduler that fits the environment.

Important boundary:

- a non-interactive scheduler cannot answer a passphrase prompt
- do not install unattended sync unless the machine already has an explicit local unlock path, such as managed unlock

## Workflow 5: Restore to a New or Reset Machine

Restore is never "download plaintext after login."

Correct order:

1. Log in first.
2. Recover decryption capability:
   - either request a device grant and wait for approval from a trusted device
   - or obtain the encrypted recovery bundle and recover locally with user-held recovery material
   - if using a trusted-device grant, the already trusted device must be unlocked before it can approve the request
3. Confirm the device is now trusted and has a valid session.
4. Call `GET /sync/status` and `GET /sync/changes`.
5. Download encrypted objects, decrypt locally, and reconstruct:
   - `MEMORY.md`
   - `memory/YYYY-MM-DD.md`
6. Use preview and conflict-safe writes before replacing existing local files.

Important constraint:

- Login identifies the user.
- Device grant or recovery material restores decryption capability.
- Those are separate layers and must not be collapsed in the skill.
- Do not claim the agent can complete third-party login or email inbox verification without the user's explicit participation.
