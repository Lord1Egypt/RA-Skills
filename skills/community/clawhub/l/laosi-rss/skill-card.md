## Description:

RSS监控技能 - 监控RSS/Atom订阅源，检测更新，获取新内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to parse RSS/Atom feeds, check for new entries, and retrieve recent feed items for monitoring blogs, news sources, podcasts, and social updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted RSS or Atom feed URLs can create network trust and egress exposure when fetched by an agent or deployed service.

Mitigation: Only add public feed URLs from trusted sources; validate feed URLs and restrict network egress before exposing this behavior as a service.

Risk: The skill depends on the third-party Python package feedparser.

Mitigation: Install feedparser in an isolated environment when practical and prefer a pinned version.

Risk: Fetched feed content may include inaccurate, stale, or untrusted third-party text and links.

Mitigation: Review fetched feed items before using them in decisions, publication workflows, or automated downstream actions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
