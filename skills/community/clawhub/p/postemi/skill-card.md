## Description:

Postemi schedules and publishes social posts from the command line to 37 platforms and apps, including Facebook, Instagram, X, LinkedIn, TikTok, YouTube, Threads, Bluesky, Pinterest and Mastodon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[norbertlevente](https://clawhub.ai/user/norbertlevente)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to prepare, schedule, publish, and manage social posts through Postemi's command-line workflow. Developers can also use its channel and post analytics and account-management commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes analytics, billing, and agent-skill management capabilities alongside social posting, and the security review did not resolve every referenced item.

Mitigation: Review those capabilities and unresolved references before use, and limit actions to the functions the user requested.

Risk: Publishing commands can post content to connected social accounts.

Mitigation: Show the destination, full content, media, and schedule, and obtain user confirmation before publishing.

## Reference(s):

- [Postemi website](https://postemi.com)
- [Postemi CLI details](reference/details.md)
- [Postemi provider settings](https://github.com/norbertlevente/postemi-agent/blob/main/PROVIDER_SETTINGS.md)
- [Postemi skill page](https://clawhub.ai/norbertlevente/skills/postemi)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Channel-specific steps and settings; obtain user confirmation before publishing.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
