## Description:

Use this skill to search and read Teamtailor data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting operations teams use this skill to search Teamtailor departments, jobs, and locations and retrieve job details through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can execute downloaded code and add other agent skills without clearly explaining those changes.

Mitigation: Review and approve CLI installation separately, verify the installer and selected release, decide whether to allow additional skills, and use OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization. Limit Teamtailor connection permissions to those needed.

## Reference(s):

- [Teamtailor homepage](https://www.teamtailor.com/)
- [Teamtailor API documentation](https://docs.teamtailor.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Teamtailor ClawHub listing](https://clawhub.ai/oomol/skills/oo-teamtailor)

## Skill Output:

**Output Type(s):** [Text, JSON data]

**Output Format:** [Structured Teamtailor records with text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only retrieval; results depend on the connected account's permissions.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
