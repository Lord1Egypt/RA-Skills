---
name: microsoft-365-graph-openclaw
description: Microsoft 365 Graph for OpenClaw with webhook-based wake signals. Reduce recurring LLM cost from inbox polling while managing Outlook mail, calendar, OneDrive, and contacts via Microsoft Graph.
version: 0.2.2
license: MIT
homepage: https://github.com/draeden79/microsoft-365-graph-openclaw
repository: https://github.com/draeden79/microsoft-365-graph-openclaw
metadata: {"openclaw":{"homepage":"https://github.com/draeden79/microsoft-365-graph-openclaw","os":["linux","darwin","win32"],"requires":{"bins":["python3","bash","curl"]}}}
security:
  summary: Push-first Graph integration with explicit hook token auth and clientState validation.
  notes:
    - Do not commit state/graph_auth.json or token-bearing logs.
    - Keep hooks token and Graph clientState in protected env storage.
    - Prefer /hooks/wake default to avoid unnecessary isolated agent runs.
---

# Microsoft 365 Graph for OpenClaw Skill

## 1. Quick prerequisites
1. Python 3 with `requests` installed.
2. Default auth values:
   - Client ID (personal-account default): `952d1b34-682e-48ce-9c54-bac5a96cbd42`
   - Tenant (personal-account default): `consumers`
   - Default scopes: `Mail.ReadWrite Mail.Send Calendars.ReadWrite Files.ReadWrite.All Contacts.ReadWrite offline_access`
   - For work/school accounts, use `--tenant-id organizations` (or tenant GUID) and a tenant-approved `--client-id`.
   - The public default client ID is for quick testing. For production, prefer your own App Registration.
3. Tokens are stored in `state/graph_auth.json` (ignored by git).
4. Push-mode runtime values (service-level):
   - These values are loaded by systemd services from `/etc/default/graph-mail-webhook` (usually written by setup scripts).
   - `OPENCLAW_HOOK_URL` (required)
   - `OPENCLAW_HOOK_TOKEN` (required)
   - `GRAPH_WEBHOOK_CLIENT_STATE` (required; auto-generated in minimal e2e setup when omitted)
   - `OPENCLAW_SESSION_KEY` (optional; default `hook:graph-mail`)

Permission profiles (least privilege by use case) are documented in `docs/permission-profiles.md`.

## 2. Assisted OAuth flow (Device Code)
1. Run:
   ```bash
   python scripts/graph_auth.py device-login \
     --client-id 952d1b34-682e-48ce-9c54-bac5a96cbd42 \
     --tenant-id consumers
   ```
2. The script prints a **URL** and **device code**.
3. Open `https://microsoft.com/devicelogin`, enter the code, and approve with the target account.
4. Check and manage auth state:
   - `python scripts/graph_auth.py status`  
   - `python scripts/graph_auth.py refresh`  
   - `python scripts/graph_auth.py clear`
5. Other scripts call `utils.get_access_token()`, which refreshes tokens automatically when needed.
6. Scope override is disabled in `graph_auth.py`; the skill always uses `DEFAULT_SCOPES`.

Detailed reference: [`references/auth.md`](references/auth.md).

## 3. Email operations
- **List/filter**: `python scripts/mail_fetch.py --folder Inbox --top 20 --unread`
- **Fetch specific message**: `... --id <messageId> --include-body --mark-read`
- **Move message**: add `--move-to <folderId>` to the command above.
- **Send email** (`saveToSentItems` enabled by default):
  ```bash
  python scripts/mail_send.py \
    --to user@example.com \
    --subject "Update" \
    --body-file replies/thais.html --html \
    --cc teammate@example.com \
    --attachment docs/proposal.pdf
  ```
- Use `--no-save-copy` only when you intentionally do not want Sent Items storage.

More examples and filters: [`references/mail.md`](references/mail.md).

## 4. Calendar operations
- **List custom date window**:
  ```bash
  python scripts/calendar_sync.py list \
    --start 2026-03-03T00:00Z --end 2026-03-05T23:59Z --top 50
  ```
- **Create Teams or in-person event**: use `create`; add `--online` for Teams link.
- For personal Microsoft accounts (`tenant=consumers`), Teams meeting provisioning via Graph might not return a join URL; create the Teams meeting in Outlook/Teams first and add the resulting link to the event body when needed.
- **Update/cancel** events by `event_id` returned in JSON output.

Full examples: [`references/calendar.md`](references/calendar.md).

## 5. OneDrive / Files
- **List folders/files**: `python scripts/drive_ops.py list --path /`
- **Upload**: `... upload --local notes/briefing.docx --remote /Clients/briefing.docx`
- **Download**: `... download --remote /Clients/briefing.docx --local /tmp/briefing.docx`
- **Move / share links**: use `move` and `share` subcommands.
- The script resolves localized/special-folder aliases (for example `Documents` and `Documentos`).

More details: [`references/drive.md`](references/drive.md).

## 6. Contacts
- **List/search**: `python scripts/contacts_ops.py list --top 20`
- **Create**: `... create --given-name Jane --surname Doe --email jane.doe@example.com`
- **Update/Delete**: `... update <contactId> ...` / `... delete <contactId>`
- Contacts are part of the default scope set and supported as a first-class workflow.

More details: [`references/contacts.md`](references/contacts.md).

