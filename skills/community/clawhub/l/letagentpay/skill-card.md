## Description: <br>
Spending guardrails for AI agents with budget limits, category restrictions, approval workflows, audit trails, and x402 crypto-micropayment authorization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maximberg](https://clawhub.ai/user/maximberg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route agent purchases and x402 crypto-micropayments through LetAgentPay policy checks before money is spent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables an agent to request or authorize real spending, including crypto micropayments. <br>
Mitigation: Use conservative budgets, require manual approval for larger purchases, and review the LetAgentPay audit trail before relying on the workflow. <br>
Risk: Payment credentials exposed directly to the agent could bypass the intended spending guardrails. <br>
Mitigation: Avoid exposing raw Stripe, PayPal, or payment keys to the agent; route spending through LetAgentPay instead. <br>
Risk: On-chain x402 payments can transfer value after authorization. <br>
Mitigation: Require x402_authorize before signing, confirm allowed chains and wallets, and report completed transactions with x402_report. <br>


## Reference(s): <br>
- [LetAgentPay](https://letagentpay.com) <br>
- [LetAgentPay Agent API Reference](https://letagentpay.com/developers) <br>
- [LetAgentPay MCP server docs](https://github.com/LetAgentPay/letagentpay-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, MCP tool calls] <br>
**Output Format:** [Markdown instructions with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LETAGENTPAY_TOKEN and the letagentpay-mcp MCP server; purchase authorization depends on configured LetAgentPay policy.] <br>

## Skill Version(s): <br>
1.2.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
