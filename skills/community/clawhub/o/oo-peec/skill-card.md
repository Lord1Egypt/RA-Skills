## Description:

Use Peec AI to retrieve project lists and reporting data on brand visibility, sentiment, rankings, share of voice, and cited sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Peec users and analysts use this skill to review project reports covering brand visibility, sentiment, rankings, share of voice, and the domains and URLs cited in responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unverified software and make broader agent changes without clear user approval.

Mitigation: Review setup behavior first, use a verified CLI release installed under your control, and review its automatic skill synchronization.

Risk: Remote installer payloads and the hosted connector implementation remain unverified; Peec access is routed through OOMOL.

Mitigation: Authorize only the Peec account access needed for the task.

## Reference(s):

- [Peec AI](https://peec.ai/)
- [Peec API documentation](https://docs.peec.ai/api/introduction)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Analysis]

**Output Format:** [Structured report data and concise summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are limited to projects and data available through the connected Peec account.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
