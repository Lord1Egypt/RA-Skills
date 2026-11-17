# Backend and mobile selection

Read the pinned downloads in developer-examples.json; full guide: https://mochi.bz/Developers/Reference.aspx#code-examples. Keep the merchant's existing stack. PHP supports7.0–8.4; Node22+, Python3.10+, .NETFramework4.6.1/VS2019 and Java17+ have independent packages. Swift/iOS15+ and Kotlin/AndroidAPI26+ are separate native source demos, not payment SDKs. Do not offer HarmonyOS/Flutter support that has not been implemented.

## Backend implementation

Choose ON_SITE by default; HPP is also available, using the same order. The four new backends expose POST /payments (staging bearer token, body request_id/payment_method), GET /checkout?r=...&t=...&mode=ON_SITE|HPP&lang=en, GET /status?r=...&t=..., POST /callback?r=...&t=..., and GET /complete?r=...&t=.... The backend owns price/currency/method validation and private API credentials. The response provides a merchant-local checkout_url, not full upstream data. The original PHP package intentionally retains order.php/checkout.php/callback.php routes; do not promise drop-in mobile compatibility with those routes.

Use the package's README and TESTING.md. Copy the entire assets directory including the QR license. Each new backend atomically stores a payload/token before creation and permits one process per private data directory. Replace the staged file store, capability ownership and shared staging bearer credential with the application database/user session/rate-limits before production. Do not create another service/table in MochiPay itself merely to demonstrate a merchant integration.

## Mobile implementation

Select the existing Swift or Kotlin source project. Set only the merchant HTTPS backend origin in the app. Keep API key/secret exclusively on that backend. Treat the independent staging access token as demo-only and replace it with the merchant app's real account session. Retain request_id and original method across retries/restarts; mode/language changes do not change the order. Protect saved capability URLs; never log them. Validate returned checkout URLs against the configured origin and /checkout path.

ON_SITE opens the merchant-local payment dialog in WKWebView/AndroidWebView. Restrict navigation to the merchant HTTPS origin and do not install a JavaScript/native success bridge. HPP opens the merchant redirect route in the external browser. On app foreground or explicit refresh, query the merchant backend; never infer payment from browser return. Active polls are15 seconds, not a background mobile job. Backend notification verification continues if the app closes.

Check current official App Store/Google Play billing policies for the product and target region. Do not claim app-store approval or compatibility with restricted digital purchases. Report native build/device/live-payment tests as unverified unless actually run. Package source review does not substitute for Xcode/AndroidStudio acceptance.
