# First-run web mode

## Purpose

Enable the public skill to start a minimal web UI even when `auth-profiles.json` does not exist yet.

## Bootstrap command

```bash
export OPENAI_AUTH_SWITCHER_PUBLIC_STATE_DIR=/tmp/openai-auth-switcher-public-runtime
python3 skills/openai-auth-switcher-public/scripts/install_web_app.py
```

## Expected output

The installer should print:

- local URL
- selected port
- generated username
- generated password
- SSH tunnel command
- service mode / log path

## Intended product behavior

If auth is missing, the page should enter onboarding mode instead of failing hard.

The current preview also protects the page with generated HTTP Basic Auth credentials and exposes:

- `GET /`
- `GET /api/state`
- `POST /api/import-auth`

The preview page now includes:

- onboarding / managed mode visual separation
- install summary
- SSH tunnel guidance
- inline auth import form for first-run takeover
- automatic refresh hint when auth becomes ready after import
- top-level status cards for mode / service readiness / next action
- additional install summary cards for local URL, username, and state directory
- systemd runtime summary (active state / sub state / log path) for easier diagnosis on first run
