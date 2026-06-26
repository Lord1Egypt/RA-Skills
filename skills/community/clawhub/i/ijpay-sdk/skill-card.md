## Description: <br>
Helps agents integrate IJPay-based payment flows for Alipay, WeChat Pay, QQ Wallet, UnionPay, JD Pay, and PayPal in Spring Boot applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add payment dependencies, configuration, order creation endpoints, callback handling, and reconciliation guidance for IJPay-supported providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment callback or refund examples could be copied into production without enough validation. <br>
Mitigation: Require provider signature verification, merchant/order/amount checks, durable idempotency, and authenticated authorization for refund or close operations before deployment. <br>
Risk: Payment secrets, private keys, certificates, or raw callback data could be exposed through configuration or logs. <br>
Mitigation: Store secrets and certificates in protected secret management, inject them at runtime, and redact sensitive payment data from logs. <br>
Risk: Provider behavior, API requirements, or IJPay usage details may differ from the examples. <br>
Mitigation: Cross-check every flow against official payment-provider documentation and current IJPay documentation before accepting real payments. <br>


## Reference(s): <br>
- [IJPay SDK ClawHub page](https://clawhub.ai/zmy1006-sudo/ijpay-sdk) <br>
- [IJPay complete guide](references/ijpay-guide.md) <br>
- [Alipay integration guide](references/alipay-guide.md) <br>
- [WeChat Pay integration guide](references/wxpay-guide.md) <br>
- [Payment callback handling guide](references/callback-handler.md) <br>
- [IJPay GitHub repository](https://github.com/javen205/IJPay) <br>
- [IJPay Gitee repository](https://gitee.com/javen205/IJPay) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with Java, YAML, XML, SQL, and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Payment-provider examples require review against official provider and IJPay documentation before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
