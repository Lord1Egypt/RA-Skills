# Scheduling and Restore Notes

## Daily Upload Schedule

Use a local scheduler, not a remote server-side job, because plaintext change detection belongs on the user's machine.

Minimum daily job behavior:

1. Check whether `MEMORY.md` or `memory/YYYY-MM-DD.md` changed since the last successful sync.
2. If the access token is stale, refresh it with `POST /auth/token/refresh`.
3. For each changed file:
   - encrypt locally
   - commit through `POST /sync/objects/commit`
4. If a file was deleted locally, call `DELETE /sync/objects/{object_id}`.
5. Run `GET /sync/status` after upload and store the latest cursor.

Non-interactive unlock requirement:

- Do not schedule unattended sync unless the machine already has an explicit local unlock path.
- A scheduler cannot answer an interactive vault passphrase prompt.
- For the plugin tool path, that usually means the user explicitly enabled managed unlock first.

Recommended behavior:

- report success and failure in a local log
- back off on transient server errors
- stop and require re-login on revoked or expired refresh tokens
- keep scheduling independent from interactive chat sessions

## Restore Through the Service Endpoint

The repository documents a service endpoint model rather than a single `/restore` route.

In practice, the skill should orchestrate restore through the configured Membox API base:

1. Authenticate first.
2. Recover key access through either:
   - trusted-device grant endpoints
   - recovery bundle download plus local recovery-material handling
3. Query `GET /sync/status`.
4. Read `GET /sync/changes?cursor={cursor}` until all needed objects are discovered.
5. Download the encrypted object blobs referenced by the manifests.
6. Decrypt locally and write the memory files back into the workspace.

This means "restore through the port" should be interpreted as "restore through the configured Membox API service endpoint," which defaults to `https://membox.cloud/api/v1`.

If restore depends on a trusted-device grant, the already trusted device must be unlocked before it can approve the new device.

## Conflict and Safety Policy

When restoring or pulling:

- never silently overwrite `MEMORY.md`
- prefer a preview before apply
- create conflict copies when a safe merge is not provable
- keep local wins, remote wins, and conflict copy as the initial policy set

Do not attempt broad Markdown auto-merge in the first version of the skill.
