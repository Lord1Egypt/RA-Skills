## Description: <br>
Paystack connector skill that guides an agent to inspect live schemas and run OOMOL oo CLI actions for Paystack customer and transaction workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent work with Paystack customers and transactions through an OOMOL-connected account. It supports listing and fetching records, creating and updating customers, initializing transactions, and verifying transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a connected Paystack account through OOMOL and may touch sensitive payment-account workflows. <br>
Mitigation: Install only for users who are comfortable granting agent access to the connected Paystack account, and confirm the exact account context before running actions. <br>
Risk: Customer changes and transaction initialization can have business or payment effects. <br>
Mitigation: Confirm exact payloads and expected effects with the user before customer writes or transaction initialization. <br>
Risk: The skill relies on live connector schemas and connected credentials. <br>
Mitigation: Run oo connector schema for the selected action before constructing payloads, and stop for user setup only when auth, connection, scope, credential, app readiness, or billing errors occur. <br>


## Reference(s): <br>
- [ClawHub Paystack skill page](https://clawhub.ai/oomol/oo-paystack) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Paystack homepage](https://paystack.com) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses oo connector schema before action execution and returns connector data with an execution ID when actions run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
