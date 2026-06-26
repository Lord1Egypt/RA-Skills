## Description: <br>
This skill provides complete QFPay API integration guidelines, including environment configuration, request formats, signature generation, payment types, supported currencies, and status codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xingstudy](https://clawhub.ai/user/xingstudy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and payment integration engineers use this skill to configure QFPay environments, generate request signatures, and implement Hong Kong payment, query, and refund flows. <br>

### Deployment Geography for Use: <br>
Hong Kong <br>

## Known Risks and Mitigations: <br>
Risk: QFPay credentials and merchant keys could be exposed through source control, shared terminals, logs, or chat. <br>
Mitigation: Keep QFPAY_KEY, QFPAY_APPCODE, and merchant credentials in secured environment variables or secret stores, and avoid echoing them in logs or generated examples. <br>
Risk: Production payment or refund examples could initiate real financial activity if used with live credentials. <br>
Mitigation: Start with sandbox or test credentials and require explicit user approval before creating, refunding, or querying production transactions. <br>
Risk: Incorrect environment, merchant ID, amount, or signature handling can cause authorization failures, duplicate transactions, or failed refunds. <br>
Mitigation: Validate endpoint selection, unique order IDs, amount units, signature inputs, and refund support before submitting payment or refund requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xingstudy/hongkong-payment-qfpay) <br>
- [QFPay Developer Center](https://sdk.qfapi.com) <br>
- [Payment Integration Guides](https://sdk.qfapi.com/docs/category/integration-by-payment-type) <br>
- [Checkout Integration](https://sdk.qfapi.com/docs/category/checkout-integration) <br>
- [QFPay Postman Collection](https://sdk.qfapi.com/assets/files/qfpay_openapi_payment_request.postman_collection-c8de8c8fe69f3fcd5a7653d41c289a29.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code examples, shell commands, tables, and API request details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for QFPay integration; no hidden execution behavior identified by the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
