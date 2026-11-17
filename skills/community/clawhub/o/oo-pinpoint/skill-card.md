## Description:

Pinpoint (pinpointhq.com). Use this skill for any Pinpoint request involving searching and reading data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting teams use this skill to search and read applications, candidates, and jobs in a connected Pinpoint account through OOMOL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup can run unverified downloads and make persistent agent-skill changes.

Mitigation: Review and approve CLI installation separately, and check managed-skill synchronization settings before use.

Risk: Pinpoint use involves sensitive recruiting data handled through the OOMOL integration.

Mitigation: Connect only the intended Pinpoint account and consider how its recruiting data is handled.

## Reference(s):

- [Pinpoint API documentation](https://developers.pinpointhq.com/docs/introduction)
- [Pinpoint](https://www.pinpointhq.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Pinpoint skill page on ClawHub](https://clawhub.ai/oomol/skills/oo-pinpoint)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON connector results with concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only application, candidate, and job data from the available get and list actions.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
