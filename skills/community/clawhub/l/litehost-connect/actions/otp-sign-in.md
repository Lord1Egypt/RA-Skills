# Sign In (email code)

Signs the user in without a browser and saves an API key for every later session. Creates a
free account (with a 7-day Pro trial) if the email is new.

## Before you start

- Run `scripts/litehost.sh session`. If it succeeds, the user is already signed in: **stop here**.
- Only sign in when the user wants you to manage their projects. To just publish something, use
  `actions/temp-project.md` — it needs no sign-in.
- Ask for the user's email if you don't know it.

---

## Step 1 — Send the code (once)

```bash
scripts/litehost.sh request-code you@example.com
```

Equivalent curl:

```bash
curl -X POST https://connect.litehost.io/v1/auth/otp/request \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com"}'
```

Response:

```json
{
  "status": "success",
  "nextStep": "Ask the user for the 6-digit code ... Do not call this endpoint again while waiting for the user.",
  "data": { "sent": true, "expiresAt": "2026-09-28T12:10:00.000Z", "resendAvailableInSeconds": 60 }
}
```

If a code is already open (for example you called this twice), nothing is sent and you get
`"codeAlreadySent": true`. That is fine: the code in the user's inbox is still valid.

Then tell the user: **"I sent a 6-digit code to {email}. Please paste it here."** and wait.

Do **not** call request-code again while you wait. If the user says no email arrived:
1. Ask them to check spam and search for "Litehost sign-in code".
2. If it is still missing, resend the same code (allowed once a minute):
   `scripts/litehost.sh request-code you@example.com --resend`

---

## Step 2 — Verify and save the key

```bash
scripts/litehost.sh verify you@example.com 482931
```

On success the helper saves the key to `~/.config/litehost/credentials.json` (permissions 600)
and prints it masked:

```json
{"status":"success","email":"you@example.com","apiKey":"lh_live_a1b2…9f0e","savedTo":"/home/you/.config/litehost/credentials.json","expiresAt":"2026-12-27T12:00:00.000Z","note":"Key saved; it renews while in use. Do not sign in again."}
```

Tell the user: "You're signed in as {email}. I saved the key in {savedTo}, so you won't need a code
next time."

### Without the helper

```bash
curl -X POST https://connect.litehost.io/v1/auth/otp/verify \
  -H "Content-Type: application/json" \
  -d '{"email":"you@example.com","code":"482931"}'
```

Take `data.apiKey` and store it where it survives this session, in this order of preference:
1. `~/.config/litehost/credentials.json` as `{"apiKey":"lh_live_…","email":"…"}` with `chmod 600`
2. The agent's secret store, as `LITEHOST_API_KEY`
3. No storage at all: ask the user to keep the key and paste it next time

Never rely on `export` alone: the next command usually runs in a new shell without it.
Never repeat the full key back to the user once saved.

---

## Errors

| Code | Meaning | Do this |
|---|---|---|
| `OTP_INVALID` | Wrong code (typo, old email). `attemptsLeft` says how many tries remain. | Ask the user to re-check the latest Litehost email. **Do not request a new code** — the current one is still valid. |
| `OTP_EXPIRED` | No open code: it expired (10 min) or was used. | Request a new code once (Step 1), then ask the user for it. |
| `OTP_TOO_MANY_ATTEMPTS` | 5 wrong codes; the code was cancelled. | Request a new code once and ask the user to copy it carefully. |
| `RATE_LIMITED` | Too many emails (5 per address per hour). | If a code was already sent, verify that one. Otherwise wait `retryAfterSeconds`; meanwhile you can publish with `actions/temp-project.md`. |
| `INVALID_REQUEST` | Email or code malformed. | Fix the input (6 digits, no spaces) and retry. |
| `SERVER_ERROR` | Account setup failed. | Wait a minute, then request a new code once. |

## Key lifetime

Keys from this flow renew automatically every time they are used, and expire only after 90 days
without use. If a call ever returns `API_KEY_EXPIRED` or `API_KEY_INVALID`, run
`scripts/litehost.sh forget` and sign in again once.
