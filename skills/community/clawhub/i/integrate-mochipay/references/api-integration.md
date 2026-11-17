# MochiPay API integration contract

Snapshot: 2026-10-17, WEB82.76. Authoritative reference: https://mochi.bz/Developers/Reference.aspx. Keep setup documentation in English and preserve the merchant application's stack.

## Authentication and money

POST https://mochi.bz/api/v1/orders/create sends UTF-8 JSON, Content-Type application/json, X-Mochi-Key and X-Mochi-Signature. Sign the exact body bytes and send those same bytes. Signature is Base64 of raw HMAC-SHA256 with the merchant API secret. GET /api/v1/orders/query signs the exact encoded query string without its question mark. API secrets stay on the merchant backend. Verify TLS certificates and hostnames; do not follow redirects carrying authenticated requests.

Use exact decimal strings, never binary floats. Required create fields include merchant_order_id, positive amount, currency and payment_method. Supported methods are USDT_TRC20, USDC_ERC20, BTC_BITCOIN, ETH_ERC20, SOL_SOLANA and TRX_TRON. Native TRX and USDT/TRC20 are different assets. Enable only configured active receiving wallets/rates. unique_amount_direction is UP or DOWN (default UP). Optional notify_url and redirect_url are merchant HTTPS endpoints. Do not invent payment_mode or a signed language field.

## Independent attempts and recovery

merchant_order_id is a repeatable business label, not an idempotency key. Each explicit new checkout gets a fresh request_id, even for the same reference/amount/customer. Persist that ID and exact payload before requesting creation. Only the same request_id plus unchanged payload represent a transport retry. Do not retrofit IDs onto historical attempts.

WEB82.6+ advertises request-id-v1. request_id accepts1-64 ASCII letters/digits or . _ : -. Repeated unchanged requests recover their saved order. REQUEST_ID_CONFLICT, REQUEST_IN_PROGRESS (Retry-After) and REQUEST_ORDER_UNAVAILABLE need explicit recovery handling. An uncertain response must not trigger a new attempt silently.

Query accepts exactly one of order_id, request_id or merchant_order_id. Prefer the saved order_id; use request_id to recover an uncertain creation. Repeated merchant references can produce MERCHANT_ORDER_ID_AMBIGUOUS; never choose an arbitrary/latest invoice. Check success, HTTP status and response schema. HTTP200 alone is insufficient. API errors have success:false and message.

## Response and checkout

Create returns order_id, merchant_order_id, status, amount, currency, base_pay_amount, unique_amount_delta/direction, pay_amount, payment_method, payment_address, payment_url and expires_at. Query includes wallet_type, network, received_amount and transaction/confirmation fields; construct the method from wallet_type + '_' + network where needed. Expose only a minimal authorized browser DTO, never the complete customer record or credentials.

Both responses now add expires_at_utc and server_time_utc ISO8601 UTC strings alongside legacy expires_at. Use the saved expiry and server time plus elapsed time for countdowns. Reopening/polling must not reset the invoice to60minutes. Do not parse legacy offset-free dates as browser local time. See checkout-current.md for QR, copy confirmation and expiration masks.

ON_SITE and HPP present the same saved order. Keep checkout_mode in local merchant config. ON_SITE displays the exact saved pay_amount, asset/network, address and QR. HPP validates HTTPS, the configured MochiPay origin and exact /pay/<saved-order-id> path, with no URL credentials or unexpected port, then redirects303. Switching presentation must not create another invoice.

## Returns, callbacks and fulfillment

Browser returns and incoming notifications only trigger an authenticated server query. Bind results to the original order ID, reference, original amount/currency, method/network and address. Require PAID, positive received_amount, and exact decimal equality with pay_amount. A mismatch is allowed only with strict Boolean manual_payment_accepted=true from the authenticated query after audited authorized acceptance. String true, number1, callback/browser fields or PAID alone do not authorize it. REVIEW_REQUIRED, UNDERPAID, OVERPAID, EXPIRED and inconsistent bindings never authorize delivery. No automatic payment tolerance.

Fulfill atomically once using the merchant application's transaction and uniqueness safeguards. A closed browser must not stop asynchronous verification. Keep redirect_url separate from notify_url. Reuse that same verification routine for callbacks, synchronous returns and status polling. Use at least30-second server transport deadlines and quiet retries for the first two transient query failures; show localized failure feedback after the third. Authorization/binding failures are immediate.

## Official resources

- PHP SDK: https://packagist.org/packages/mochipay/php-sdk (PHP7.4+, MIT client; service subscription separate).
- Backend/mobile demos: https://mochi.bz/Developers/Examples.aspx
- Store packages: store-packages.md and catalog.json.
- MCP1.0.7: local stdio server; payment-request/status tools, no wallet transfers or fulfillment.
- Chrome1.0.7: desktop ZIP manual installation; sharing QR opens HPP, separate from on-chain payment QR.

Test fixtures and merchant ownership/recovery/duplicate notification handling before deployment. Offline tests do not establish real payment or native-store acceptance.
