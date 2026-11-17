## Description:

Use this skill to search and read data from a connected Coinbase account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use it to retrieve Coinbase Advanced Trade brokerage account details or list accounts available to their connected API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions may run downloaded installers that were not verified, or introduce broader changes to agent skills.

Mitigation: Review setup first, use a verified oo CLI release, and require approval before installation or changes to other agent skills.

Risk: Coinbase access passes through OOMOL, and the connected API key determines the available account access.

Mitigation: Use a read-only Coinbase API key and understand that requests are handled through OOMOL.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-coinbase)
- [Coinbase Advanced Trade API documentation](https://docs.cdp.coinbase.com/api-reference/advanced-trade-api/rest-api/introduction)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands and JSON account data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only account lookup results; requires an existing OOMOL connection.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
