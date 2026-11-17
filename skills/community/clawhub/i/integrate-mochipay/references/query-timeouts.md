# Current WEB82.27 / Monitor32 / DB25

MCP1.0.6 preserves bounded Retry-After, cooldown and safe error_id. Payment differences require explicit authenticated manual acceptance after saved-binding, PAID and positive-amount checks. Automatic amount tolerance is removed. REVIEW_REQUIRED stays unpaid. See README_WEB82_25.md for deployment. Historical timing notes below do not replace current scoped read budgets.

# Query timeouts and recovery — WEB82.4

All payment API connections and requests allow at least 30 seconds. Native buyer AJAX allows 40 seconds. The website business SQL connection allows at least 30 seconds and existing commands allow 60 seconds; website payment/subscription polling allows 100 seconds so the database operation has time to finish. Only one browser poll may be in flight. Low-budget optional telemetry/geolocation checks keep their existing budgets.

A transient transport timeout, disconnection, HTTP408/429/5xx is retried against the original saved invoice. The first two consecutive failed polls are quiet; the third displays an existing localized friendly connection message. Polling continues at a capped60-second interval. A successful verified query clears the failure count. Authorization, ownership, invalid response and payment binding failures are immediate and never disguised as a network timeout. Terminal/underpaid/overpaid/review states preserve the payment verification rules.

MCP performs at most three identical read-only GET attempts, each with a30-second socket deadline, then returns an honest unavailable result; configure the AI host tool deadline to at least120 seconds. Chrome requests allow30 seconds; order refresh counts consecutive transient failures across refresh/alarm cycles and QR download makes at most three read-only attempts. The popup permits130 seconds for a queued QR request. Uncertain create payloads stay saved. No automatic POST replay is introduced by this transport patch.

Never generate a new purchase reference, clear mappings or mark payment paid because a query timed out. Fulfillment still requires authenticated, financially bound PAID with exact received_amount==pay_amount. TLS verification and redirect restrictions stay enabled. For a genuinely new purchase, use an independent purchase reference as documented in PAYMENT_RECOVERY.md.

Upgrade modules in place; preserve gateway settings/private credentials/order mappings. Compile and deploy website assembly1.0.82.4 and changed website pages. Rebuild Monitor15 as1.8.0.1: chain-provider request/read budgets default to30 seconds and clamp to30–120 seconds. Keep existing cooldowns/scan cursors and operational error logs. Deploy the referenced WEB1.0.82.4 DLL alongside Monitor. DB21 has no SQL update in this patch. This bundle is source code; no Windows/.NET build, live store installation or real-payment acceptance is claimed.
