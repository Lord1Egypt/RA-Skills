# Agent do-am flow and script contract — powpow-register

Execution details for each step of SKILL.md. All commands na `node scripts/powpow-register.mjs <sub-command> [parameters]`, di script **zero dependency**, e need **Node >= 18**, all requests dey go only `https://global.powpow.online`.

## Security design (why dem design am like dis)

| Design | Reason |
|---|---|
| Password only pass in through di environment variable `POWPOW_REGISTER_PASSWORD` | Di command line arguments of a process fit dey visible to other processes on di same machine (argv leak surface), di environment variable inside di script dem read am and use am sharp sharp |
| Password **never write into state file**, never show inside log | Di state file fit remain on disk; inside di chat, di generate mode show am once only so di user go save am |
| Di state file dey store for di system temporary directory (`os.tmpdir()/powpow-register-state.json`, 0600) | E only contain five fields: email / username / nickname / token / outTradeNo, `cleanup` go clear am one click |
| Di JWT wey agent collect, dem exchange am for browser cookie through di official `me?token=` endpoint | Na di official bridge wey di platform build for Harmony WebView; di signature check only check signature + validity period, e no bind device fingerprint, di user browser fit use am |
| Payment only do create-order / query / open cashier | Di payment action and payment credential always dey between di user and di Alipay official cashier, agent no dey pass through am |

## Command reference

| Command | Key parameters | Work / when |
|---|---|---|
| `status` | —— | Check di flow progress (read di state file); after chat break, run dis one first |
| `gen-password` | —— | Generate 24-character strong password (contain capital + small letter and number), e show for stdout **only dis one time** |
| `prepare-suggest` | `--username --nickname --email` | Write di confirmed info into di state file (after dat register no need pass dem again) |
| `send-code` | `--email` | Trigger di platform to send 6-digit verification code (e dey valid 10 minutes, 60s cooldown) |
| `register` | `--code` (required); `--username --nickname --avatar --phone` (optional, if di state file get dem, no need pass am) | Build pending account; password pass through `POWPOW_REGISTER_PASSWORD` environment variable; after success di JWT go save into di state file automatic |
| `login-link` | `--target pending` or `--target home` | E dey generate one-click login link (dual-link design, see below) |
| `create-order` | `--package monthly\|quarterly\|yearly` (Alipay default)<br>`--provider alipay\|paypal` | Create di payment order; Alipay return di payment page file path + outTradeNo; PayPal return di authorization page file path + subscriptionId (e dey write into di state file automatic) |
| `query` | —— | Check di order/subscription status. Alipay: `paid / pending / closed / unknown`; PayPal: `ACTIVE / PENDING`; poll every 10–15s |
| `refresh-login` | Password pass through environment variable | Login again to change to **new JWT** (di subscription claim change from NONE to ACTIVE), you must run am after money land |
| `whoami` | —— | Use di token inside di state file to check di account and subscription status (verify whether di activation don work) |
| `cleanup` | —— | Delete di state file (you must run am at di end) |

**Environment variable passing** (password never enter command line):

```bash
# bash / zsh / WSL
POWPOW_REGISTER_PASSWORD='<password>' node scripts/powpow-register.mjs register --code 123456
# PowerShell
$env:POWPOW_REGISTER_PASSWORD = '<password>'; node scripts/powpow-register.mjs register --code 123456
# cmd
set POWPOW_REGISTER_PASSWORD=<password> && node scripts/powpow-register.mjs register --code 123456
```

## Dual-Link Mechanism (core design)

Di platform login state na HttpOnly cookie, wey di agent no fit plant am for di browser directly; di bridge na di official
`/api/auth/me?token=<JWT>&redirect=<in-site path>` endpoint: verify signature → auto-create
session → `Set-Cookie: powpow_token` (HttpOnly / SameSite=Lax / 7 days) → validate
redirect (must start with single slash, `//` and backslash dem forbid, must be same-origin after parsing) → 307 temporary redirect to di target page.

Two link targets dey, **first generate home, then decide whether to pass through pending based on where di user land**:

- **home link (wey dem dey send by default, `--target home` → land for `/`)**: dem dey generate am and send to di user right after registration succeed.
  During di free testing period di user dey go straight to di home page, fully usable; **if di user click am but land for di subscription page, di free testing period don end** — switch to di payment path (see below); no need to change script and no need to register again.
- **pending link (wey dem dey use for di payment path, `--target pending` → land for `/subscription`)**:
  di user browser dey enter "half-logged-in" state: di subscription page and di payment return page dey visible and dey workable. After payment arrive,
  run `refresh-login` to exchange for new JWT with di ACTIVE claim, then send di home link again for di full membership state.

