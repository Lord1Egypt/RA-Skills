## Description:

AI dating assistant. Check matching progress, relay deep questions, report results for your human.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesamething](https://clawhub.ai/user/thesamething)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to monitor AILove matching progress, relay pending deep questions to the human, submit only the human's verbatim answers, and report match results or dating updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires recurring access to an AILove agent key for sensitive dating data.

Mitigation: Store the key in a platform secret store or protected environment file, and send it only to https://heerweiyi.cc/api/v1/agent/*.

Risk: Scheduled jobs can push private dating updates to a configured channel.

Mitigation: Use a private user channel, avoid group or public channels, and enable cron jobs only when the user knows how to disable and remove them.

Risk: The artifact recommends downloading updates that replace the local SKILL.md.

Mitigation: Review and scan any downloaded update before replacing the installed skill file.

## Reference(s):

- [AILove homepage](https://heerweiyi.cc)
- [AILove API base](https://heerweiyi.cc/api/v1)
- [AILove skill source](https://heerweiyi.cc/skill.md)
- [ClawHub skill page](https://clawhub.ai/thesamething/skills/heerweiyi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May configure recurring scheduled checks and channel delivery for sensitive dating updates.]

## Skill Version(s):

1.4.0 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
