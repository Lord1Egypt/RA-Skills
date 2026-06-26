# Troubleshooting

## No real webhook deliveries

Symptoms:
- adapter logs only show `validationToken` requests
- queue remains empty

Actions:
1) Verify active subscription resource (`me/messages` recommended).
2) Verify notification URL is public HTTPS and reachable.
3) Check adapter service and reverse proxy status.
4) Run `sudo bash scripts/diagnose_mail_webhook_e2e.sh --domain <your-domain> --repo-root "$(pwd)"` for full pipeline checks.

## Subscription has `clientState: null`

Cause:
- subscription created without resolved env var or with wrong shell context

Actions:
1) Load env from `/etc/default/graph-mail-webhook` in the same shell.
2) Recreate subscription with explicit `--client-state`.
3) Confirm via `mail_subscriptions.py status --id <id>`.

## OpenClaw hook returns 400/401

Actions:
0) Confirm running services load values from `/etc/default/graph-mail-webhook` (or source it in the same shell before manual tests).
1) Verify `OPENCLAW_HOOK_URL` points to `/hooks/wake`.
2) Verify `OPENCLAW_HOOK_TOKEN` and header auth.
3) Check OpenClaw `hooks.enabled=true` and `hooks.token`.

## Worker loops with `Queue is empty`

If expected:
- there may be no new Graph deliveries

If unexpected:
1) confirm adapter logs show real `POST /graph/mail ... 202`
2) confirm queue file path matches service config
3) run diagnostics and inspect `graph_ops.log`

## TLS / domain issues

Actions:
1) confirm DNS points to the expected host
2) confirm ports `80/443` are open
3) confirm reverse proxy obtains valid cert
4) validate endpoint with local and external HTTPS checks
