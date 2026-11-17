## Description:

Trust infrastructure for AI agents to register on-chain identities, check trust scores, assess token safety, and protect wallet transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhinresh](https://clawhub.ai/user/jhinresh)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to register agent identities, check counterparties before transactions, evaluate token risk, and report trust outcomes through Maiat services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill links wallet identities and agent reputation data with an external service.

Mitigation: Use a dedicated wallet or pseudonymous identity, and confirm what transaction and report data Maiat receives before production use.

Risk: Wallet transaction protection depends on third-party npm packages and service responses.

Mitigation: Pin and audit the packages before installation, and review failure behavior before enabling automatic blocking or reporting.

Risk: Automatic blocking or threat reporting may affect transaction availability or privacy.

Mitigation: Enable automatic actions only when the privacy, failure, and appeal behavior matches the operator's risk tolerance.

## Reference(s):

- [Maiat App](https://app.maiat.io)
- [Maiat API Base](https://app.maiat.io/api/v1)
- [Maiat API Docs](https://app.maiat.io/docs)
- [Maiat Passport Portal](https://passport.maiat.io)
- [ClawHub Skill Listing](https://clawhub.ai/jhinresh/skills/maiat-trust-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl commands, JSON examples, TypeScript snippets, and configuration values.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to call external Maiat APIs, install npm packages, and store identity or wallet-related configuration.]

## Skill Version(s):

2.4.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
