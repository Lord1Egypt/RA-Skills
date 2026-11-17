## Description:

Generate and deliver a Hacker News daily report (Top-N) with article summaries and multi-view comment synthesis, in user-selected language, with optional file persistence and index update.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liu7yong](https://clawhub.ai/user/liu7yong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate a daily Hacker News brief with source summaries, comment viewpoint synthesis, optional saved Markdown output, and index updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches live Hacker News stories and follows third-party article URLs from the user's environment.

Mitigation: Run it in a sandboxed or network-restricted environment and add URL validation or an allowlist before unattended use.

Risk: Scheduled retry jobs may run automatically and repeatedly if reminders are enabled.

Mitigation: Disable scheduling unless needed and review scheduled jobs for isolation, idempotency, and expected timing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liu7yong/skills/hn-daily-brief)
- [Hacker News Firebase API](https://hacker-news.firebaseio.com/v0)
- [Hacker News Item Pages](https://news.ycombinator.com/item?id={sid})

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown report body with optional saved Markdown files and JSON materials]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports language, Top-N count, strict or lite style, output directory, persistence, and optional scheduled reminder settings.]

## Skill Version(s):

0.8.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
