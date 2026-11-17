## Description:

Use this skill to search and read data in IT Glue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

IT administrators and service providers can use the skill to search and read configurations, contacts, organizations, and users in an IT Glue account connected through OOMOL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs downloaded code without clear approval or limits on lasting local changes.

Mitigation: Review setup behavior before enabling the skill; prefer a separately approved and reviewed CLI installation, and retain control over additional agent-skill changes.

Risk: Using the connected IT Glue account involves trusting OOMOL with the connection and returned records.

Mitigation: Connect IT Glue only if you trust OOMOL to handle the connection and returned records.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [IT Glue](https://www.itglue.com/)
- [IT Glue API documentation](https://api.itglue.com/developer/)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured IT Glue records with natural-language summaries and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read operations for configurations, contacts, organizations, and users.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
