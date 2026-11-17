## Description:

Builds dated, source-aware news briefings from GDELT, BBC, CNN, The Guardian, and Yahoo News through Crawlora.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and other news readers use this skill to compare public coverage, follow recent headlines and timelines, and prepare linked briefings that distinguish reporting from inference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: News queries, article URLs, and the API key are sent to Crawlora.

Mitigation: Avoid including secrets, personal data, or confidential research topics in queries; use a key you are comfortable sharing with Crawlora.

Risk: Search coverage varies by publisher, region, and freshness, and may include TV-news metadata or reader comments rather than reporting.

Mitigation: State the collection window and coverage limits, distinguish comments from reporting, and verify important claims against linked original articles.

## Reference(s):

- [News briefing endpoint reference](artifact/reference/endpoints.md)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/news-briefing-research)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dated briefings with source links, coverage limits, and uncertainty labels.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
