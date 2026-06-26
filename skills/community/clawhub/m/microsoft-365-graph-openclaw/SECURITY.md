# Security Policy

## Security posture

This project is designed for self-hosted OpenClaw deployments with explicit, auditable webhook boundaries.

Key controls:
- Dedicated OpenClaw hook token for webhook auth
- Graph `clientState` validation for notification integrity
- Local queue + dedupe before agent wake-up
- No dependency on `curl | bash` installers in project scripts

## Supported release line

- Latest `main` branch and latest tagged release are considered supported for security fixes.

## Secrets and sensitive data

Treat the following as secrets:
- `OPENCLAW_HOOK_TOKEN`
- `GRAPH_WEBHOOK_CLIENT_STATE`
- OAuth tokens in `state/graph_auth.json`
- Any raw `Authorization: Bearer ...` values

Not secrets:
- Microsoft Graph `client_id` (application ID)
- Subscription IDs
- Public webhook URL hostname

## Recommended minimum permissions

Use least privilege by profile:
- Mail-only: `Mail.ReadWrite Mail.Send offline_access`
- Calendar-only: `Calendars.ReadWrite offline_access`
- Contacts-only: `Contacts.ReadWrite offline_access`
- Full suite: add only the scopes you actually use

Avoid adding extra scopes unless required for a concrete feature.

## Credential storage and rotation

- Keep env secrets in host-managed files (for example `/etc/default/graph-mail-webhook`) with restricted permissions.
- Never commit token-bearing files under `state/`.
- Rotate immediately if logs, shell history, or screenshots may have exposed a token.

Revocation checklist:
1) Rotate OpenClaw hook token and restart gateway.
2) Replace `GRAPH_WEBHOOK_CLIENT_STATE` and recreate Graph subscriptions.
3) Revoke affected OAuth grants in Microsoft account/App Registration.
4) Re-run setup + diagnostics to confirm healthy state.

## Hardening guidance

- Bind adapter to loopback when using a reverse proxy.
- Expose only HTTPS publicly.
- Keep OpenClaw webhook endpoint local/private when possible.
- Prefer `/hooks/wake` as default trigger and fetch message data only during real processing.
- Keep request session key override disabled unless strictly needed.

## Reporting vulnerabilities

If you find a security issue:
- Do not open a public issue with exploit details.
- Share a private report with:
  - impact summary
  - reproduction steps
  - affected commit/tag
  - suggested mitigation (if available)

If no private contact channel is available yet, open a minimal public issue requesting a secure contact route without disclosing exploit details.
