# Java backend (Spring Boot 3) - Paytm reference

Reference Spring Boot 3 backend covering all four Paytm products: JS Checkout, Subscription (UPI Autopay), Payment Link, Dynamic QR. Plus an idempotency layer and S2S webhook receiver.

> Looking for the older Spring 5 / Tomcat 9 / WAR variant? See `scripts/backend-spring-legacy/`. Same routes, older stack.

## Stack

| | Version |
|---|---|
| Java | 17+ |
| Spring Boot | 3.3.x |
| Servlet API | `jakarta.servlet` (Servlet 6) |
| Packaging | Executable JAR (`spring-boot-maven-plugin`) |
| HTTP client | `RestTemplate` |
| Checksum | `io.github.paytm:paytmpayments-checksum:2.1.1` |

## Routes

| Method | Path | Purpose |
|---|---|---|
| GET | `/paytm-client-config.json` | mid + JS loader URL for the browser |
| POST | `/paytm/create-order` | initiateTransaction → `{orderId, txnToken, amount, mid}` (one-time payment) |
| POST | `/paytm/create-subscription` | `/subscription/create` → `{orderId, txnToken, subscriptionId, ...}` |
| POST | `/paytm/create-link` | `/link/create` → `{orderId, linkId, shortUrl, longUrl, ...}` |
| POST | `/paytm/link-transactions` | reconcile via `/link/fetchTransaction` → `{linkId, orders: [...]}` (use this for Payment Link flows, NOT `/v3/order/status`) |
| POST | `/paytm/create-qr` | `/paymentservices/qr/create` → `{orderId, qrCodeId, qrData, image, mid}` |
| POST | `/paytm/order-status` | server-side Transaction Status API |
| POST | `/paytm/webhook` | Paytm S2S webhook - verifies head.signature, dedupes by (orderId,status) |
| GET\|POST | `/paytm/callback` | Paytm browser redirect; verifies CHECKSUMHASH |

All four `/create-*` endpoints accept an `Idempotency-Key` request header (or `idempotencyKey` in the body). Repeats with the same key replay the cached response with header `Idempotent-Replayed: true`.

## Setup
```bash
mvn clean package
```

Produces an executable `target/paytm-backend.jar` and pulls the demo HTMLs from `scripts/frontend/` into `static/` on the classpath.

## Run
```bash
PAYTM_MID="YOUR_MID" \
PAYTM_MERCHANT_KEY="YOUR_MERCHANT_KEY" \
PAYTM_WEBSITE_NAME="WEBSTAGING" \
java -jar target/paytm-backend.jar
```

Demo pages (default port 8080):
- <http://localhost:8080/checkout.html> - one-time payment via JS Checkout
- <http://localhost:8080/subscription.html> - UPI Autopay subscription
- <http://localhost:8080/payment-link.html> - generate shareable payment link
- <http://localhost:8080/qr.html> - dynamic QR with auto-polling

See the repo-root `.env.example` for how to get your MID and Merchant Key.

## Env vars / system properties

Each setting can be supplied via `-Dpaytm.*` system property OR `PAYTM_*` env var OR `application.properties`.

| Var / Prop | Default |
|---|---|
| `PAYTM_MID` / `paytm.mid` | required |
| `PAYTM_MERCHANT_KEY` / `paytm.merchant.key` | required |
| `PAYTM_ENVIRONMENT` / `paytm.environment` | `staging` |
| `PAYTM_WEBSITE_NAME` / `paytm.website.name` | `WEBSTAGING` (staging) / `DEFAULT` (production) |
| `PAYTM_PG_DOMAIN` / `paytm.pg.domain` | derived from `PAYTM_ENVIRONMENT` |
| `PAYTM_CALLBACK_URL` / `paytm.callback.url` | derived from `PAYTM_CALLBACK_BASE` |
| `PAYTM_CALLBACK_BASE` / `paytm.callback.base` | `http://localhost:8080` |
| `PAYTM_STATUS_API_URL` / `paytm.status.api.url` | `<pgDomain>/v3/order/status` |
| `PAYTM_CLIENT_ID` / `paytm.client.id` | `C11` (per-merchant - confirm with your KAM) |


## Idempotency

Wired via the `Idempotency-Key` header on every `/paytm/create-*` route. Backed
by an in-memory cache (`IdempotencyCache`) - fine for the demo, **swap for Redis
or a DB row in production**. Replays return the cached response with header
`Idempotent-Replayed: true`. Definitive 4xx errors are cached too; transient 5xx
are not, so retries can succeed.

## Webhook receiver

`POST /paytm/webhook` verifies `head.signature` against the raw body bytes
Paytm signed (re-serializing breaks the signature), dedupes on
`(orderId, status)` for at-least-once delivery, then calls a stub
`fulfillOrder` hook - replace it with your DB write / queue push. Returns 200
fast on success or duplicates, 401 on signature failure, 5xx on processing
errors so Paytm retries.
