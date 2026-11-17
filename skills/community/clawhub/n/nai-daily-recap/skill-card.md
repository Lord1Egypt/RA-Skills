## Description:

Generate a daily recap of agent activity from memory logs and optional Discord messages, then save a structured Obsidian journal entry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users who keep Obsidian journals use this skill to summarize end-of-day agent activity, capture notable requests and outcomes, and maintain a dated daily recap.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and persist private agent activity and optional Discord messages.

Mitigation: Limit access to approved memory files and Discord channels, make Discord scanning opt-in, and redact secrets or private details before writing recaps.

Risk: Nightly cron execution can create unattended records of sensitive activity.

Mitigation: Run with least-privilege file and channel access, then review generated entries before sharing or syncing them broadly.

## Reference(s):

- [Daily Recap ClawHub Skill Page](https://clawhub.ai/newageinvestments25-byte/skills/nai-daily-recap)

## Skill Output:

**Output Type(s):** [Markdown, Text, Files]

**Output Format:** [Markdown journal entry with YAML frontmatter and concise bullet sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes or appends a dated Obsidian recap under vault/daily-recap and notes completion in the memory log.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
