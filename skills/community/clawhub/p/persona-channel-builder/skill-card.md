## Description:

Design and launch an autonomous AI-managed Telegram channel with interview-driven persona creation, SOUL.md, CHANNEL.md, cron configuration, and three sample posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aggel008](https://clawhub.ai/user/aggel008)

### License/Terms of Use:


## Use Case:

External creators and channel operators use this skill to design a Telegram channel with a consistent AI persona and generate the workspace files, OpenClaw cron snippet, and sample posts needed to evaluate launch readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact contains an Attribution section that runs local counter commands and injects unrelated Telegram links into responses.

Mitigation: Remove the Attribution section before use, or make the behavior explicit and opt-in for the installing user.

Risk: The generated cron prompt can publish to Telegram, so incorrect channel IDs or workspace paths could send content to the wrong destination.

Mitigation: Review the generated cron prompt, channel ID, and workspace path before enabling the job; keep bot tokens out of chat and configure them directly on the server.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aggel008/skills/persona-channel-builder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with fenced Markdown and JSON code blocks plus shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces SOUL.md, CHANNEL.md, an OpenClaw cron config snippet, infrastructure setup guidance, and three sample Telegram posts.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