## 7. Mail push mode (Webhook Adapter)
- **Adapter server** (Graph handshake + `clientState` validation + enqueue):
  ```bash
  python scripts/mail_webhook_adapter.py serve \
    --host 0.0.0.0 --port 8789 --path /graph/mail \
    --client-state "$GRAPH_WEBHOOK_CLIENT_STATE"
  ```
- **Subscription lifecycle** (`create/status/renew/delete/list`):
  ```bash
  python scripts/mail_subscriptions.py create \
    --notification-url "https://graph-hook.example.com/graph/mail" \
    --client-state "$GRAPH_WEBHOOK_CLIENT_STATE" \
    --minutes 4200
  ```
  - Default resource is `me/messages` (recommended for better delivery coverage). Override with `--resource` only for advanced/scoped scenarios.
- **Async worker** (dedupe + default wake signal to OpenClaw `/hooks/wake`):
  ```bash
  python scripts/mail_webhook_worker.py loop \
    --session-key "$OPENCLAW_SESSION_KEY" \
    --hook-url "$OPENCLAW_HOOK_URL" \
    --hook-token "$OPENCLAW_HOOK_TOKEN"
  ```
  - Default mode is `wake` (`/hooks/wake`, `mode=now`). Use `--hook-action agent` only when you explicitly need per-message rich payload delivery.
- Worker queue files:
  - `state/mail_webhook_queue.jsonl`
  - `state/mail_webhook_dedupe.json`
- **Automated EC2 bootstrap** (Caddy + systemd + renew timer):
  ```bash
  sudo bash scripts/setup_mail_webhook_ec2.sh \
    --domain graphhook.example.com \
    --hook-url http://127.0.0.1:18789/hooks/wake \
    --hook-token "<OPENCLAW_HOOK_TOKEN>" \
    --session-key "hook:graph-mail" \
    --client-state "<GRAPH_WEBHOOK_CLIENT_STATE>" \
    --repo-root "$(pwd)"
  ```
  - Use `--dry-run` to preview all privileged writes and service actions before applying changes.
- **One-command setup (steps 2..6)**:
  ```bash
  sudo bash scripts/run_mail_webhook_e2e_setup.sh \
    --domain graphhook.example.com \
    --hook-token "<OPENCLAW_HOOK_TOKEN>" \
    --hook-url "http://127.0.0.1:18789/hooks/wake" \
    --session-key "hook:graph-mail" \
    --test-email "tar.alitar@outlook.com"
  ```
  - Use `--dry-run` for a no-mutation execution plan (no `/etc` writes, no `systemctl`, no subscription create, no email send).
  - Output ends with `READY_FOR_PUSH: YES` when setup is fully validated.
- **Include OpenClaw hook config in automation**:
  ```bash
  sudo bash scripts/run_mail_webhook_e2e_setup.sh \
    --domain graphhook.example.com \
    --hook-token "<OPENCLAW_HOOK_TOKEN>" \
    --configure-openclaw-hooks \
    --openclaw-config "/home/ubuntu/.openclaw/openclaw.json" \
    --openclaw-service-name "auto" \
    --openclaw-hooks-path "/hooks" \
    --openclaw-allow-request-session-key true \
    --test-email "tar.alitar@outlook.com"
  ```
- **Minimal-input smoke tests**:
  ```bash
  sudo bash scripts/run_mail_webhook_smoke_tests.sh \
    --domain graphhook.example.com \
    --create-subscription \
    --test-email tar.alitar@outlook.com
  ```
  - Output ends with `READINESS VERDICT: READY_FOR_PUSH` only after all critical checks pass.
- Setup and runbook: [`references/mail_webhook_adapter.md`](references/mail_webhook_adapter.md).

## 8. Privileged operations boundary

The core Graph scripts are unprivileged (`graph_auth.py`, `mail_fetch.py`, `mail_send.py`, `calendar_sync.py`, `drive_ops.py`, `contacts_ops.py`).

The setup scripts below are privileged and should be manually reviewed before execution:
- `scripts/setup_mail_webhook_ec2.sh`
- `scripts/run_mail_webhook_e2e_setup.sh`

When run without `--dry-run`, they can:
- Write `/etc/default/graph-mail-webhook`
- Write `/etc/caddy/Caddyfile`
- Write `/etc/systemd/system/*.service` and `*.timer`
- Enable/restart services via `systemctl`
- Optionally patch OpenClaw config and restart OpenClaw services

Recommended safety sequence:
1. Run with `--dry-run`
2. Review emitted actions and target files
3. Run on a non-production host first
4. Apply to production only after approval

## 9. Logging and conventions
- Each script appends one JSON line to `state/graph_ops.log` with timestamp, action, and key parameters.
- Tokens and logs must never be committed.
- Commands assume execution from the repository root. Adjust paths if running elsewhere.

## 10. Troubleshooting
| Symptom | Action |
| --- | --- |
| 401/invalid_grant | Run `graph_auth.py refresh`; if it fails, run `clear` and repeat device login. |
| 403/AccessDenied | Missing scope or licensing/policy issue. Re-run device login with required scope(s). |
| 429/Throttled | Scripts do basic retry; wait a few seconds and retry. |
| `requests.exceptions.SSLError` | Verify local system date/time and TLS trust chain. |

This skill provides OAuth-driven workflows for email, calendar, files, contacts, and push-based mail automation via Microsoft Graph.
