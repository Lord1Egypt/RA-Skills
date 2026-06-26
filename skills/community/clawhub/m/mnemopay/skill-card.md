## Description: <br>
MnemoPay helps agents use governed memory, payments, reputation, identity, approvals, audit evidence, and durable jobs for consequential workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[t49qnsx7qt-kpanks](https://clawhub.ai/user/t49qnsx7qt-kpanks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Use when an agent needs persistent memory, scoped authority, budgets, approvals, payment rails, identity, reputation, or verifiable evidence for high-impact actions. <br>

### Deployment Geography for Use: <br>
Not specified in the supplied evidence. <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence identifies payment, identity, memory, and durable job capabilities as high-impact agent powers. <br>
Mitigation: Start with the default essentials tool group, keep admin/operator/all groups disabled unless authorized, and require explicit approvals for payments or other high-impact actions. <br>
Risk: Payment actions can move money or create financial obligations. <br>
Mitigation: Require an explicit amount, currency, recipient, and reason before initiating payment-related actions. <br>
Risk: Credential, invitation token, or worker secret exposure could compromise privileged systems. <br>
Mitigation: Do not return API keys, invitation tokens, worker credentials, or secrets in agent responses. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/t49qnsx7qt-kpanks/mnemopay) <br>
- [Publisher Profile](https://clawhub.ai/user/t49qnsx7qt-kpanks) <br>
- [Website listed in skill artifact](https://mnemopay.com) <br>
- [npm package listed in skill artifact](https://www.npmjs.com/package/@mnemopay/sdk) <br>
- [Python package listed in skill artifact](https://pypi.org/project/mnemopay/) <br>
- [Source link listed in skill artifact](https://github.com/mnemopay/mnemopay-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Agent-facing installation steps, MCP tool group guidance, safety rules, and operational guidance for MnemoPay integrations.] <br>
**Output Parameters:** [May depend on the user's requested workflow, install environment, MCP tool groups, payment amount, currency, recipient, reason, identity context, budget, approval policy, and credential scope.] <br>
**Other Properties Related to Output:** [The artifact says the essentials tool group is exposed by default and admin, operator, or all tool groups should remain disabled unless used by authorized operators with explicit credentials.] <br>

## Skill Version(s): <br>
1.2.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
