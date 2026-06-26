# Paytm PG Troubleshooting

> _Companion to **`SKILL.md`** - load this file alongside `SKILL.md`, never instead of it._

Symptom → most-likely cause → fix. Work top-down per section.

---

## Initiate Transaction fails

### `resultCode: 227` - checksum mismatch
- Body bytes used to **generate** checksum must equal body bytes **sent**. Build `body` once, JSON-stringify once, hash the same string, then send that exact string.
- Don't pretty-print, re-serialize, or sort keys between hashing and sending.
- Wrong `MERCHANT_KEY` (staging key on prod host or vice versa).
- Trailing whitespace / newline in env var (`.env` files often add `\n`).
- For `verifySignature` on callbacks: pass the form params *minus* `CHECKSUMHASH` - and as the raw map, not a JSON string.

### `resultCode: 330` - invalid orderId
- `orderId` charset: alphanumerics + `_` / `@` / `-`. Avoid `.`, spaces, slashes, unicode.
- Length ≤ ~50 chars. UUIDs without hyphens or hex tokens are safe.

### `resultCode: 334` - duplicate orderId
- `orderId` already used (even for a *failed* prior attempt). Generate a fresh one for every retry; never reuse.

### `resultCode: 335` - request expired / invalid
- System clock skew on server, or stale request being retried.

### `resultCode: 400` / HTTP 400 - bad request
- Missing required field. Always include: `requestType`, `mid`, `websiteName`, `orderId`, `callbackUrl`, `txnAmount.value`, `txnAmount.currency`, `userInfo.custId`.
- `websiteName` must match the value provisioned for your MID on the dashboard (e.g. `WEBSTAGING`, `DEFAULT`, `retail`). Wrong value → silent failure or `400`.
- `txnAmount.value` must be a **string**, two-decimal, INR (`"1.00"`, not `1.0` or `1`).

### `resultCode: 501` / `502` / 5xx - Paytm system error
- Transient. Retry with the **same** orderId (idempotent on Paytm side until success).

### `MISSING_TXN_TOKEN`
- HTTP 200 but no `body.txnToken`. Inspect `body.resultInfo.resultMsg`. Usually a config error (websiteName / industryTypeId / channelId mismatch on dashboard).

---

## `Failed to parse URL from /paytm-client-config.json` (or `/paytm/create-order`)

You're calling `fetch()` with a relative or root-relative URL in a context where it's evaluated by **Node's `fetch`** (not the browser's). Node requires absolute URLs.

Where this happens:
- **Next.js / Remix / SvelteKit SSR** - the component runs server-side first.
- **React Server Components** - runs in Node.
- **Node test scripts** that import the frontend code.
- HTML opened via `file://` (relative resolves but the request fails differently).

Two fixes, pick one:

1. **Always use absolute URLs in browser-only code.** The reference frontends use `new URL("paytm/create-order", document.baseURI).toString()` - works in browser regardless of mount path, fails fast in SSR (so you know not to call it there).
2. **For SSR / Node contexts:** prepend the backend origin explicitly:
   ```js
   const base = process.env.PAYTM_BACKEND_BASE || "http://localhost:3001";
   fetch(`${base}/paytm/create-order`, { ... })
   ```
   Or move the fetch into a `useEffect` / client-only component so it never runs server-side.

Rule of thumb: any code that talks to your `/paytm/*` backend endpoints is client-side only - guard it with `"use client"` (Next.js), `onMount` (Svelte), or browser-only checks (`typeof window !== "undefined"`).

---

## "Pay" button does nothing - modal doesn't open on click

The most common cause is wrapping `CheckoutJS.init`/`invoke` inside `CheckoutJS.onLoad()` *inside* the click handler. `onLoad` fires once at script-load time; by the time the user clicks, it has already fired and your callback never runs.

**Fix:** Use the merchant script's `onload` (or `Paytm.CheckoutJS.onLoad` only if the script is a static `<script src=...>` tag) to enable the button at page level; call `init`/`invoke` **directly** in the click handler — never wrap them inside `Paytm.CheckoutJS.onLoad()`. Full pattern in `SKILL.md` → "Common Integration Bugs" → #3, and live code in `scripts/frontend/checkout.html`.

