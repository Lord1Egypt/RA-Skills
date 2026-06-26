## Description: <br>
拉卡拉MOSS统一接口功能演示，创建测试订单并生成演示链接，用于流程体验与功能验证。 <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[mars9043](https://clawhub.ai/user/mars9043) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and integrators use this skill to exercise a Lakala MOSS test order flow, create non-production payment-style orders, and inspect the returned demo link and order details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates payment-style orders through an external API endpoint. <br>
Mitigation: Use only the disclosed non-production test flow and test order data; do not use real merchant credentials, real customer information, or real payment scenarios. <br>
Risk: A callback URL may receive transaction test callbacks. <br>
Mitigation: Provide only callback URLs you control and expect to receive Lakala MOSS test callbacks. <br>
Risk: Generated links may be mistaken for production payment links. <br>
Mitigation: Treat returned links and order details as demonstration artifacts with no real payment effect. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mars9043/lakala-moss) <br>
- [mars9043 Publisher Profile](https://clawhub.ai/user/mars9043) <br>
- [拉卡拉MOSS支付API指南](references/moss-api-guide.md) <br>
- [Lakala MOSS unified order API](https://moss.lakala.com/ord-api/unified/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, Python usage examples, shell commands, and JSON-like API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates test orders through an external Lakala MOSS API and reports success, error details, order metadata, and a demo payment link.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
