## Description:

Fetch RSS feeds via curl, curate, and deliver news briefings to Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hohobohan](https://clawhub.ai/user/hohobohan)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, or developers use this skill to schedule recurring AI and market news briefings that fetch RSS feeds, curate 5-7 stories, and deliver a concise Telegram-ready Markdown briefing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled runs auto-send briefings to a hard-coded Telegram chat destination.

Mitigation: Replace or disable the Telegram delivery target before installation and confirm the intended recipient for scheduled briefings.

Risk: The skill relies on recurring shell-based curl retrieval from external RSS feeds.

Mitigation: Grant cron and exec access only in environments where recurring feed retrieval is acceptable, or adapt the skill to use a restricted feed-fetching wrapper.

Risk: RSS feed failures or blocked endpoints can reduce briefing completeness.

Mitigation: Use the verified feed list, keep failed-feed notes in the briefing, and avoid sources identified by the artifact as unreliable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hohobohan/skills/news-curator)
- [Publisher profile](https://clawhub.ai/user/hohobohan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown briefing with linked headlines and operational guidance for cron-based RSS retrieval]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets 5-7 stories and approximately 1500-3000 characters per briefing.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