Other causes for the same symptom:
- Browser popup blocker - invoke must come from a real user gesture (it does, in the click handler).
- `txnToken` already used / expired - generate a fresh one for each click.
- `window.Paytm` undefined - script loader didn't finish; check Network tab for the merchant `.js` file.

---

## JS Checkout doesn't render

| Symptom | Likely cause |
|---|---|
| `window.Paytm` undefined | Loader `<script>` not loaded - wrong MID in URL, or merchant not provisioned for CheckoutJS on that environment |
| Blank popup, immediate close | Browser blocked the popup. Use `redirect: true` or trigger from a user gesture (click handler) |
| `init` resolves but `invoke` does nothing | `txnToken` already used / expired (15-min TTL) - generate a fresh one |
| `SESSION_EXPIRED` event | `txnToken` past its 15-minute TTL - call `/paytm/create-order` again |
| Loader 403 / 404 | PG domain mismatch - check Developer Settings → API Keys on the dashboard for the correct host |
| Mixed-content blocked | Page on HTTP loading HTTPS Paytm script; serve your page over HTTPS |

---

## Callback arrives but is ignored / treated as failure

- **Callback verification is a separate scheme from API checksum.** Build a `TreeMap`/sorted dict of all POSTed params *except* `CHECKSUMHASH`, then call `PaytmChecksum.verifySignature(map, key, checksum)`.
- Field names from Paytm are uppercase (`ORDERID`, `TXNID`, `TXNAMOUNT`, `STATUS`, `RESPCODE`, `RESPMSG`, `CHECKSUMHASH`, `BANKTXNID`, `PAYMENTMODE`, `GATEWAYNAME`, `BANKNAME`, `CURRENCY`, `TXNDATE`).
- Some browsers receive the callback as **GET** (not POST) when the user hits *Back*. Implement both.
- The callback is the user's browser - **not** a webhook. It can be lost (popup blocker, network drop). Always reconcile with the Transaction Status API or the S2S webhook.

---

## Transaction Status API gives `S` / `TXN_SUCCESS` but order not delivered

- Don't trust the JS callback alone. Final source of truth: **`/v3/order/status`** server-to-server.
- Compare `TXNAMOUNT` against your stored amount before fulfilling - defends against tampered redirects.
- If `STATUS == PENDING` keep polling (typical: 30s → 2m → 5m → give up at 30m, then mark `FAILURE`).

---

## Refunds

| Symptom | Cause |
|---|---|
| `refundAmount > txnAmount` rejected | Partial refunds allowed but cumulative ≤ original |
| `Duplicate refId` | `refId` is unique per refund attempt; generate fresh per call |
| Refund stuck `PENDING` | Bank-side delay, can take up to T+7 working days |

---

## Expanded RESPCODE reference

Paytm publishes an authoritative table; common ones merchants hit:

| RESPCODE | RESPMSG / Meaning | Action |
|---|---|---|
| `01` | Txn success | Fulfill order |
| `141` | User cancelled at bank page | Allow retry |
| `227` | Checksum mismatch | See "Initiate Transaction fails" above |
| `235` | Insufficient bank balance | Show retry / different payment option |
| `267` | Bank declined | Retry / switch payment option |
| `295` | Invalid card details | User error |
| `334` | Duplicate orderId | Generate new orderId |
| `335` | Request expired | New session |
| `400` | Bad request | Check field formats |
| `401` | Unauthorized | MID/key mismatch |
| `402` | Pending - awaiting bank | Poll Transaction Status |
| `501` | System error | Retry |
| `810` | Risk system declined | Contact Paytm support |
| `911` / `BANK_PENDING` | Bank confirmation pending | Poll, do not refund |

For unfamiliar codes: query Transaction Status API with the orderId - `body.resultInfo.resultMsg` is the canonical explanation. Full list: <https://www.paytmpayments.com/docs/response-codes>.

---

## Corp proxy TLS interception (`UNABLE_TO_GET_ISSUER_CERT_LOCALLY`)

