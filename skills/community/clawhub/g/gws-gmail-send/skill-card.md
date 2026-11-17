## Description:

Gmail: Send an email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to prepare Gmail send commands with recipients, subject, body text or HTML, sender alias, copies, blind copies, and attachments. It supports sending immediately, saving a draft, or using a dry run for review before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prepare Gmail write commands that send messages or create drafts, which may disclose message content or attachments to unintended recipients.

Mitigation: Review recipients, sender alias, subject, body, and attachments before approving execution; prefer --dry-run or --draft for sensitive messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-gmail-send)

## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws command-line tool; review email fields before approving execution.]

## Skill Version(s):

1.0.15 (source: server release metadata; embedded skill metadata 0.22.5 from SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
