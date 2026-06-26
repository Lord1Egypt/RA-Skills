---
name: leapcat-auth
description: Manage user authentication for Leapcat. Handles login, logout, session management, token refresh, re-authentication, and trade password operations via the leapcat CLI.
homepage: https://leapcat.ai
---

# LeapCat Authentication Skill

Manage user authentication for the leapcat. Handles login, logout, session management, token refresh, re-authentication, and trade password operations.

## Prerequisites

- Node.js 18+ is required (commands use `npx leapcat@0.1.1` which auto-downloads the CLI)
- A valid email address registered with LeapCat

## Commands

### auth login (non-interactive, two-step flow)

Step 1 — Send OTP to email:

```bash
npx leapcat@0.1.1 auth login --email <email> --send-only --json
```

**Response:**
```json
{ "otp_id": "<otp-id-string>" }
```

Step 2 — Verify OTP and complete login:

```bash
npx leapcat@0.1.1 auth login --email <email> --otp-id <otp-id> --otp-code <code> --json
```

**Parameters:**
- `--email <email>` — User email address (required)
- `--send-only` — Only send the OTP, do not attempt verification
- `--otp-id <id>` — OTP identifier returned from step 1
- `--otp-code <code>` — 6-digit code the user received via email
- `--json` — Output in JSON format (always use for agent consumption)

### auth logout

End the current session and clear stored credentials.

```bash
npx leapcat@0.1.1 auth logout --json
```

### auth status

Check if the user is currently authenticated and whether the token is still valid.

```bash
npx leapcat@0.1.1 auth status --json
```

### auth refresh

Refresh the current authentication token before it expires.

```bash
npx leapcat@0.1.1 auth refresh --json
```

### auth reauth

Perform a re-authentication to obtain an elevated session (e.g., for withdrawal operations that require a Turnkey session).

```bash
npx leapcat@0.1.1 auth reauth --json
```

### auth trade-password set

Set the trade password for the first time. Required before placing orders or subscribing to IPOs.

```bash
npx leapcat@0.1.1 auth trade-password set --json
```

### auth trade-password verify

Verify the trade password.

```bash
npx leapcat@0.1.1 auth trade-password verify --json
```

### auth trade-password reset

Reset a forgotten trade password.

```bash
npx leapcat@0.1.1 auth trade-password reset --json
```

### auth trade-password status

Check whether a trade password has been set.

```bash
npx leapcat@0.1.1 auth trade-password status --json
```

## Workflow

1. **Check auth status** — Run `auth status --json` to determine if the user is already logged in.
2. **Login if needed** — If not authenticated, execute the two-step login flow:
   - Send OTP with `--send-only`
   - Ask the user for the OTP code they received
   - Complete login with `--otp-id` and `--otp-code`
3. **Refresh when expired** — If a command returns a 401/token-expired error, run `auth refresh --json`. If refresh fails, re-run the full login flow.
4. **Re-auth for sensitive operations** — Before wallet withdrawals or other sensitive actions, run `auth reauth --json` to elevate the session.

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `OTP_EXPIRED` | OTP code timed out | Re-send OTP with `--send-only` and retry |
| `INVALID_OTP` | Wrong OTP code entered | Ask the user to double-check the code and retry |
| `TOKEN_EXPIRED` | Auth token has expired | Run `auth refresh --json`; if that fails, login again |
| `NOT_AUTHENTICATED` | No active session | Run the full login flow |
| `TRADE_PASSWORD_NOT_SET` | Trade password required but not set | Run `auth trade-password set --json` |
