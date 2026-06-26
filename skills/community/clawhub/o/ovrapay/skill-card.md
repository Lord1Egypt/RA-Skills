## Description: <br>
Enables AI agents to complete online purchases, handle payment-required flows, manage payment records, and use tokenized credentials without exposing real card data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ovra](https://clawhub.ai/user/ovra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent complete approved online purchases, handle HTTP 402 payments, manage virtual cards, enforce spending policy, and keep transaction records. <br>

### Deployment Geography for Use: <br>
Global; the skill claims EU (Germany) data residency. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate real-money payment and account-management actions. <br>
Mitigation: Use sandbox or restricted keys first, enforce spending policy, and require explicit user confirmation before any real purchase. <br>
Risk: Payment intent, merchant, amount, transaction, and receipt data is sent to Ovra. <br>
Mitigation: Install only if you trust Ovra with that data and upload only receipts or invoices from the current transaction. <br>
Risk: Sensitive card, token, agent, policy, and GDPR actions require strong backend approval controls. <br>
Mitigation: Verify that the Ovra backend enforces approval and authorization for those actions before production use. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/ovra/ovrapay) <br>
- [Ovra website](https://getovra.com) <br>
- [Ovra documentation](https://docs.getovra.com) <br>
- [Ovra MCP endpoint](https://api.getovra.com/api/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, API Calls, JSON] <br>
**Output Format:** [Markdown instructions with JSON tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OVRA_API_KEY and an MCP connection to https://api.getovra.com/api/mcp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; skill metadata reports 2.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