## Full Sequence

### Fast Path (during di free testing period — di vast majority of cases)

```
1.  status                          # environment self-check
2.  (step 2 conversation to confirm info, password either/or; generated mode: gen-password → tell di user make e save am at once)
3.  prepare-suggest --username U --nickname N --email E
4.  send-code --email E             # → user check di code for inbox (di only time to comot from di conversation)
5.  POWPOW_REGISTER_PASSWORD=*** register --code 123456 [--avatar pic.jpg]
6.  login-link --target home        # → send di link to di user; one click and e don dey for home page
7.  (user confirm say e don enter) → wrap up directly: cleanup + account card + guide di first steps
```

### Payment Path (wen di user want membership, or di free testing period don end)

```
1–5. Same as di fast path (di state already get di token after register succeed)
6.  login-link --target pending     # → half-login link, keep di payment return page working
7.  (user pick payment method)
    # Alipay: create-order --package monthly|quarterly|yearly
    # PayPal: create-order --provider paypal
8.  start <payment page file>       # Windows; macOS dey use open, Linux dey use xdg-open
    # → di user complete payment/authorization for di Alipay/PayPal cashier (e comot from di conversation)
9.  query (every 10–15s) until paid / ACTIVE
10. refresh-login                   # exchange for new JWT with di ACTIVE claim
11. login-link --target home        # → send di full-membership link to di user
12. whoami                          # confirm subscriptionStatus: ACTIVE (optional)
13. cleanup                         # clear di state file
```
## Command → platform API mapping

| Script command | Platform endpoint |
|---|---|
| `send-code` | `POST /api/auth/register/send-code` |
| `register` | `POST /api/auth/register` (multipart, avatar direct upload) |
| `login-link` | `GET /api/auth/me?token=…&redirect=…` (na di link itself, e work when di browser click am) |
| `create-order` | `POST /api/payment/alipay/create-order` (Bearer, Alipay)<br>`GET /api/subscription/plans` + `POST /api/subscription/create` (Bearer, PayPal) |
| `query` | `GET /api/payment/alipay/query?outTradeNo=…` (Bearer, Alipay)<br>`GET /api/subscription/create` (Bearer, PayPal) |
| `refresh-login` | `POST /api/auth/login` (`{step:1, username, password}`) |
| `whoami` | `GET /api/auth/me?token=…` |

Where di rules come from: registration fields and rate limit see `registration-flow.md`; packages and activation chain see `payment-and-activation.md` (dem all mark di platform source code file).

## Script-level error handling

| Wetin you see | How to handle am |
|---|---|
| `Node 版本过低` (Node version too low) | Fall back to guide-only mode, no force try |
| Network error / timeout | Retry one time; if e still fail, make di user check di network then continue (di state file still dey, run `status` from di start to recover) |
| register report business error (用户名已存在 etc.) | Handle am with di table for SKILL.md Step 5, **no need resend di verification code** (e still dey valid within 10 minutes) |
| register report 邮箱验证码错误或已过期 | If e timeout → run `send-code` again |
| After `create-order` di user close di payment page | Just run `create-order` again (old order go close automatic after 2h; PayPal PENDING subscription expire after 1h) |
| `create-order --provider paypal` returns 409 | There is already an unfinished PayPal subscription; wait 1h for it to expire, or complete the old authorization in the browser |
| `query` dey pending anyhow / PENDING | Di user fit be say e no pay yet; ask am one question. If e truly pay → follow di troubleshooting table for payment-and-activation.md |
| User click di home link but land for di subscription page | Di free testing period don end → switch to di payment path: `login-link --target pending` → pick payment method → `create-order` |
| `refresh-login` 403 `pending_payment` | Di free testing period don end and payment no arrive; go back to step 9 to keep polling, or confirm whether di user complete di payment |
| Di state file lost (hand slip delete am / change machine) | `whoami`/`refresh-login` no fit work; make di user for di browser wey don open link 1 before, refresh di subscription page direct to confirm di status, or login again (web mode) |

## Fall back mode (guide only)

For any of di following situations, fall back to v1-style guide-only sharp sharp, no dey disturb di script again:

- No get Node >= 18 or di script fail two times straight with di same kind of failure;
- Di user talk am clear say "I go do am myself for di web";
- Company/device policy no allow di script to connect internet.

After you fall back: give di registration page https://global.powpow.online/register (during di free testing period, web registration dey equally instant; wen subscription dey needed, still give di subscription page https://global.powpow.online/subscription ), troubleshoot along per di rules for `registration-flow.md`, keep di same tone, and still end every turn with "next step" block.
