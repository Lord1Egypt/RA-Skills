## Description:

Userflow (userflow.com). Use this skill for ANY Userflow request — reading, creating, updating, and deleting data. Whenever a task involves Userflow, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to read, create, update, and delete Userflow users, groups, and events through a connected OOMOL account. Review the exact effect of writes and deletions before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded CLI code that has not been verified.

Mitigation: Review and approve CLI installation separately; prefer a verified, pinned release.

Risk: Using the connected Userflow account gives OOMOL access to its credentials and requested data operations.

Mitigation: Keep approval requirements for writes and deletions, and disable automatic skill synchronization if other agent skills should not be changed.

## Reference(s):

- [Userflow](https://userflow.com)
- [Userflow API documentation](https://userflow.com/docs/api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON action payloads, oo CLI commands, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action schemas are inspected before payloads are run; writes and deletions require confirmation.]

## Skill Version(s):

1.0.7 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
