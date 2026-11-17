## Description:

LINE (line.me). Use this skill for ANY LINE request — reading, creating, and updating data. Whenever a task involves LINE, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to read LINE Official Account and user profile information, and to send text messages through their connected LINE account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs users to run downloaded installation code without verification or separate approval; the external installer and CLI were not inspected.

Mitigation: Review setup instructions, install through a verified process, and require approval before host software changes.

Risk: LINE write actions can send messages to one user, a group, or all friends of the connected Official Account.

Mitigation: Check the connected account and confirm recipients and message text, especially for broadcasts.

## Reference(s):

- [ClawHub LINE skill release](https://clawhub.ai/oomol/skills/oo-line)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [LINE Messaging API reference](https://developers.line.biz/en/reference/messaging-api/)
- [LINE homepage](https://line.me)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON connector responses with natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides bot and user profile reads and text messaging actions; messaging actions require confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
