# Troubleshooting

Inspect sanitized evidence and authenticated queries. Never print credentials, recovery phrases, raw private configs or complete customer query responses.

| Symptom | Check and next action |
| --- | --- |
| Gateway absent | Correct branch/PHP, enabled setting, scope, currencies, cache/modification/compiler steps and theme hooks. |
| Invalid API key | Header name and private config source; merchant/whitespace. Do not print or rotate the key automatically. |
| Invalid signature | Base64 raw HMAC-SHA256; exact create bytes; encoded query without ?. Avoid BOM/newline/reserialization changes. |
| Create rejected | Actual HTTP status/message, subscription, merchant, wallet, method/network, precision and rate pair. |
| Create timeout | Preserve attempt; query/reconcile before retry. Merchant references are not server idempotency. |
| HPP URL rejected | Expected HTTPS origin and /pay/<saved-id>, order ownership; retain URL validation. |
| Waiting/underpaid | Actual network, address, exact payable amount and confirmations; screenshots are not payment evidence. |
| Dashboard paid, store pending | Callback HTTPS reachability/firewall/auth/routing, signed query, original binding, decimal checks, repeat-safe transition and sanitized logs. |
| Upgrade regression | Settings/order mappings preserved, no uninstall, refreshed core caches/compiler and retained HPP preference. |

Report concrete findings, fix and verification. Without live access, report live payment status unverified.


## Return, notification and mobile troubleshooting

A browser returning to redirect_url is not payment confirmation. Check the asynchronous notify_url separately; verify its public HTTPS reachability and that the saved URL matches the creation payload. Test browser-closed notifications and duplicate delivery. All paths must query the saved ID and compare exact received/payable amounts. For lost initial creation responses retain request_id and payload; interpret REQUEST_IN_PROGRESS/CONFLICT/ORDER_UNAVAILABLE before retrying. Never solve conflicts by generating a fresh request ID for the same uncertain purchase.

For Swift/Kotlin inspect the merchant backend URL, certificate chain, request ownership and common route contract before changing API credentials. HPP uses an external browser; ON_SITE uses merchant WebView with local popup. No incoming native/browser success message can unlock content. Report simulator/device/live acceptance separately from source/fixture results. See developer-examples.md and returns-notifications.md.

## Unpaid previous order and legacy recovery

New checkouts are independent even when merchant_order_id repeats. Use saved request_id for transport retry and order_id for status; merchant-reference recovery is retired in WEB82.6. The merchant accepted Zen Cart1.2.0; WEB82.7 extends its policy to the other native adapters, MCP, Chrome and demo packages.


## Zen Cart and invoice precision repairs (WEB82.5)

For null checkout products or a cleared order object, use the saved Zen Cart order and saved order products. Do not introduce a separate FEC hook unless the actual installation changes the payment-module lifecycle. Build standalone pay/return/callback links with Zen Cart zen_href_link sixth argument static=true and fifth argument search_engine_safe=false; main_page=mochipay_pay.php is not a standalone endpoint. Reject an incomplete saved attempt token rather than bypassing ownership checks.

INVALID_AMOUNT_PRECISION concerns the invoice currency, not the chosen payment asset or saved PayAmount. Converted fiat order totals use two decimal places by default; USDT/USDC invoices use six and BTC/ETH/SOL use eight under the bundled API defaults. Round only the store invoice conversion as an exact decimal string and use the same calculation during settlement. Never round blockchain payable amounts. Check customized MP_Currency.Decimals against the store currency configuration. Keep saved payloads and uncertain attempts unchanged; a wrong historical conversion needs manual review.

OpenCart adapters must use DB_PREFIX, send id plus MOCHIPAY_ATTEMPT_TOKEN for their HPP return, and verify the same saved payment on return. Browser navigation alone must not mark an order paid.

## WEB82.6 Zen Cart independent attempts

Bypass Zen queryCache for payment records and locks. Use one token per payment attempt in mochipay_attempt_v2; every explicit checkout creates anew. Keep exact invoice conversion, PAID/received checks and static endpoint URLs. No historical-order migration is included.
