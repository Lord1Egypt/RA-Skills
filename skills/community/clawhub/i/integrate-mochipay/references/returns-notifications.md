# HPP returns and ON_SITE/HPP asynchronous processing

Full reference: https://mochi.bz/Developers/Reference.aspx#returns-notifications. Distinguish the three entry points and use the same verified update routine.

| Entry | Transport | Purpose |
|---|---|---|
| redirect_url | Browser GET after HPP | Display verified result; browser may never return |
| notify_url | MochiPay server POST for either mode | Query and atomically update local order, even with no browser/app |
| ON_SITE polling | Browser/app GET to merchant backend | Display a minimal DTO from signed Query Order |

Never call a browser redirect a signed callback. Verify every entry with the saved binding and authenticated query. For a notification, treat its body/order_id as untrusted lookup hints, not proof. A saved URL capability authorizes lookup but does not prove payment. Compare MochiPay ID, merchant reference, original amount/currency, method reconstructed from wallet_type/network, address and exact payable amount. Require PAID and exact received_amount == pay_amount. Reject mismatches; retain UNDERPAID/OVERPAID/EXPIRED for review. Do not echo customer/credential fields.

In the new backend demos, create() builds notify_url=/callback?r=...&t=... and redirect_url=/complete?r=...&t=.... verify() (C#:Verify) queries the saved order_id and applies the same comparisons. POST /callback writes the paid_verified flag atomically once, returns200 OK for verified PAID, and409 for an unconfirmed/review state; upstream/storage unavailability must not be acknowledged as success. /complete and /status reuse verification, so a missing notification can be reconciled. Polling is not the only business update path. In production commit the paid state and fulfillment marker atomically in the existing database, then queue any external side effect safely. Duplicate notifications must return success without duplicate delivery/credit.

The PHP demo uses callback.php POST for notify_url and GET for redirect_url, and order.php polling. New1.1.4 attempts add stable request_id and a return capability, while legacy saved attempts retain query-first recovery. mochipay_record_verified() records the same once-only paid marker under a file lock. Replace the TODO with the merchant application's transaction; do not label the staging marker as real fulfillment.

HPP browser returns may precede confirmations or fail to occur. Display waiting and let verified asynchronous updates/polls resolve it. ON_SITE popup closure does not cancel an order or notifications. A delayed callback does not authorize creating another payment or rounding the exact amount. Do not alter MochiPay's existing API or require native-plugin customers to upgrade for documentation/demo changes.

## Saved HPP cancel destination (WEB82.7)

The HPP page exposes a cancel/merchant-return link only for a validated saved HTTP(S) destination. Pending Classic SaaS uses cancel_return_url when present; a paid return uses redirect_url. A cancellation marker is navigation context, never proof of an order state. Bind every returned token/system ID to the original attempt, including older links for a repeated merchant order. Queries and authenticated callbacks continue verifying the exact saved invoice.


## Authenticated manual payment acceptance (WEB82.18)
A received amount must be valid and positive. Preserve all original invoice bindings and require PAID from an authenticated server query. Accept a received/payable mismatch only when that authenticated query contains the Boolean manual_payment_accepted=true, backed by the server audit. A notification/browser field, string "true", number 1, or PAID alone cannot authorize it. Require WEB82.14+ for this proof; exact paid amounts retain older-server compatibility. Manual callback retries must retain atomic once-only fulfillment.
