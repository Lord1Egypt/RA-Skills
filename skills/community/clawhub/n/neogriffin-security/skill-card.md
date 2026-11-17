## Description:

NeoGriffin Security helps autonomous agents call a multi-chain security API for prompt injection scanning, token scam checks, transaction simulation, MEV detection, policy checks, cross-agent threat reporting, and wallet monitoring on Solana and Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cazaboock9](https://clawhub.ai/user/cazaboock9)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and autonomous-agent operators use this skill to add remote security checks before agents act on external prompts, token metadata, transactions, NFTs, wallet activity, or other on-chain inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent prompts, messages, wallet-related data, or on-chain security metadata may be sent to a third-party remote API.

Mitigation: Require explicit user approval for remote scans and redact secrets, credentials, seed phrases, private keys, personal data, and confidential business text before API calls.

Risk: Wallet monitoring, transaction simulation, paid endpoint use, and threat reporting can disclose sensitive wallet activity or incur payment.

Mitigation: Require explicit approval before wallet monitoring, transaction simulation, paid endpoint calls, and threat reports.

## Reference(s):

- [NeoGriffin API homepage](https://api.neogriffin.dev)
- [NeoGriffin Security on ClawHub](https://clawhub.ai/cazaboock9/skills/neogriffin-security)
- [Publisher profile](https://clawhub.ai/user/cazaboock9)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with HTTP endpoint descriptions, JSON request examples, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require NEOGRIFFIN_PAYMENT_WALLET and paid endpoint payment signatures for some API calls.]

## Skill Version(s):

2.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
