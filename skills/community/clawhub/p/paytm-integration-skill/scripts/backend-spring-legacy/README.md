# Paytm backend - Spring MVC 5 (WAR) - LEGACY

> **The recommended Java reference is `scripts/backend-spring/`** - Spring Boot 3
> + Jakarta + executable JAR. Use this legacy WAR variant only if you're stuck on
> Tomcat 9 / Java EE 8 / `javax.servlet`.

Plain Spring MVC 5.3 packaged as a WAR for deployment to Tomcat 9 / Jetty 9. Same
four-product routes as the Boot variant (including idempotency + webhook).

## Stack

| | Version | Why |
|---|---|---|
| Java | 11+ | `maven.compiler.release=11` |
| Spring MVC | 5.3.x | Pinned to last `javax.servlet` line for Tomcat 9 / Java EE 8 compatibility |
| Servlet API | `javax.servlet:javax.servlet-api:4.0.1` (provided) | Matches Tomcat 9 |
| HTTP client | `RestTemplate` | Simpler than WebClient for synchronous Paytm calls |
| Checksum | `io.github.paytm:paytmpayments-checksum:2.1.1` | Official Paytm lib |

> **Migrating to Spring 6 / Spring Boot 3?** Switch the servlet dependency to `jakarta.servlet:jakarta.servlet-api:6.0.0` and update *every* `import javax.servlet.*` → `import jakarta.servlet.*`. The current code uses `javax.*` deliberately to stay on the LTS-supported Tomcat 9 line.

## Setup
```bash
mvn -s maven-central-settings.xml clean package
```

Produces `target/paytm-backend.war`.

## Run (Tomcat 9 example)
```bash
PAYTM_MID=YOUR_MID \
PAYTM_MERCHANT_KEY=YOUR_KEY \
PAYTM_ENVIRONMENT=staging \
PAYTM_CALLBACK_BASE=http://localhost:8080/paytm-backend \
$CATALINA_HOME/bin/catalina.sh run
```

Drop the WAR into `$CATALINA_HOME/webapps/`. Open <http://localhost:8080/paytm-backend/checkout.html>.

## Env vars / system properties

Each setting can be supplied via `-Dpaytm.*` system property OR `PAYTM_*` env var OR `src/main/resources/application.properties`.

| Var / Prop | Default |
|---|---|
| `PAYTM_MID` / `paytm.mid` | required |
| `PAYTM_MERCHANT_KEY` / `paytm.merchant.key` | required |
| `PAYTM_ENVIRONMENT` | `production` (set to `staging` for sandbox) |
| `PAYTM_PG_DOMAIN` / `paytm.pg.domain` | derived from environment |
| `PAYTM_CALLBACK_BASE` / `paytm.callback.base` | `http://localhost:8080/paytm-backend` |
| `PAYTM_CALLBACK_URL` / `paytm.callback.url` | derived from base + `/paytm/callback` |
| `PAYTM_STATUS_API_URL` / `paytm.status.api.url` | `<pg>/v3/order/status` |

`websiteName` and `channelId` are class constants in `PaytmMerchantConfig` (`retail` / `WEB`) - change them if your dashboard uses different values.

## Endpoints

| Method | Path (relative to context `/paytm-backend`) | Purpose |
|---|---|---|
| GET | `/paytm-client-config.json` | mid + JS loader URL for the browser |
| POST | `/paytm/create-order` | initiateTransaction → `{orderId, txnToken, amount, mid}` (one-time payment) |
| POST | `/paytm/create-subscription` | `/subscription/create` → `{orderId, txnToken, subscriptionId, ...}` |
| POST | `/paytm/create-link` | `/link/create` → `{orderId, linkId, shortUrl, longUrl, ...}` |
| POST | `/paytm/link-transactions` | reconcile via `/link/fetchTransaction` → `{linkId, orders: [...]}` (use this for Payment Link flows, NOT `/v3/order/status`) |
| POST | `/paytm/create-qr` | `/paymentservices/qr/create` → `{orderId, qrCodeId, qrData, image, mid}` |
| POST | `/paytm/order-status` | server-side Transaction Status API |
| GET\|POST | `/paytm/callback` | Paytm browser redirect; verifies CHECKSUMHASH |

Demo pages (one per product, all under `/paytm-backend/`):
- `/checkout.html` - one-time payment via JS Checkout
- `/subscription.html` - UPI Autopay subscription
- `/payment-link.html` - generate shareable payment link
- `/qr.html` - dynamic QR with auto-polling

All HTML files use `new URL(..., document.baseURI)` so they work regardless of the WAR context path.

