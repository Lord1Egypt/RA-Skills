## Description:

拉卡拉MOSS统一接口功能演示，创建测试订单并生成演示链接，用于流程体验与功能验证。

This skill is for demonstration purposes and not for production usage.

## Publisher:

[mars9043](https://clawhub.ai/user/mars9043)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and payment-integration testers use this skill to create Lakala MOSS test orders and inspect returned demo payment links and order details during API flow validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script sends order number, amount, subject, remark, and callback URL to Lakala's external MOSS endpoint.

Mitigation: Use only test order data and non-sensitive callback URLs unless the endpoint, merchant, and data-handling expectations have been independently approved.

Risk: The release describes the skill as test-only, but sandbox-only behavior and no-real-payment guarantees are not enforced in code.

Mitigation: Treat generated links as potentially payment-capable, confirm the merchant and endpoint are sandbox-only, and add sandbox enforcement and confirmation prompts before using production amounts or real merchant data.

## Reference(s):

- [拉卡拉MOSS支付API指南](references/moss-api-guide.md)
- [Lakala MOSS unified API endpoint](https://moss.lakala.com/ord-api/unified/v3)
- [ClawHub skill page](https://clawhub.ai/mars9043/skills/lakala-moss)
- [Publisher profile](https://clawhub.ai/user/mars9043)

## Skill Output:

**Output Type(s):** [Shell commands, Code, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated demo payment links, order numbers, amounts, service serial numbers, and full API responses.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