Symptom: Node `fetch` to `https://secure.paytmpayments.com` (prod) fails with `UNABLE_TO_GET_ISSUER_CERT_LOCALLY`, `SELF_SIGNED_CERT_IN_CHAIN`, or `unable to verify the first certificate`. Staging (`securestage.paytmpayments.com`) often works because many corp proxies exempt non-prod hosts from TLS inspection.

Cause: A corporate proxy (Zscaler / Netskope / Palo Alto / BlueCoat / etc.) is doing TLS interception - it terminates the TLS connection, re-signs the response with an internal CA, and forwards it to your machine. Your OS keychain trusts that internal CA, but Node / Python / Java each ship their own CA bundle and don't pick it up automatically.

### Fix 1 (recommended): Trust the corp CA in your runtime

Extract the corp root cert, then point your runtime at it. TLS verification stays ON.

**macOS** - export from System keychain:
```bash
mkdir -p ./certs
security find-certificate -a -p /Library/Keychains/System.keychain > ./certs/corp-proxy-ca.crt
# Or just the corp root if you know its CN:
security find-certificate -a -c "YourCorpName Root CA" -p \
  /Library/Keychains/System.keychain > ./certs/corp-proxy-ca.crt
```

**Linux** - usually already in the system bundle:
```bash
cp /etc/ssl/certs/ca-certificates.crt ./certs/corp-proxy-ca.crt
# Debian/Ubuntu: corp certs land in /usr/local/share/ca-certificates/ after `update-ca-certificates`
```

**Windows (PowerShell, admin)**:
```powershell
Get-ChildItem Cert:\LocalMachine\Root |
  Where-Object Subject -match "YourCorpName" |
  Export-Certificate -FilePath .\certs\corp-proxy-ca.crt -Type CERT
```

**Pull what the proxy is actually serving** (works on any OS with openssl):
```bash
openssl s_client -showcerts -connect secure.paytmpayments.com:443 </dev/null \
  2>/dev/null | sed -n '/BEGIN CERT/,/END CERT/p' > ./certs/corp-proxy-ca.crt
```

Then per runtime:

| Runtime | Config |
|---|---|
| Node | `NODE_EXTRA_CA_CERTS=./certs/corp-proxy-ca.crt` in `.env`, restart |
| Python (requests) | `REQUESTS_CA_BUNDLE=./certs/corp-proxy-ca.crt` |
| Python (httpx) | `SSL_CERT_FILE=./certs/corp-proxy-ca.crt` |
| Java | `keytool -import -alias corpProxy -file ./certs/corp-proxy-ca.crt -keystore $JAVA_HOME/lib/security/cacerts -storepass changeit` |
| curl | `curl --cacert ./certs/corp-proxy-ca.crt ...` |

Verify:
```bash
node -e "fetch('https://secure.paytmpayments.com').then(r=>console.log(r.status)).catch(e=>console.error(e.code))"
```
Should print a status code (e.g. `404`), not an error code.

### The asymmetric-MITM trap (the one that actually bit us)

Some corp proxies (Zscaler is the common one) intercept **staging hosts but pass production through unintercepted** - or vice versa. This produces a confusing failure mode:

| Endpoint | Proxy behavior | Chain Node sees | Trusted? |
|---|---|---|---|
| `securestage.paytmpayments.com` | MITM (re-signed with corp intermediate) | Corp-issued | Only if corp CA is trusted |
| `secure.paytmpayments.com` | Passthrough | Real DigiCert chain | Only if DigiCert root is trusted |

If your shell exports `SSL_CERT_FILE=~/zscaler-root-ca.pem` (Zscaler's installer does this), Node uses **only** that file as its trust store - DigiCert is gone. Staging works, prod fails with `UNABLE_TO_GET_ISSUER_CERT_LOCALLY`. Same outcome on Python (`requests` honors `SSL_CERT_FILE` too).

### `SSL_CERT_FILE` vs `NODE_EXTRA_CA_CERTS` - critical distinction

| Variable | Behavior | Effect |
|---|---|---|
| `SSL_CERT_FILE` | **Replaces** Node's bundled trust store | Only the CAs in that file are trusted - public CAs (DigiCert, Let's Encrypt, etc.) are silently dropped |
| `NODE_EXTRA_CA_CERTS` | **Adds** to Node's bundled trust store | Public CAs still trusted, plus the extras |

