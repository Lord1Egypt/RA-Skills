# Agent-Assisted Flow and Script Contract — powpow-register

Execution details for each step of SKILL.md. All commands are `node scripts/powpow-register.mjs <subcommand> [args]`,
the script is **zero-dependency** and requires **Node ≥ 18**, and all requests go to `https://global.powpow.online` only.

## Security Design (why it's built this way)

| Design | Reason |
|---|---|
| The password is passed only via the `POWPOW_REGISTER_PASSWORD` environment variable | Process command-line arguments are visible to other processes on the same machine (argv leak surface); the environment variable is read inside the script and used immediately |
| The password is **never written to the state file** and never appears in logs | The state file may persist on disk; in generated mode it's shown once in the conversation only so the user can save it |
| The state file lives in the system temp directory (`os.tmpdir()/powpow-register-state.json`, 0600) | Contains only five fields — email / username / nickname / token / outTradeNo; `cleanup` removes it in one shot |
| The JWT obtained by the agent is exchanged for browser cookies via the official `me?token=` endpoint | The platform's official bridge designed for the HarmonyOS WebView; signature verification checks signature + validity only, no device fingerprint binding, so the user's browser can use it |
| Payment only does create-order / query / opening the cashier | The payment action and payment credentials always stay between the user and the official Alipay cashier; the agent never handles them |

## Command Reference

