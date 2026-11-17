## Description:

Qase (qase.io). Use this skill for ANY Qase request — reading, creating, updating, and deleting data. Whenever a task involves Qase, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA teams use the skill to list and retrieve Qase projects, test cases, and test runs, and to create cases or runs and complete runs through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The oo CLI may make persistent changes to skills used by other agents through startup synchronization.

Mitigation: Review the CLI's skill-sync behavior, use a verified fixed CLI version, and disable synchronization with OO_SKILLS_SYNC_DISABLED before invoking it.

Risk: Remote installer contents and hosted connector behavior were not verified.

Mitigation: Review publisher documentation, connect only the Qase account access needed, and retain the skill's approval checks for changes.

## Reference(s):

- [Qase](https://qase.io/)
- [Qase API documentation](https://developers.qase.io/reference/introduction-to-the-qase-api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown instructions with shell command examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may return JSON data from the Qase connector.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
