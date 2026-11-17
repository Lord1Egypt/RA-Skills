## Description:

Fetches and displays current Weibo hotspot data, groups titles by source_name, reports service status, and can provide a user-approved cron setup command for daily updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xltang](https://clawhub.ai/user/xltang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve current Weibo hotspot titles, check hotspot service availability, and optionally prepare a user-approved daily scheduled update.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill calls the listed hotspot API when invoked.

Mitigation: Installers should be comfortable with requests to https://hotspot.api4claw.com and the skill should report API failures clearly.

Risk: Optional cron setup can create recurring daily messages if the user approves it.

Mitigation: Only approve the cron command after checking the target channel, recipient, time, timezone, and agent session.

Risk: External hotspot data may be unavailable, malformed, or incomplete.

Mitigation: The skill should avoid fabricated content, report malformed or unreachable responses, and continue only with valid parsed items.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xltang/skills/hotspots-weibo)
- [Hotspot API base URL](https://hotspot.api4claw.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise Markdown text with optional bash command blocks for cron setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches fresh minute-stamped API data when invoked; scheduled behavior requires explicit user approval.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
