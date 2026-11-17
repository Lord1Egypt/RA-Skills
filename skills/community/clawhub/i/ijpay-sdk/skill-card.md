## Description:

Guides developers through IJPay-based integrations for WeChat Pay, Alipay, QQ Wallet, UnionPay, JDPay, PayPal, and related payment callback workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add online payment support to Java or Spring Boot applications with IJPay. It provides integration guidance, provider-specific configuration, code examples, callback handling patterns, and operational checklists for common payment channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment callbacks may update order state or customer records incorrectly if notifications are not verified and handled idempotently.

Mitigation: Verify every provider callback before state changes, use idempotent order updates, and test callback flows with sandbox accounts before production use.

Risk: Payment keys, certificates, and raw callback payloads may expose customer or merchant data if stored or logged carelessly.

Mitigation: Keep secrets out of source control, load credentials from protected runtime configuration, and avoid logging full raw payment payloads.

Risk: Refund and order-close examples can affect money movement if exposed without strong access control.

Mitigation: Protect refund and close endpoints with strong authorization, server-side amount derivation, and audit logging.

Risk: Copyable examples may need production hardening before handling real payments.

Mitigation: Review the generated implementation carefully, validate amounts and order status against server-side records, and complete sandbox testing for each payment provider.

## Reference(s):

- [IJPay Complete Reference Guide](references/ijpay-guide.md)
- [Alipay Integration Guide](references/alipay-guide.md)
- [WeChat Pay Integration Guide](references/wxpay-guide.md)
- [Payment Callback Handling Guide](references/callback-handler.md)
- [IJPay GitHub Repository](https://github.com/javen205/IJPay)
- [IJPay Gitee Repository](https://gitee.com/javen205/IJPay)
- [IJPay Spring Boot Demo](https://github.com/Javen205/IJPay-Demo-SpringBoot)
- [IJPay JFinal Demo](https://github.com/Javen205/IJPay-Demo-JFinal)
- [IJPay Solon Demo](https://github.com/Javen205/IJPay-Demo-Solon)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with Java, YAML, XML, SQL, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include payment-provider setup checklists, callback safety guidance, and integration decision paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
