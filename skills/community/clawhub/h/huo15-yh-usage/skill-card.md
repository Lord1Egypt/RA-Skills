## Description:

Queries token usage and billing for a customer-provided Huo15 YanHua Zhihui API key, with totals, provider and model breakdowns, daily trends, and CNY/USD display options based on the platform billing endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, support teams, and sales teams use this skill to produce a customer-facing usage and cost summary for a specific Huo15 YanHua Zhihui API key. It helps identify overall spend, high-cost models or providers, and recent daily usage trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a live customer API key to query usage and billing data.

Mitigation: Use only trusted terminals and automation, avoid logging command invocations that contain keys, and rotate keys after use in untrusted environments.

Risk: The billing request is sent to a third-party endpoint and can be redirected with YH_BASE.

Mitigation: Trust the publisher and endpoint before installation, and leave YH_BASE unset unless the alternate endpoint is fully trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-yh-usage)
- [Huo15 usage API endpoint](https://fireworks-simulator-api.huo15.com/v1/usage?days=N)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown billing report with optional raw JSON output and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are scoped to one fsk-prefixed API key, support a 1-90 day range, and can display CNY or USD-converted costs.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
