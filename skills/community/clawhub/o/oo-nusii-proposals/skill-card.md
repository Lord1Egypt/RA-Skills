## Description:

Manage Nusii Proposals data through connected account actions for clients, proposals, templates, themes, and users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing Nusii proposals can use this skill to inspect clients and proposals, create or update records, send proposals, and archive proposals. It requires confirmation before write or destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback directs the agent to run an unverified remote installer without separate user approval.

Mitigation: Prefer a verified CLI release installed under your control and require approval before either downloaded installer executes. Check proposal changes and recipients when approving actions.

## Reference(s):

- [Nusii Proposals](https://nusii.com/)
- [Nusii API documentation](https://developer.nusii.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Nusii Proposals skill page](https://clawhub.ai/oomol/skills/oo-nusii-proposals)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON action results with concise textual guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by the requested Nusii action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
