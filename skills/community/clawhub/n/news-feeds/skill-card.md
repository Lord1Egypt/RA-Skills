## Description:

Fetch latest news headlines from major RSS feeds (BBC, Reuters, AP, Al Jazeera, NPR, The Guardian, DW).

This skill is ready for commercial/non-commercial use.

## Publisher:

[lknik](https://clawhub.ai/user/lknik)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to fetch current headlines, news briefings, daily digests, and topic-filtered RSS news from supported international sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to external RSS providers when used.

Mitigation: Run it only in environments where access to the configured news feed domains is acceptable, and review returned links before relying on or sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lknik/skills/news-feeds)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown grouped by source, or JSON when the --json option is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Headlines may include descriptions, publication times, links, source/category labels, fetch errors, and topic-filtered results.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
