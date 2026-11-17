## Description:

This skill provides complete QFPay API integration guidelines including environment configuration, request formats, signature generation, payment types, supported currencies, and status codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xingstudy](https://clawhub.ai/user/xingstudy)

### License/Terms of Use:

MIT

## Use Case:

Developers and payment integration teams use this skill to configure QFPay OpenAPI environments, generate request signatures, understand payment and refund flows, and handle status codes for Hong Kong payment integrations.

### Deployment Geography for Use:

Hong Kong

## Known Risks and Mitigations:

Risk: Payment credentials, order IDs, logs, and production endpoints are sensitive and may be exposed if examples are copied into shared code or transcripts.

Mitigation: Store credentials in environment variables or a secrets manager, avoid logging secrets or full order details, and redact sensitive values before sharing outputs.

Risk: The skill includes live payment and refund flows that could move funds if production credentials and endpoints are used.

Mitigation: Use sandbox or test credentials for examples and require explicit human approval before any live payment or refund request.

Risk: Incorrect environment selection or mixed credentials can cause authorization or signature failures.

Mitigation: Confirm the selected QFPay environment, base URL, merchant ID, app code, and signing key before executing API calls.

## Reference(s):

- [QFPay Developer Center](https://sdk.qfapi.com)
- [Payment Integration Guides](https://sdk.qfapi.com/docs/category/integration-by-payment-type)
- [Checkout Integration](https://sdk.qfapi.com/docs/category/checkout-integration)
- [QFPay OpenAPI Payment Request Postman Collection](https://sdk.qfapi.com/assets/files/qfpay_openapi_payment_request.postman_collection-c8de8c8fe69f3fcd5a7653d41c289a29.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with API examples, tables, environment variable commands, and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include payment and refund examples; requires user-supplied QFPay credentials and explicit environment selection.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
