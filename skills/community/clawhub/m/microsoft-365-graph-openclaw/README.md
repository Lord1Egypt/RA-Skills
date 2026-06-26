# Microsoft 365 Graph for OpenClaw

Microsoft 365 Graph for OpenClaw with webhook-based wake signals.

Reduce recurring LLM cost from inbox polling while managing Outlook mail, calendar, OneDrive, and contacts via Microsoft Graph.
This repository provides a webhook-driven Graph skill that wakes OpenClaw only when work actually happens in self-hosted deployments.

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Release](https://img.shields.io/badge/release-v0.2.2-blue.svg)
![CI](https://img.shields.io/badge/ci-github_actions-informational.svg)

## Why this exists

Polling-based inbox checks are expensive in practice:
- A cron/heartbeat loop keeps waking agents even when nothing changed.
- Those recurring turns consume tokens and increase operating cost.
- They also increase noise in operational logs and incident triage.

Microsoft Graph change notifications flip the model:
- Graph pushes an event when a message changes.
- The skill validates and deduplicates events.
- OpenClaw receives a wake signal only when there is new work.

Core message: replace recurring inbox polling with event-driven notifications.

## Cost model

Assume one lightweight inbox-check wake-up uses about `2,000` input tokens and `400` output tokens.

Using GPT-5.3-Codex pricing (`$1.75 / 1M` input, `$14.00 / 1M` output), each wake-up costs about **$0.0091**. 

- **2-minute polling** = `720` wake-ups/day = about **$6.55/day** = about **$196.56/month**
- **Push mode with 5 real events/day** = `5` wake-ups/day = about **$0.05/day** = about **$1.37/month**

In this example, push reduces recurring wake-up spend by about **99%**.

These numbers are illustrative. Push does not remove the cost of processing real email work — it mainly removes the cost of waking the agent repeatedly just to check whether anything changed.

## What is included

Skill:
- `microsoft-365-graph-openclaw`

Capabilities:
- OAuth device-code auth with refresh handling
- Mail, calendar, drive, and contacts automation
- Graph webhook adapter + worker queue + dedupe
- OpenClaw wake integration via `/hooks/wake`
- EC2-oriented setup, smoke testing, and end-to-end diagnostics

## Architecture at a glance

`Microsoft Graph -> webhook endpoint -> queue -> dedupe worker -> /hooks/wake -> OpenClaw`

See full architecture and flow in `docs/architecture.md`.

## Public HTTPS webhook URL prerequisite

Graph can deliver notifications only to a public HTTPS endpoint. Conceptual setup steps:

1) Own a domain or subdomain for webhook traffic (for example `graphhook.yourdomain.com`).
2) Create DNS record (`A`/`AAAA`) pointing that hostname to your public server IP.
3) Open inbound ports `80` and `443` in cloud firewall/security group.
4) Configure TLS termination (for example Caddy or Nginx) with a valid certificate.
5) Route `https://<your-host>/graph/mail` to `mail_webhook_adapter.py` in your host.
6) Validate externally:
   - `GET https://<your-host>/graph/mail?validationToken=test` returns `200` + token echo.
   - Graph subscription creation succeeds with `notificationUrl` set to this endpoint.

After this prerequisite is in place, use the setup scripts in `scripts/` to automate the remaining pipeline.

## Minimal setup (6 steps)

Use this path for a low-friction installation (including ClawHub installs). It uses the fewest parameters, auto-generates `clientState`, and creates the Graph subscription automatically.

0) Install from ClawHub (if not already installed):
```bash
clawhub install microsoft-365-graph-openclaw
```

1) Prepare:
```bash
cd /path/to/skills/microsoft-365-graph-openclaw
export REPO_ROOT="$(pwd)"
```

2) Authenticate (choose one):
```bash
# Personal account (Outlook/Hotmail)
python3 scripts/graph_auth.py device-login \
  --client-id 952d1b34-682e-48ce-9c54-bac5a96cbd42 \
  --tenant-id consumers

# Work/school account
python3 scripts/graph_auth.py device-login \
  --client-id 952d1b34-682e-48ce-9c54-bac5a96cbd42 \
  --tenant-id organizations
```

3) Configure OpenClaw hooks in `openclaw.json` and restart OpenClaw:
```json
"hooks": {
  "enabled": true,
  "token": "<OPENCLAW_HOOK_TOKEN>",
  "defaultSessionKey": "hook:ingress",
  "allowRequestSessionKey": false,
  "allowedSessionKeyPrefixes": ["hook:"]
}
```
- Use the same token value in setup step 4.
- Full hook guidance: `docs/setup-openclaw-hooks.md`.

4) Run one setup command:
```bash
sudo bash scripts/run_mail_webhook_e2e_setup.sh \
  --domain graphhook.example.com \
  --hook-token "<OPENCLAW_HOOK_TOKEN>" \
  --test-email "your-email@example.com" \
  --repo-root "$REPO_ROOT"
```

5) Run diagnostics:
```bash
sudo bash scripts/diagnose_mail_webhook_e2e.sh \
  --domain graphhook.example.com \
  --repo-root "$REPO_ROOT"
```

6) Run smoke test:
```bash
sudo bash scripts/run_mail_webhook_smoke_tests.sh \
  --domain graphhook.example.com \
  --create-subscription \
  --test-email "your-email@example.com"
```

Note: steps 5 and 6 use `sudo` because they load `/etc/default/graph-mail-webhook`, which is root-owned by default.

Expected final verdict: `READY_FOR_PUSH`.

Detailed walkthrough: `docs/minimal-setup.md`.
If setup checks fail, see `docs/troubleshooting.md` and `docs/faq.md`.

## Authentication for your use case

- Personal Outlook/Hotmail: use `--tenant-id consumers` with the default client ID.
- Work/school Entra account: use `--tenant-id organizations` (or tenant GUID).
- Production environments: use your own app registration and consent model. See `docs/app-registration.md`.
- Scope sets by use case (mail-only, calendar-only, full suite): `docs/permission-profiles.md`.

## Security and auditability

- Token-bearing files stay in `state/` and must never be committed.
- Webhook authentication requires dedicated hook token headers.
- Graph webhook integrity uses `GRAPH_WEBHOOK_CLIENT_STATE`.
- Push-mode runtime uses service-level values from `/etc/default/graph-mail-webhook` (written by setup scripts): `OPENCLAW_HOOK_URL` (required), `OPENCLAW_HOOK_TOKEN` (required), `GRAPH_WEBHOOK_CLIENT_STATE` (required), and `OPENCLAW_SESSION_KEY` (optional; default `hook:graph-mail`).
- The project is self-hosted and production-oriented, with explicit setup and diagnostics.
- See `SECURITY.md` for threat model and credential revocation guidance.
- API command references by workload:
  - Mail: `references/mail.md`
  - Calendar: `references/calendar.md`
  - Drive: `references/drive.md`
  - Contacts: `references/contacts.md`
  - Webhook adapter: `references/mail_webhook_adapter.md`

## Privileged operations boundary

Core Graph operations are unprivileged Python scripts.

Privileged automation is limited to:
- `scripts/setup_mail_webhook_ec2.sh`
- `scripts/run_mail_webhook_e2e_setup.sh`

Without `--dry-run`, these can write under `/etc`, create/enable systemd units, and optionally patch OpenClaw config + restart services. Review script output with `--dry-run` before applying changes on production hosts.
