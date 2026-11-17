## Description:

Use this skill for Dailybot requests involving reading, creating, or updating data through the connected Dailybot service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Dailybot-connected users and agents use this skill to retrieve organization, team, and user information, and to open conversations or send email and chat messages through Dailybot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI can persistently install skills across agent applications, and those changes are not described in the skill.

Mitigation: Review the CLI setup before installing, review the installer separately, and disable startup skill synchronization if those changes are unwanted.

Risk: Actions that send messages or emails can communicate externally through the connected Dailybot account.

Mitigation: Retain confirmation for messages and emails.

## Reference(s):

- [Dailybot](https://www.dailybot.com)
- [Dailybot API documentation](https://www.dailybot.com/developers)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Dailybot skill release](https://clawhub.ai/oomol/skills/oo-dailybot)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with shell command examples; connector action results in JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results vary by Dailybot action and the connected account.]

## Skill Version(s):

1.0.6 (source: artifact metadata, server release version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
