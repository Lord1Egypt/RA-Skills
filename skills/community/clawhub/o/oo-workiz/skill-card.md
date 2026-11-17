## Description:

Use Workiz to search and read jobs, leads, and team member information through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Workiz account users can retrieve jobs, leads, and active team member records from their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may direct the agent to execute downloaded CLI software without a separate review or approval step.

Mitigation: Review and separately approve CLI installation; use a reviewed release with verified integrity.

Risk: Connecting Workiz gives OOMOL access to business records and account credentials.

Mitigation: Review the connection's access and the skill's automatic synchronization settings before connecting.

## Reference(s):

- [Workiz](https://www.workiz.com)
- [Workiz API documentation](https://developer.workiz.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Text]

**Output Format:** [JSON results and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Workiz account and requested filters.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
