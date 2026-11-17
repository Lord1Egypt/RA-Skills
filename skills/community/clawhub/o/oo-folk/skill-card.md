## Description:

folk (folk.app). Use this skill for ANY folk request — reading, creating, updating, and deleting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing Folk workspaces can use this agent skill to retrieve and maintain contacts, companies, groups, custom fields, and workspace users through Folk's connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup depends on an external installer payload, and the exact installed CLI release is unverified.

Mitigation: Review and install a fixed CLI version yourself before use.

Risk: The CLI may synchronize additional agent skills during startup.

Mitigation: Verify that OO_SKILLS_SYNC_DISABLED=1 is supported by the selected release and use it to disable startup synchronization when appropriate.

Risk: Connected Folk actions can access or change workspace records.

Mitigation: Connect only the intended Folk account and keep the required confirmations for record changes.

## Reference(s):

- [Folk](https://folk.app)
- [Folk API documentation](https://developer.folk.app/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI commands and environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON action results and shell command instructions in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions include retrieval, creation, updates, and deletion; write actions require confirmation and destructive actions require explicit approval.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
