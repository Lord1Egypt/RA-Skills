## Description:

Operate Formbricks through a connected account, including creating contacts and managing contact attribute keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to work with Formbricks contacts and contact attribute keys through their connected account. It supports reading data and preparing changes, with confirmation required before write or destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes downloaded installation code, and the CLI may automatically synchronize other agent skills.

Mitigation: Review and install the CLI separately, and disable automatic skill synchronization if you want changes limited to this integration.

Risk: The connected Formbricks account can be changed or data can be deleted through write and destructive actions.

Mitigation: Connect only the intended account and confirm every change or deletion.

## Reference(s):

- [Formbricks](https://formbricks.com)
- [Formbricks REST API documentation](https://formbricks.com/docs/api-reference/rest-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and destructive actions require confirmation before execution.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