| Command | Key arguments | Purpose / when |
|---|---|---|
| `status` | —— | Check flow progress (reads the state file); run this first after an interrupted conversation |
| `gen-password` | —— | Generate a 24-character strong password (upper + lower case + digits), shown on stdout **once only** |
| `prepare-suggest` | `--username --nickname --email` | Record the confirmed info into the state file (register won't need them again afterwards) |
| `send-code` | `--email` | Trigger the platform to send the 6-digit code (valid 10 minutes, 60s cooldown) |
| `register` | `--code` (required); `--username --nickname --avatar --phone` (optional; skip if already in the state file) | Create the pending account; the password goes through the `POWPOW_REGISTER_PASSWORD` environment variable; on success the JWT is stored into the state file automatically |
| `login-link` | `--target pending` or `--target home` | Generates a one-click login link (dual-link design, see below) |
| `create-order` | `--package monthly\|quarterly\|yearly` (Alipay default)<br>`--provider alipay\|paypal` | Creates the payment order; Alipay returns the payment page file path + outTradeNo; PayPal returns the authorization page file path + subscriptionId (recorded into the state file automatically) |
| `query` | —— | Checks the order/subscription status. Alipay: `paid / pending / closed / unknown`; PayPal: `ACTIVE / PENDING`; poll every 10–15s |
| `refresh-login` | password via environment variable | Log in again to get a **new JWT** (subscription claim changes from NONE to ACTIVE); must run after payment arrives |
| `whoami` | —— | Use the token in the state file to check the account and subscription status (verify the activation took effect) |
| `cleanup` | —— | Delete the state file (must run at wrap-up) |

**Passing the environment variable** (the password never goes on the command line):

```bash
# bash / zsh / WSL
POWPOW_REGISTER_PASSWORD='<password>' node scripts/powpow-register.mjs register --code 123456
# PowerShell
$env:POWPOW_REGISTER_PASSWORD = '<password>'; node scripts/powpow-register.mjs register --code 123456
# cmd
set POWPOW_REGISTER_PASSWORD=<password> && node scripts/powpow-register.mjs register --code 123456
```

## Dual-Link Mechanism (core design)

The platform's login state is an HttpOnly cookie, which the agent cannot plant for the browser directly; the bridge is the official
`/api/auth/me?token=<JWT>&redirect=<in-site path>` endpoint: verify signature → auto-create
session → `Set-Cookie: powpow_token` (HttpOnly / SameSite=Lax / 7 days) → validate
redirect (must start with a single slash, `//` and backslashes forbidden, must be same-origin after parsing) → 307 temporary redirect to the target page.

There are two link targets, **generate home first, then decide whether to go through pending based on where the user lands**:

- **home link (sent by default, `--target home` → lands on `/`)**: generated and sent to the user immediately after successful registration.
  During the free testing period the user goes straight to the home page, fully usable; **if the user clicks it but lands on the subscription page, the free testing period has ended** — switch to the payment path (see below); no script changes and no re-registration needed.
- **pending link (used in the payment path, `--target pending` → lands on `/subscription`)**:
  the user's browser enters a "half-logged-in" state: the subscription page and payment return page are visible and operable. After payment arrives,
  run `refresh-login` to exchange for a new JWT with the ACTIVE claim, then send the home link once more for the full membership state.

## Full Sequence

### Fast Path (during the free testing period — the vast majority of cases)

```
1.  status                          # environment self-check
2.  (Step 2 conversation to confirm info, password either/or; generated mode: gen-password → have the user save it immediately)
3.  prepare-suggest --username U --nickname N --email E
4.  send-code --email E             # → user checks the code in their inbox (the only time leaving the conversation)
5.  POWPOW_REGISTER_PASSWORD=*** register --code 123456 [--avatar pic.jpg]
6.  login-link --target home        # → send the link to the user; one click and they're on the home page
7.  (user confirms they're in) → wrap up directly: cleanup + account card + guide first steps
```

### Payment Path (when the user wants membership, or the free testing period has ended)

```
1–5. Same as the fast path (the state already has the token after register succeeds)
6.  login-link --target pending     # → half-login link, keeps the payment return page working
7.  (user picks a payment method)
    # Alipay: create-order --package monthly|quarterly|yearly
    # PayPal: create-order --provider paypal
8.  start <payment page file>       # Windows; macOS uses open, Linux uses xdg-open
    # → the user completes payment/authorization at the Alipay/PayPal cashier (leaves the conversation)
9.  query (every 10–15s) until paid / ACTIVE
10. refresh-login                   # exchange for a new JWT with the ACTIVE claim
11. login-link --target home        # → send the full-membership link to the user
12. whoami                          # confirm subscriptionStatus: ACTIVE (optional)
13. cleanup                         # clear the state file
```
## Command → Platform API Mapping

| Script command | Platform endpoint |
|---|---|
| `send-code` | `POST /api/auth/register/send-code` |
| `register` | `POST /api/auth/register` (multipart, direct avatar upload) |
| `login-link` | `GET /api/auth/me?token=…&redirect=…` (the link itself; takes effect when the browser opens it) |
| `create-order` | `POST /api/payment/alipay/create-order` (Bearer, Alipay)<br>`GET /api/subscription/plans` + `POST /api/subscription/create` (Bearer, PayPal) |
| `query` | `GET /api/payment/alipay/query?outTradeNo=…` (Bearer, Alipay)<br>`GET /api/subscription/create` (Bearer, PayPal) |
| `refresh-login` | `POST /api/auth/login` (`{step:1, username, password}`) |
| `whoami` | `GET /api/auth/me?token=…` |

Where the rules come from: registration fields and rate limits in `registration-flow.md`; plans and the activation chain in
`payment-and-activation.md` (both cite the platform source files).

## Script-Level Error Handling

| Symptom | Handling |
|---|---|
| `Node version too low` | Fall back to pure guidance mode; don't keep trying |
| Network error / timeout | Retry once; if it still fails, have the user check the network and continue (the state file is still there; run `status` from the top to resume) |
| register returns a business error (username already exists, etc.) | Handle per the table in Step 5 of SKILL.md; **no need to resend the verification code** (still valid within 10 minutes) |
| register returns "email verification code incorrect or expired" | Timed out → `send-code` again |
| User closed the payment page after `create-order` | Just `create-order` again (the old order auto-closes after 2h; PayPal PENDING subscriptions expire after 1h) |
| `create-order --provider paypal` returns 409 | There is already an unfinished PayPal subscription; wait 1h for it to expire, or complete the old authorization in the browser |
| `query` stays pending / PENDING | The user may not have paid; ask. If they really paid → follow the troubleshooting table in payment-and-activation.md |
| User clicks the home link but lands on the subscription page | The free testing period has ended → switch to the payment path: `login-link --target pending` → pick a payment method → `create-order` |
| `refresh-login` 403 `pending_payment` | The free testing period has ended and payment hasn't arrived; go back to step 9 to keep polling, or confirm whether the user completed the payment |
| State file lost (accidentally deleted / different machine) | `whoami`/`refresh-login` are unusable; have the user refresh the subscription page directly in the browser that opened Link 1 to check the status, or log in again (web mode) |

## Fallback Mode (pure guidance)

Fall back to the v1-style pure guidance immediately — stop wrestling with the script — when any of these happens:

- No Node ≥ 18, or the script fails the same way twice in a row;
- The user explicitly says "I'll do it myself on the website";
- Company/device policy restricts the script's network access.

After falling back: give the registration page https://global.powpow.online/register (during the free testing period, web registration is equally instant; when a subscription is needed, also give the subscription page https://global.powpow.online/subscription ), troubleshoot alongside per the rules in `registration-flow.md`, keep the same tone, and still end every turn with a "next step" block.
https://global.powpow.online/subscription, walk alongside the user per the rules in `registration-flow.md` and help troubleshoot,
keep the same tone, and still end every turn with a "next step" block.
