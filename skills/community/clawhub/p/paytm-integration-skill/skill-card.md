## Description: <br>
Expert guide for integrating Paytm Payment Gateway APIs and SDKs into websites, mobile apps, and backend systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ankit1goel-paytmpayments](https://clawhub.ai/user/ankit1goel-paytmpayments) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and merchants use this skill to build Paytm payment flows for web, mobile, and backend systems, including JS Checkout, payment links, dynamic QR codes, subscriptions, callbacks, and payment-status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles real payment credentials and customer payment data. <br>
Mitigation: Use staging first and complete careful production review before connecting live Paytm credentials or customer traffic. <br>
Risk: PAYTM_MERCHANT_KEY exposure can compromise payment signing. <br>
Mitigation: Keep the merchant key only in server-side, secret-managed configuration and never expose it to client-side code. <br>
Risk: Sample services may be insufficient for production traffic controls. <br>
Mitigation: Add authentication, rate limits, strict CORS, durable idempotency, and minimal webhook logging before production deployment. <br>
Risk: Payment-link status can be misread if reconciliation uses the wrong endpoint. <br>
Mitigation: Verify payment-link reconciliation against /link/fetchTransaction. <br>


## Reference(s): <br>
- [Paytm Web Integration Reference](artifact/references/js-checkout.md) <br>
- [Paytm Payment Links](artifact/references/payment-links.md) <br>
- [Paytm QR Codes](artifact/references/qr-codes.md) <br>
- [Paytm Subscriptions / UPI Autopay](artifact/references/subscriptions.md) <br>
- [Paytm PG Troubleshooting](artifact/references/troubleshooting.md) <br>
- [Paytm Developer Docs](https://www.paytmpayments.com/docs/) <br>
- [Paytm Checksum Library](https://www.paytmpayments.com/docs/checksum/) <br>
- [Paytm Server SDK](https://www.paytmpayments.com/docs/server-sdk/) <br>
- [Paytm Payments GitHub](https://github.com/Paytm-Payments) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code blocks, configuration snippets, and sample implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include language-specific backend and frontend examples for Node.js, Python, Java Spring, and browser-based checkout flows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
