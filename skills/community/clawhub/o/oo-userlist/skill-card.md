## Description:

Userlist (userlist.com). Use this skill for ANY Userlist request — reading, creating, and updating data. Whenever a task involves Userlist, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and customer operations teams use this skill to read, create, and update Userlist data, and to send transactional messages through a connected account. It directs users to approve write actions before they run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified remote code and may add undisclosed changes to other agent skills.

Mitigation: Review setup behavior and install a reviewed CLI release. Set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI to prevent startup changes to other agent skills.

Risk: The connected service processes Userlist data and credentials, and write actions can change data or send messages.

Mitigation: Confirm OOMOL may process the data and credentials, and keep the existing approval requirement for each write action.

## Reference(s):

- [Userlist Push API documentation](https://userlist.com/docs/developers/push-api/)
- [oo CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Text and JSON returned from oo CLI actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions require user approval.]

## Skill Version(s):

1.0.6 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
