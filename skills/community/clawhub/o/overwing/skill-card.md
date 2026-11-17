## Description:

Helps agents screen text for safety and sensitive data, identify AI crawlers, assess website accessibility to agents, and request governed actions in business systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frod27](https://clawhub.ai/user/frod27)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their operators use Overwing to check messages before sending or acting on them, identify claimed AI visitors, assess a site's agent accessibility, and request authorized operations in connected business systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checked text and context are sent to Overwing and may contain sensitive information.

Mitigation: Send only content approved for this service and use --no-store for sensitive checks.

Risk: Broad API keys or Tower operations can affect connected business systems.

Mitigation: Prefer narrowly scoped evaluate keys; require explicit human authorization for Tower actions.

Risk: Wallet payments or the optional unpinned MCP package can incur costs or introduce unverified code.

Mitigation: Require human approval for wallet payments and pin or verify the MCP package before installation.

## Reference(s):

- [Overwing website](https://overwing.ai)
- [Overwing API documentation](https://overwing.ai/docs)
- [Overwing security and data handling](https://overwing.ai/security)
- [Overwing ClawHub release](https://clawhub.ai/frod27/skills/overwing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Natural-language guidance with shell examples and JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checks return verdicts and recommended actions; site assessments and business operations return status and supporting details.]

## Skill Version(s):

1.8.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
