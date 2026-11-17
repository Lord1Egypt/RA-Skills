## Description:

Search and read Supervisely data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents and users managing Supervisely projects use this skill to retrieve account, team, workspace, project, and dataset information through an OOMOL-connected Supervisely account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified remote code without a clear user approval step.

Mitigation: Review the setup source before installation, install a verified and pinned oo CLI separately, and require approval before setup changes. Disable automatic skill synchronization if it is unwanted, and use a limited Supervisely connection.

## Reference(s):

- [Supervisely homepage](https://supervisely.com)
- [Supervisely API documentation](https://api.docs.supervisely.com/)
- [oo CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-supervisely)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance, Shell commands]

**Output Format:** [JSON data returned by oo CLI with concise task-relevant guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Supervisely data retrieval; no write actions are documented.]

## Skill Version(s):

1.0.4 (source: frontmatter; server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
