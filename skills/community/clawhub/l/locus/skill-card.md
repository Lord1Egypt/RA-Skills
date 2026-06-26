## Description: <br>
Locus provides payment tools for agents to send crypto payments, check wallet balances, list tokens, approve token spending, and process payment-related emails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cdermott7](https://clawhub.ai/user/cdermott7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use Locus to connect an agent to a wallet-backed payment service for balance checks, token management, payment approvals, and payment execution after explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores wallet-authorized credentials for a payment service. <br>
Mitigation: Use a least-privilege Locus API key with spending limits and know how to revoke the key or remove the mcporter Locus configuration. <br>
Risk: The skill gives the agent broad dynamic access to payment tools. <br>
Mitigation: Discover available tools before use, confirm every payment or token approval manually, and avoid unlimited allowances. <br>
Risk: Incorrect recipients, spender addresses, payment amounts, or token approvals can cause financial loss. <br>
Mitigation: Verify recipient and spender addresses, token, amount, and memo with the user before executing any wallet action. <br>


## Reference(s): <br>
- [Locus ClawHub listing](https://clawhub.ai/cdermott7/locus) <br>
- [Locus website](https://paywithlocus.com) <br>
- [Locus app](https://app.paywithlocus.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes payment summaries and confirmation prompts before wallet actions.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