Always prefer `NODE_EXTRA_CA_CERTS`. If `SSL_CERT_FILE` is set in your environment (check `env | grep SSL_CERT_FILE`), unset it for the Node process:

```bash
# Correct - drops the variable entirely
env -u SSL_CERT_FILE NODE_EXTRA_CA_CERTS=./certs/corp-proxy-ca.crt node server.js

# WRONG - empty string still tells Node "use this (empty) file as the trust store"
SSL_CERT_FILE= NODE_EXTRA_CA_CERTS=./certs/corp-proxy-ca.crt node server.js
```

In a `package.json` script:
```json
"start": "env -u SSL_CERT_FILE NODE_EXTRA_CA_CERTS=./certs/corp-proxy-ca.crt node server.js"
```

Python equivalent: `unset SSL_CERT_FILE REQUESTS_CA_BUNDLE` before running, then point `REQUESTS_CA_BUNDLE` at a bundle that contains **both** the corp CA and the public roots (concatenate `certifi.where()` output with your corp PEM).

### Fix 2: Ask IT to bypass TLS inspection for Paytm

One-line ticket: "Please exempt `*.paytmpayments.com` from TLS inspection - payment gateway, PCI-scope traffic." Most proxies have a financial-services bypass category already.

### Fix 3: Run from outside the corp network (fastest for a demo)

- Phone hotspot - proxy isn't in the path, real Paytm chain validates, zero config.
- Cloud VM (EC2 / Render / Fly / Railway) - point your demo at that origin.
- Home network over personal VPN.

### What NOT to do

- **Do not** set `NODE_TLS_REJECT_UNAUTHORIZED=0` or `rejectUnauthorized: false` with real production merchant credentials. It disables verification for *every* outbound HTTPS call in the process - any host on-path can read your `MERCHANT_KEY`.
- **Do not** set `verify=False` (Python `requests`) or trust-all `SSLContext` (Java) in prod for the same reason.
- **Do not** commit the extracted CA bundle to a public repo - it's not secret, but it leaks your employer's name and proxy vendor.

### Quick triage

```
prod TLS fails, staging works?      → corp proxy intercepting prod only → Fix 1 or 2
both fail with same cert error?     → corp proxy intercepting all → Fix 1 or 2
both fail, different errors?        → not a TLS issue → check DNS / firewall / MID env mismatch
works on hotspot, fails on wifi?    → confirmed corp-proxy MITM → Fix 1, 2, or 3
```

---

## Environment / config gotchas

- **PG domain.** Use `https://secure.paytmpayments.com` (prod) and `https://securestage.paytmpayments.com` (staging). The exact host provisioned for your MID is shown under Developer Settings → API Keys on the dashboard.
- **One environment per MID.** Staging MID will not authenticate against prod host (and gives `401`/checksum errors that look like a key mismatch).
- **`websiteName` is per-MID.** Defaults seen: `DEFAULT`, `WEB_STAGING`, `WEBSTAGING`, `retail`. Wrong value → `initiateTransaction` succeeds with a token that fails to render.
- **Currency is INR-only** for domestic Paytm PG. Cross-border requires a separate account.

---

## Quick decision tree

```
Payment failed?
├─ Did initiateTransaction return a txnToken?
│   ├─ No  → check resultInfo.resultMsg → see "Initiate Transaction fails"
│   └─ Yes
│       ├─ Did JS Checkout render?
│       │   ├─ No  → see "JS Checkout doesn't render"
│       │   └─ Yes
│       │       ├─ Did Paytm POST callback?
│       │       │   ├─ No  → call Transaction Status API anyway (browser issue)
│       │       │   └─ Yes
│       │       │       └─ Did CHECKSUMHASH verify?
│       │       │           ├─ No  → "Callback arrives but is ignored"
│       │       │           └─ Yes → call /v3/order/status - that is the truth
```
