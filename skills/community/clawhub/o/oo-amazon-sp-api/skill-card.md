## Description:

Connects agents to Amazon Selling Partner API actions through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Amazon sellers use the skill to read catalog and inventory data, search listings, and manage seller listings through their connected account. Changes to listings require careful review before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marks the external installer as suspicious because it was not shown to support the stated Amazon API purpose. The scan is partial and does not establish what the remote installer does.

Mitigation: Avoid installation until its source and contents are verified and its local changes are understood.

Risk: Write and destructive actions can change or delete seller listings.

Mitigation: Inspect the live action schema, review the exact payload and effect, and obtain explicit approval before running these actions.

## Reference(s):

- [Amazon Selling Partner API documentation](https://developer-docs.amazon/sp-api/docs/overview)
- [Amazon Selling Partner API homepage](https://developer.amazonservices.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON API action payloads and responses with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs must match the live connector schema; responses include data and execution metadata.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
