## Description:

Use this skill for PractiTest requests to read, create, update, and delete data through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

QA teams and test engineers use the skill to retrieve PractiTest projects and tests and manage tests through a connected account. It supports read operations, test creation and updates, and approved test deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI installation and startup synchronization can affect local agent skills; the remote installers and deployed connector were not verified.

Mitigation: Review and install a verified CLI release separately. Review synchronization behavior and use OO_SKILLS_SYNC_DISABLED=1 to suppress startup synchronization when appropriate.

Risk: PractiTest changes can create, modify, or permanently delete account data.

Mitigation: Use a narrowly scoped PractiTest connection and require approval for every write or deletion.

## Reference(s):

- [PractiTest API v2 documentation](https://www.practitest.com/api-v2/)
- [oo CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [PractiTest on ClawHub](https://clawhub.ai/oomol/skills/oo-practitest)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON inputs and structured PractiTest responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read, create, update, or delete PractiTest records; the skill requires approval for writes and explicit approval for deletion.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
