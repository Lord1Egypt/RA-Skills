## Description:

Search GetProspect for companies and leads, find or verify business email addresses, and look up saved contact profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to search GetProspect's B2B company and lead data, find or verify business email addresses, and retrieve saved contact details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute a remote CLI installer without verifying a pinned release.

Mitigation: Review the CLI installation separately and use a pinned, verified release before enabling the skill.

Risk: Names, email addresses, and search inputs are processed through OOMOL and GetProspect.

Mitigation: Submit only information appropriate to share with both services.

## Reference(s):

- [GetProspect](https://getprospect.com)
- [GetProspect API documentation](https://getprospect.com/api-docs)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-getprospect)

## Skill Output:

**Output Type(s):** [Structured data, Text, Shell commands, Guidance]

**Output Format:** [JSON action requests and returned GetProspect data, with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by action and can include company, lead, contact, or email deliverability data.]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
