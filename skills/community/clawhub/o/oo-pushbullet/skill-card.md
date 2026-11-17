## Description:

Pushbullet (pushbullet.com). Use this skill for ANY Pushbullet request — reading, creating, updating, and deleting data. Whenever a task involves Pushbullet, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Pushbullet can read and manage pushes, chats, and devices through their OOMOL-connected account. The skill also sends pushes and creates, updates, or deletes Pushbullet data when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs downloaded code execution without a clear approval step.

Mitigation: Review and approve CLI installation separately, using a verified release, and check automatic skill synchronization before first use.

Risk: OOMOL brokers access to the connected Pushbullet account.

Mitigation: Connect only an account intended for this use and retain the skill's confirmation steps for sending, changing, and deleting data.

## Reference(s):

- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Pushbullet](https://www.pushbullet.com)
- [Pushbullet API documentation](https://docs.pushbullet.com/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON connector responses and concise action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include connector data and execution metadata.]

## Skill Version(s):

1.0.6 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
