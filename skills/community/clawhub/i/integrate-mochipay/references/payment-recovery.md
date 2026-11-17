# Independent payment creation — WEB82.7

merchant_order_id is a repeatable merchant label. Every new explicit checkout is independent:123,124,124 produces three system orders. Give each attempt a new request_id and token, and persist its unchanged payload before transport. An earlier unpaid or uncertain attempt never blocks a new checkout. Viewing an existing link, changing ON_SITE/HPP presentation, or querying status continues that link's exact invoice.

Only the same saved request_id/payload identify a transport retry. Query order_id once saved, or request_id after an uncertain response. An authenticated404 ORDER_NOT_FOUND with request-id-v1 permits replay only of the original saved request. Never recover using merchant_order_id: duplicate references return409 MERCHANT_ORDER_ID_AMBIGUOUS. Without request_id every Create is independent.

The merchant reported Zen Cart acceptance. WEB82.7 extends the policy to the other seventeen native packages, WooCommerce's separate WordPress.org distribution, MCP1.0.4, Chrome1.0.4, PHP1.2.0, report1.0.8, four backend demos1.0.5 and Swift/Kotlin1.0.2. These have offline fixture validation, not real native-store/mobile acceptance. Each native branch retains its original install structure and language/PHP requirements.

HPP offers Cancel and return to merchant when a saved return destination exists. The destination is stored merchant data, never a browser-supplied redirect. Cancel returns only; it does not cancel the on-chain invoice or mark it paid. Classic SaaS prefers its saved cancel_return_url for a pending return. Keep callback and polling verification active.

No historical-order migration is included in this pre-launch rollout. Preserve credentials, settings, exact amount precision, signed verification and atomic once-only fulfillment. Authenticated PAID plus exact received_amount==pay_amount remains required. Native tables are created automatically; upgrade in place, never uninstall to upgrade. Monitor15 and DB21 are unchanged; rebuild WEB1.0.82.7. Keep SSL peer verification enabled and host verification2; configure a trusted CA bundle for certificate failures.
