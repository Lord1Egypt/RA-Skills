## Description:

Use this skill when the user explicitly mentions Hacker News or HN to fetch, rank, present, and optionally summarize Hacker News stories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ken7y](https://clawhub.ai/user/ken7y)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to get a concise Hacker News briefing that is ranked by stored interests when available and can be followed by deeper article summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses stored interests and preferences to rank Hacker News stories.

Mitigation: Use it only when interest-based ranking is acceptable, and fall back to points-based ranking when no clear interests are available.

Risk: The skill opens article URLs from Hacker News when the user asks for deeper summaries.

Mitigation: Review destination links and treat paywalled, PDF, or unavailable articles transparently before summarizing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ken7y/skills/hn-morning-brief)
- [Hacker News RSS front page feed](https://hnrss.org/frontpage)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown briefing with article and discussion links; helper script returns JSON story data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses up to 20 fetched Hacker News stories, ranks 8-12 items for the briefing, and may summarize selected article URLs on request.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
