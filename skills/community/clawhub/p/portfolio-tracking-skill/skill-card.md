## Description:

An investment portfolio tracker that runs entirely locally. All data stays in ~/.portfolio-tracker/.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aigeneralstore](https://clawhub.ai/user/aigeneralstore)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to track portfolios, refresh prices, sync holdings from Binance, Interactive Brokers, and EVM wallets, and request portfolio allocation guidance from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles financial credentials and portfolio data while the security review flags unsafe credential handling and misleading local-only claims.

Mitigation: Review carefully before installing, use read-only and IP-restricted exchange credentials where possible, and assume exchange credentials, wallet addresses, and symbol lookups may be sent to third parties.

Risk: Local portfolio and configuration files may contain sensitive financial data and API credentials.

Mitigation: Set strict permissions on ~/.portfolio-tracker and review storage behavior before entering credentials.

Risk: The security review recommends waiting for improvements to command-line secret passing, secure local storage, dependency pinning or updates, and privacy disclosures.

Mitigation: Treat this release as requiring human security review before deployment, especially in shared, enterprise, or regulated environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aigeneralstore/skills/portfolio-tracking-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented instructions, with JSON exchanged through local CLI scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include portfolio summaries, price refresh results, sync summaries, setup guidance, and investment-analysis guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
