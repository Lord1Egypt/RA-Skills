---
name: keymint
description: Add software licensing to an app with Keymint. Choose a licensing model (node-locked, floating, offline, subscription), create and manage license keys, activate and deactivate devices, run floating (concurrent-seat) licenses, issue offline signed licenses, and manage customers through the Keymint REST API or official SDKs (Node.js, Python, Go, C#, PHP).
version: 1.0.1
metadata:
  openclaw:
    requires:
      env:
        - KEYMINT_API_KEY
      anyBins:
        - curl
        - node
        - python3
    primaryEnv: KEYMINT_API_KEY
    envVars:
      - name: KEYMINT_API_KEY
        required: true
        description: Keymint API key (Bearer token). Use a client-scoped key for activation flows, read-only for lookups, admin only for management tasks.
      - name: KEYMINT_PRODUCT_ID
        required: false
        description: Default Keymint product ID when the user does not name one.
    emoji: "\U0001F511"
    homepage: https://keymint.dev
---

# Keymint licensing

[Keymint](https://keymint.dev) is a licensing API for software vendors: license keys, device activation limits, floating seats, offline licenses, and customer records. Use this skill when the user wants to license, sell, or protect a desktop app, CLI, plugin, or SaaS add-on, or wants to manage existing Keymint keys and customers.

## Choosing a licensing model

| Product | Model | How it works |
|---|---|---|
| Single-user desktop app, paid per machine | Node-locked | A key activates on a limited number of devices, each identified by a stable `hostId`. Each activation uses a device slot. |
| Team or enterprise tool, paid per seat | Floating | A pool of concurrent seats: clients check out a seat, keep it with signed heartbeats, and check it in on exit. |
| Air-gapped, embedded or offline kiosk | Offline signed | Your server signs an Ed25519 license file; the app verifies it locally with a bundled public key. No network or API key at runtime. |
| SaaS or app with recurring billing | Subscription + activation | Time-limited keys. Keymint does not watch your billing: your payment webhook (for example Stripe's) creates the key on purchase and blocks or deletes it on cancellation through the API. See the [Stripe guide](https://keymint.dev/docs/guides/stripe-subscription-licensing). |

## Setup

1. Create a free account at [app.keymint.dev](https://app.keymint.dev/auth/login?type=signup). The free plan covers 1 product and 25 license keys, with floating and offline licensing included. Paid plans are listed on the [pricing page](https://keymint.dev/pricing).
2. Create a product in the dashboard and copy its **Product ID**.
3. Go to **Developer → API Keys**, click **Create key**, pick a scope, and copy the key. It is shown once.
4. Export it for this session:

```bash
export KEYMINT_API_KEY="..."        # never commit this or print it back to the user
export KEYMINT_PRODUCT_ID="..."     # optional default
```

### Pick the right key scope

| Scope | Use for | Can be shipped inside an app? |
|---|---|---|
| `client` | Activate, deactivate the current device, floating checkout/heartbeat/checkin | Yes, this is the only scope meant for bundling |
| `read-only` | Look up key details and customers | No |
| `admin` | Create, update, block, unblock, sign offline licenses, manage customers | No, server-side or local use only |

Prefer the narrowest scope that does the job, and bind keys to a single product in the dashboard when possible. Never embed `admin` or `read-only` keys in shipped client code, and never log raw API keys or license keys.

## API basics

- Base URL: `https://api.keymint.dev`
- Auth header: `Authorization: Bearer $KEYMINT_API_KEY`
- Bodies are JSON. Success responses carry `"code": 0`; errors carry a non-zero `code` and a `message`.
- Mutating requests accept an `Idempotency-Key` header (a fresh UUID per operation) so retries are safe.
- Errors carry `message`, a numeric `code` and a stable `errorCode` string such as `license_invalid_or_forbidden`, `activation_limit_reached` or `rate_limited`. Branch on `errorCode`, never on the message text: [error codes](https://keymint.dev/docs/api-reference/error-codes).
- Request bodies are limited to 64 KB (`413 payload_too_large`), and every field has a limit (`400 invalid_request` names the field).
- Raw license keys are returned when a key is created, and by `GET /key` to admin keys; everyone else sees them masked.
- Product-bound API keys only work for their own products and cannot use the customer endpoints.
- OpenAPI spec: [keymint.dev/openapi.json](https://keymint.dev/openapi.json)
- Full reference: [keymint.dev/docs](https://keymint.dev/docs)

## Common tasks

### Create a license key (admin)

```bash
curl -s https://api.keymint.dev/key \
  -H "Authorization: Bearer $KEYMINT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: <new-uuid>" \
  -d '{
    "productId": "'"$KEYMINT_PRODUCT_ID"'",
    "maxActivations": 3,
    "expiryDate": "2027-12-31T00:00:00.000Z",
    "newCustomer": { "name": "Jane Doe", "email": "jane@example.com" },
    "metadata": { "is_trial": false, "features": { "pro_mode": true } }
  }'
```

Returns `{ "code": 0, "key": "XXXXX-XXXXX-XXXXX-XXXXX" }`. One key per request. Use `customerId` instead of `newCustomer` to attach an existing customer (not both). For seat-based licenses set `"licenseType": "floating"` and `"maxConcurrentSessions"`.

### Activate on a device (client)

```bash
curl -s https://api.keymint.dev/key/activate \
  -H "Authorization: Bearer $KEYMINT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "productId": "...", "licenseKey": "XXXXX-...", "hostId": "<stable device id>" }'
```

- `hostId` must be stable across restarts. The SDKs provide one (Node: `KeyMint.getOrCreateInstallationId()`). Omitting it uses a single shared `"N/A"` slot, which is not device binding.
- Optional `licensee: { name, email }` attaches an anonymous buyer to an unassigned license.
- The response includes `expirationDate` (ISO string, or `null` if it never expires) and `metadata` (including feature flags). Store the last `expirationDate`: an expired key fails with the same generic error as an invalid one, so the stored date is how the app can tell the user it expired.
- HTTP 402 means the vendor's workspace billing blocks new activations.

### Deactivate (client or admin)

`POST /key/deactivate` with `productId`, `licenseKey` and `hostId`. Client keys must send `hostId` and can only free that device. Admin keys may omit `hostId` to remove every activation.

### Look up a key (read-only or admin)

`GET /key?productId=...` with the license key in an `x-license-key` header, not the query string, so it stays out of logs. Client keys cannot use this endpoint.

### Update, block, unblock, delete (admin)

- `PATCH /key` with `productId`, `licenseKey` and any of `maxActivations` (number or `"unlimited"`), `expiryDate`, `customerId` (or `null` to unassign), `newCustomer`.
- `POST /key/block` and `POST /key/unblock` with `productId` and `licenseKey`.
- `DELETE /key` with a JSON body of `productId` and `licenseKey` permanently deletes the key and its device activations. Prefer blocking unless the user clearly wants it gone.

### Floating licenses (client)

Concurrent-seat licensing with proof of possession:

1. `POST /key/checkout` with `productId`, `licenseKey`, `hostId`. Returns `sessionId`, `sessionSecret`, `nextNonce`, `heartbeatInterval`, `expiresAt`.
2. Every `heartbeatInterval` seconds, `POST /key/heartbeat` with `productId`, `licenseKey`, `sessionId`, `timestamp` set to the latest `nextNonce`, and `signature` = hex HMAC-SHA256 of `"<sessionId>:<nonce>"` keyed with `sessionSecret`. Each response returns a new `nextNonce`; always use the newest one.
3. On exit, `POST /key/checkin` with the same fields to release the seat.

Checking out again for a `hostId` that still holds an active session extends it, and must include the same `timestamp` and `signature` pair to prove it owns the session.

Keep `sessionSecret` in memory only. The SDKs (`floatingCheckout`, `floatingHeartbeat`, `floatingCheckin`) handle the signing for you.

### Offline licenses (admin)

`POST /key/sign` with `productId`, `licenseKey`, `hostId` and optional `ttl` in seconds (60 to 315,360,000; required when the license never expires and the product sets no maximum offline lifetime). Returns a `.lic` file containing an Ed25519-signed JWT. The app verifies it locally against Keymint public keys bundled in the app, matched by key ID (`kid`). See [Offline Verification](https://keymint.dev/docs/topics/offline-key).

### Customers (admin; reads also work with read-only)

| Method | Path | Notes |
|---|---|---|
| POST | `/customer` | Create `{ name, email }` |
| GET | `/customer?page=&limit=&email=` | List or search |
| GET | `/customer/by-id?customerId=` | One customer |
| GET | `/customer/keys?customerId=` | A customer's license keys |
| PUT | `/customer/by-id` | Update; body is `customerId`, `name` and `email`. Send both fields: omitting `email` clears it |
| POST | `/customer/disable?customerId=` | Toggle active status |
| DELETE | `/customer?customerId=` | Deletes the customer; their license keys are kept and unassigned |

Confirm with the user before blocking or deleting keys, deleting customers, or removing all activations.

## Integrating into an app

Prefer an official SDK over hand-written HTTP calls:

| Language | Install |
|---|---|
| Node.js / TypeScript | `npm install keymint` |
| Python | `pip install keymint` |
| Go | `go get github.com/keymint-dev/keymint-go` |
| C# / .NET | `dotnet add package Keymint` |
| PHP | [keymint-dev/keymint-php](https://github.com/keymint-dev/keymint-php) |

```typescript
import { KeyMint } from 'keymint';

const client = new KeyMint(process.env.KEYMINT_API_KEY!); // client-scoped key
const hostId = KeyMint.getOrCreateInstallationId();

const result = await client.activateKey({
  productId: process.env.KEYMINT_PRODUCT_ID!,
  licenseKey: userEnteredKey,
  hostId,
});
```

Starter templates with licensing already wired in:

- Electron: [keymint-electron-starter](https://github.com/keymint-dev/keymint-electron-starter), guide: [Electron licensing](https://keymint.dev/docs/guides/electron-licensing)
- Tauri: [keymint-tauri-starter](https://github.com/keymint-dev/keymint-tauri-starter), guide: [Tauri licensing](https://keymint.dev/docs/guides/tauri-licensing)
- Next.js SaaS: [keymint-nextjs-starter](https://github.com/keymint-dev/keymint-nextjs-starter)
- PyQt: [keymint-pyqt-starter](https://github.com/keymint-dev/keymint-pyqt-starter)

Recommended app flow: ask for the key on first run, activate with a stable `hostId`, cache the result and `expirationDate`, re-activate on launch when online, and show a clear message when activation fails. Use `metadata.features` from the activation response to gate paid features.
