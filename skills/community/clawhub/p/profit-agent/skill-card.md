## Description: <br>
利润优化引擎 — 订单管理/计价/结算模拟。核心能力：(1) 订单管理 (2) 计价模型 (3) 成本追踪 (4) 利润计算 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freeman88-tch](https://clawhub.ai/user/freeman88-tch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to manage local order records, model pricing and costs, calculate profit margins, and generate simple profit reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Order, pricing, cost, and payment-status records are saved locally on the user's machine. <br>
Mitigation: Install only when local storage of these business records in the OpenClaw workspace state directory is acceptable. <br>
Risk: Payment confirmation is manual bookkeeping and does not verify an actual payment. <br>
Mitigation: Confirm payments through an external payment system before treating an order as paid. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freeman88-tch/profit-agent) <br>
- [Publisher profile](https://clawhub.ai/user/freeman88-tch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and local text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Order data is stored locally in the OpenClaw workspace state directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
