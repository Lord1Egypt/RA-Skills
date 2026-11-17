## Description:

Use your OOMOL-connected account to search and read Northflank project and service information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to list Northflank projects and services and retrieve their details through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup recommends running downloaded installer code whose full local changes were unavailable for inspection.

Mitigation: Review the installer, verify an official CLI release, and explicitly approve installation; check the CLI's bundled-skill synchronization settings.

Risk: The connected account can expose Northflank project and service information through OOMOL.

Mitigation: Use read-only permissions where available and limit the connected account to the projects needed for the task.

## Reference(s):

- [Northflank API documentation](https://northflank.com/docs/v1/api/use-the-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell command and JSON examples; Northflank results are returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only project and service lookup actions.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
