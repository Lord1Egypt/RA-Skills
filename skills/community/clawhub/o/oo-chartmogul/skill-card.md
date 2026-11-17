## Description:

ChartMogul (chartmogul.com). Use this skill for ANY ChartMogul request — searching and reading data. Whenever a task involves ChartMogul, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users with an OOMOL-connected ChartMogul account use this skill to retrieve account settings, customer records, contacts, and data sources through read-only actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute unverified remote code and make broader changes to agent skills.

Mitigation: Review and install a verified CLI release separately, consider disabling automatic skill synchronization with OO_SKILLS_SYNC_DISABLED=1, and confirm the connected account's access.

## Reference(s):

- [ChartMogul homepage](https://chartmogul.com/)
- [ChartMogul API authentication documentation](https://dev.chartmogul.com/docs/authentication/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ChartMogul ClawHub release](https://clawhub.ai/oomol/skills/oo-chartmogul)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON data with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only account, customer, contact, and data-source retrieval; results depend on the selected action and filters.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
