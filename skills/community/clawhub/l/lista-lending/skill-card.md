## Description:

View and operate Lista Lending vaults and markets for lending-only positions and deposit, withdraw, borrow, or repay workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lawson-ccy](https://clawhub.ai/user/lawson-ccy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect Lista Lending vault and market positions, select supported vault or market targets, and prepare or execute lending actions such as deposits, withdrawals, supply, borrow, and repay with wallet consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: State-changing lending operations may be unsafe because the security review reports a serious command-injection flaw in transaction execution.

Mitigation: Do not run deposit, withdraw, supply, borrow, repay, or market-withdraw until transaction execution avoids shell interpretation; review every transaction before signing.

Risk: Wallet-session metadata and debug logs may expose wallet topics or related session details.

Mitigation: Avoid enabling debug logs with wallet topics, restrict access to wallet-session files, and reconnect or rotate sessions if logs were exposed.

Risk: RPC endpoint trust affects lending reads and transaction preparation.

Mitigation: Use trusted RPC endpoints and confirm chain, market or vault target, token, and amount before consent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lawson-ccy/skills/lista-lending)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON CLI output summarized by the agent as concise text or Markdown tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports vault, market, holdings, selection, configuration, simulation, and wallet-mediated transaction workflows.]

## Skill Version(s):

0.1.1 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
