## Description: <br>
The Agent Procurement Playbook helps developers build autonomous purchasing agents with spending controls, vendor evaluation, escrow protection, and multi-protocol buying across UCP, ACP, and A2A marketplaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this guide to design autonomous procurement workflows with policy checks, vendor evaluation, payment routing, escrow, reconciliation, and audit trails. It is a non-executing playbook with Python examples for GreenHelix-based purchasing agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copyable examples can initiate real payments and may not consistently enforce the promised spending controls. <br>
Mitigation: Run examples only in sandbox until every purchase path has a mandatory approval wrapper, hard budgets, vendor allowlists, and tests proving threshold purchases cannot execute without human approval. <br>
Risk: The guide references payment, wallet, Stripe, and GreenHelix credentials. <br>
Mitigation: Use scoped test credentials, avoid production wallet or payment keys during evaluation, and store required environment variables in the agent platform's secret manager. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mirni/greenhelix-agent-procurement-playbook) <br>
- [Publisher profile](https://clawhub.ai/user/mirni) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API endpoint](https://api.greenhelix.net/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guide with Python code examples and configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executing guide; examples reference GREENHELIX_API_KEY, WALLET_ADDRESS, and STRIPE_API_KEY.] <br>

## Skill Version(s): <br>
1.3.1 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
