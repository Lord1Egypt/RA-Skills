## Description:

Expert guide for integrating Paytm Payment Gateway APIs and SDKs into websites, mobile apps, and backend systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ankit1goel-paytmpayments](https://clawhub.ai/user/ankit1goel-paytmpayments)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate Paytm Payment Gateway integrations for JS Checkout, subscriptions, payment links, dynamic QR codes, callbacks, webhooks, and transaction-status verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sample backends can expose live merchant payment authority if deployed as-is.

Mitigation: Treat included servers as demos unless hardened with authentication, authorization, ownership checks, rate limits, request-size limits, strict CORS, and callback URL allowlists before using live credentials.

Risk: Payment flows can expose customer contact or transaction data through broad responses or unclear notices.

Mitigation: Return only minimal response fields and provide clear privacy and notification notices for customer contact data.

Risk: Reference idempotency implementations are demo-oriented and may not be sufficient for production retries.

Mitigation: Replace in-memory idempotency storage with a production datastore such as Redis or a database before production use.

## Reference(s):

- [Paytm Web Integration Reference](references/js-checkout.md)
- [Paytm Subscriptions / UPI Autopay](references/subscriptions.md)
- [Paytm Payment Links](references/payment-links.md)
- [Paytm QR Codes](references/qr-codes.md)
- [Paytm PG Troubleshooting](references/troubleshooting.md)
- [Paytm Developer Docs](https://www.paytmpayments.com/docs/)
- [Paytm Checksum Library](https://www.paytmpayments.com/docs/checksum/)
- [Paytm Server SDK](https://www.paytmpayments.com/docs/server-sdk/)
- [Paytm JS Checkout](https://www.paytmpayments.com/docs/jscheckout/)
- [Paytm Initiate Transaction API](https://www.paytmpayments.com/docs/api/initiate-transaction-api)
- [Paytm Dashboard](https://dashboard.paytmpayments.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, configuration examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate example frontend and backend integration code for Node.js, Python, Spring Boot, Spring MVC, and static HTML.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
