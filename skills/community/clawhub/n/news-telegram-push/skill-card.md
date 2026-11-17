## Description:

Curate and send twice-daily English Telegram news pushes covering Industry News, Financial News, and Global Political News with strict deduplication and trusted-source filtering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chamic24](https://clawhub.ai/user/chamic24)

### License/Terms of Use:

MIT-0

## Use Case:

News and market-communications operators use this skill to produce Telegram-ready English news pushes with three fixed sections, ten vetted headline links per section, and strict deduplication across daily sends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill formats news for Telegram but does not implement posting controls, approval steps, scheduling safeguards, or delivery checks.

Mitigation: Keep review, scheduling, and send permissions in the surrounding Telegram workflow or operator process.

Risk: Strict no-summary and no-source-label formatting can reduce context for readers and reviewers.

Mitigation: Require each item to include a credible "Read more" link and review selected headlines before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chamic24/skills/news-telegram-push)
- [Publisher profile](https://clawhub.ai/user/chamic24)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Telegram-ready Markdown-style text with numbered headline links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [English only; exactly three sections with ten numbered items each; no summaries, source labels, or extra commentary.]

## Skill Version(s):

2.0.4 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
