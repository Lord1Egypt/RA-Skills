## Description:

Balance tracking, order overview, and market data across exchanges using OpenMM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adacapo21](https://clawhub.ai/user/adacapo21)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to inspect exchange balances, open orders, tickers, order books, trades, and Cardano token prices through the OpenMM CLI or MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires exchange API credentials for a third-party CLI package.

Mitigation: Use separate read-only API keys for this skill and disable trading and withdrawal permissions.

Risk: Credential examples may lead users to put secrets directly into shell history or shared terminals.

Mitigation: Set credentials through a secure environment or secrets manager and avoid pasting live keys into shell history.

Risk: The OpenMM package release is installed by package name rather than pinned in the skill metadata.

Mitigation: Review and trust the current @3rd-eye-labs/openmm package release before exposing account credentials to it.

## Reference(s):

- [Exchange Data Reference](references/exchange-data.md)
- [OpenMM Portfolio on ClawHub](https://clawhub.ai/adacapo21/skills/openmm-portfolio)
- [adacapo21 ClawHub Publisher Profile](https://clawhub.ai/user/adacapo21)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash command examples and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the openmm binary and at least one configured exchange API credential set.]

## Skill Version(s):

0.1.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
