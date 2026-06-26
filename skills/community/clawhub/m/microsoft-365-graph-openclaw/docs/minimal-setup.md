# Minimal Setup: Mail Webhook in 6 Steps

This guide uses the minimum required parameters and assumes you installed the skill via ClawHub. The setup command generates `clientState` automatically and creates the subscription. You do not need to run the adapter manually to copy values, and you do not need to pass `--session-key`.

## Prerequisites

- DNS: your domain (for example, `graphhook.example.com`) points to the public IP of your host (EC2 or equivalent).
- Ports `80` and `443` are open in your firewall/security group.
- OpenClaw is running locally (for example on `127.0.0.1:18789`).

## Steps

### 0. Install the skill with ClawHub

```bash
clawhub install microsoft-365-graph-openclaw
```

### 1. Prepare

```bash
cd /path/to/skills/microsoft-365-graph-openclaw
export REPO_ROOT="$(pwd)"
```

### 2. Authenticate

Personal account (Outlook/Hotmail):

```bash
python3 scripts/graph_auth.py device-login \
  --client-id 952d1b34-682e-48ce-9c54-bac5a96cbd42 \
  --tenant-id consumers
```

Work/school account:

```bash
python3 scripts/graph_auth.py device-login \
  --client-id 952d1b34-682e-48ce-9c54-bac5a96cbd42 \
  --tenant-id organizations
```

Open the URL shown by the script, paste the device code, and authorize.

### 3. Configure OpenClaw hooks

Update `openclaw.json` (typically `~/.openclaw/openclaw.json`) and restart OpenClaw:

```json
"hooks": {
  "enabled": true,
  "token": "<OPENCLAW_HOOK_TOKEN>"
}
```

Use the same token value in step 4 (`--hook-token`). Full details: [setup-openclaw-hooks.md](setup-openclaw-hooks.md).

### 4. Run one setup command

This script installs Caddy and systemd units (adapter/worker/timer), creates the Graph subscription, and persists runtime values.

```bash
sudo bash scripts/run_mail_webhook_e2e_setup.sh \
  --domain graphhook.example.com \
  --hook-token "<OPENCLAW_HOOK_TOKEN>" \
  --test-email "your-email@example.com" \
  --repo-root "$REPO_ROOT"
```

Replace `graphhook.example.com` and `<OPENCLAW_HOOK_TOKEN>` with your real values.
Run steps 5 and 6 with `sudo` because the scripts read `/etc/default/graph-mail-webhook` (root-owned by default).

### 5. Run diagnostics

```bash
sudo bash scripts/diagnose_mail_webhook_e2e.sh \
  --domain graphhook.example.com \
  --repo-root "$REPO_ROOT"
```

Resolve any `FAIL` result before proceeding.

### 6. Run smoke test

```bash
sudo bash scripts/run_mail_webhook_smoke_tests.sh \
  --domain graphhook.example.com \
  --create-subscription \
  --test-email "your-email@example.com"
```

Confirm the final verdict is `READY_FOR_PUSH`.

## Summary

| Step | Action |
|------|--------|
| 0 | `clawhub install microsoft-365-graph-openclaw` |
| 1 | `cd` into skill folder and `export REPO_ROOT` |
| 2 | Device login (`consumers` or `organizations`) |
| 3 | Configure `hooks.token` in `openclaw.json` and restart OpenClaw |
| 4 | Run `run_mail_webhook_e2e_setup.sh` with `--domain`, `--hook-token`, `--test-email` |
| 5 | Run diagnostics |
| 6 | Run smoke test |
