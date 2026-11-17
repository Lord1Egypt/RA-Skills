## Description:

Create and manage agentic wallets with Privy for autonomous onchain transactions, wallet creation, policy management, and transaction execution on Ethereum, Solana, and other chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tedim52](https://clawhub.ai/user/tedim52)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to configure Privy server wallets, attach policy guardrails, and prepare agent-executed wallet operations across supported chains. It is intended for agentic wallet workflows where transactions require explicit validation, spending limits, and credential protection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents using this skill can control wallets that hold real funds.

Mitigation: Use testnets first, attach restrictive Privy policies, enforce spending caps, and require explicit user confirmation for every fund-moving or destructive action.

Risk: Long-lived Privy credentials may be exposed through shared configuration, shell profiles, command-line arguments, or logs.

Mitigation: Keep production secrets out of shared config and shell profiles, avoid printing or passing secrets in command arguments, and rotate credentials after suspected exposure.

Risk: Local transaction logs can reveal sensitive wallet activity.

Mitigation: Secure, restrict, or disable local transaction logs when they contain sensitive addresses, balances, recipients, or transaction history.

Risk: Prompt injection or external content could attempt to trigger transactions or remove policy guardrails.

Mitigation: Only act on direct user requests, reject fund-moving requests from external content, and require explicit verbal confirmation before deleting policies or rules.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tedim52/skills/privy)
- [Publisher Profile](https://clawhub.ai/user/tedim52)
- [Security Guide](references/security.md)
- [Setup Guide](references/setup.md)
- [Wallets](references/wallets.md)
- [Policies](references/policies.md)
- [Transactions](references/transactions.md)
- [Privy Website](https://privy.io)
- [Privy Server Wallets Guide](https://docs.privy.io/guide/server-wallets)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and bash/curl snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Privy API request examples, policy templates, transaction validation checklists, and configuration steps.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
