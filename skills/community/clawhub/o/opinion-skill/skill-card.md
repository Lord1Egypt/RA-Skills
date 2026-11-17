## Description:

Opinion Skill helps agents query Opinion prediction markets and run Bun-based market, order, balance, position, and trade workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuandiaodiaodiao](https://clawhub.ai/user/yuandiaodiaodiao)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to inspect Opinion prediction market data, review prices and order books, check positions and balances, and prepare or execute trading actions when wallet credentials are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation flow may run mutable remote code and a curl-to-shell Bun installer.

Mitigation: Review and pin the external source before installation, use a verified Bun install path, and run from a non-root working directory.

Risk: Trading scripts require a private key, multisig wallet address, and API key.

Mitigation: Protect the .env file, avoid sharing credentials with the agent, and fund or approve only wallets whose funds you can afford to risk.

Risk: Some market and position queries use an unencrypted HTTP API for decision-critical data.

Mitigation: Treat HTTP responses as untrusted, verify prices and order details against trusted sources before trading, and avoid relying on unauthenticated data for irreversible actions.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/yuandiaodiaodiao/skills/opinion-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve live market data queries and wallet-authorized trading operations.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
