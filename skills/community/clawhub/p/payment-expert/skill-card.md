## Description:

粤收付交易集成：用于聚合支付、托管支付、checkout-js、下单、查单、关单、退款、对账、支付通知、签名验签、请求头、幂等、交易终态、本地沙箱和支付上线；不用于企业/个人商户进件、图片上传、商户业务开通、商户详情或申请状态查询，这些任务使用 huifu-merchant-onboarding。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huanglin88](https://clawhub.ai/user/huanglin88)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical operations teams, and merchant integration staff use this skill to integrate and troubleshoot CNYepay payment APIs across PHP, Java, Python, Go, and Node.js. It supports payment order creation, queries, closing orders, refunds, reconciliation, callbacks, RSA2 signing, idempotency, sandbox validation, and production readiness checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated payment, refund, transfer, withdrawal, or profit-sharing code may move funds or alter transaction state if used without review.

Mitigation: Review generated code, enforce merchant-side authorization, test in the CNYepay sandbox, and require approval before production deployment.

Risk: Callback, refund, transfer, or withdrawal handling can create duplicate or incorrect processing if terminal states and retries are not handled idempotently.

Mitigation: Use idempotency keys, verify platform signatures, reconcile amounts and order identifiers, and treat callbacks and query results as the basis for final state.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/huanglin88/payment-expert/tree/main/skills/cnyepay)
- [ClawHub skill page](https://clawhub.ai/huanglin88/skills/payment-expert)
- [Publisher profile](https://clawhub.ai/user/huanglin88)
- [CNYepay API documentation](https://open.cnyepay.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code snippets and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include language-specific examples, request parameters, signing steps, webhook handling notes, and troubleshooting guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
