# Current checkout and API presentation contract

Presentation inventory reviewed: 2026-10-20, WEB82.102. Earlier release notes below retain their original scope.

- Native plugins and custom API backends use one saved order for ON_SITE and HPP. Subscription checkout shares its presentation. DEMO uses non-payable example data.
- Compact warm-orange QR-first design. The QR retains a small centered asset icon. Label the fields Network, Receiving address, Exact payment amount. Do not enlarge the asset SVG through a descendant-wide QR selector.
- Copy buttons display a localized Copied tooltip and the same transient field-border feedback for address and amount. Clipboard failures show a manual-copy message. Copy the full address or numeric amount only, preserving exact digits. Wrap long BTC addresses rather than shortening the payable value.
- When expired, retain and mask the QR and receiving-address region and disable their copy controls. Poll/query the original attempt; do not create a replacement invoice from a display transition.
- Create/query responses retain legacy expires_at and add expires_at_utc and server_time_utc ISO8601 UTC strings. Use the saved expiry minus server time, advanced by elapsed time. Do not reset to60 minutes on a refresh or reopen. Existing historical orders retain their deadlines. Prefer UTC fields; treat legacy timestamps according to the documented server contract.
- Hosted ASP.NET heads must not contain direct inline output blocks if SiteLanguage adds controls at PreRenderComplete. Use application-relative runat=server links.
- Browser UI and copy/QR events never authorize delivery. Preserve authenticated query, immutable bindings, positive received amount, exact equality or strict Boolean audited manual_payment_accepted, and atomic once-only fulfillment. No automatic payment tolerance.
- API documentation: https://mochi.bz/Developers/Reference.aspx
- Interactive demo: https://mochi.bz/CheckoutDemo.aspx

Hosted and subscription checkout on WEB82.77 calibrate saved UTC payment deadlines against server time. Device wall-clock changes must not reset a payment to 60 minutes or expire it early. Deploy the matching page, script and WEB assembly together; source availability does not prove a merchant deployment is current.


## Merchant sandbox mode

The merchant selects sandbox or live mode in the MochiPay dashboard; the existing API key, secret, query contract and notification contract stay the same. Sandbox orders use non-payable placeholder addresses and demonstration QR codes. Do not send real funds to them or require a live blockchain receipt to exercise the sandbox flow.

Use the official HPP or current native ON_SITE simulation controls to request success or failure. A local button click alone does not prove payment: run the existing authenticated query, saved-order binding and once-only fulfillment checks. A successful sandbox test can trigger the merchant application's normal fulfillment or subscription logic; test with appropriate internal orders.

WooCommerce 1.5.24 includes the sandbox destination fix and responsive simulation controls. Cross-origin ON_SITE simulation also requires the WEB82.102 scoped SandboxSimulate.aspx OPTIONS handler configuration on the MochiPay server. Updating the store plugin alone cannot repair a server that omits the CORS preflight headers. Preserve HTTPS destination checks and the normal live-payment path.
