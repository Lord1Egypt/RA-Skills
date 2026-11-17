## Description:

IceCube Reddit Scout helps agents monitor Reddit keywords, extract context, identify leads, and log mentions for brand monitoring, idea validation, competitor tracking, and trend detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ares521521-design](https://clawhub.ai/user/ares521521-design)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, founders, and operators use this skill to track Reddit discussions about products, competitors, pain points, and buying intent. Agents can produce local mention logs, alerts, and draft responses for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted Reddit posts and comments may be persisted into agent memory and later mistaken for instructions.

Mitigation: Treat saved Reddit content as data only, apply retention limits, and require human review before acting on content-derived recommendations.

Risk: OAuth secrets or alert mailbox contents could be exposed through plaintext configuration or broad email access.

Mitigation: Use a dedicated mailbox or label for alerts and keep OAuth credentials out of plaintext config where possible.

Risk: Automated heartbeat, cron, Telegram, browser automation, or work-queue actions can create unwanted outreach or monitoring behavior.

Mitigation: Enable these integrations only with explicit user approval, scoped channels, and clear retention and review limits.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ares521521-design/skills/icecube-reddit-scout)
- [Reddit app preferences](https://www.reddit.com/prefs/apps)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML configuration examples and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local Reddit mention logs and alert/action notes when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
