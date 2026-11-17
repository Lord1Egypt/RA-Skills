## Description:

RSS news aggregator that fetches current headlines from curated public feeds across news, games, and finance categories and returns structured JSON without requiring API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nesdeq](https://clawhub.ai/user/nesdeq)

### License/Terms of Use:

MIT

## Use Case:

Agents use this skill to collect and summarize current RSS headlines for users asking for news, gaming, finance, market, or briefing-style updates. It is useful when the agent needs a concise, source-attributed rundown from public feeds instead of broad web search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts many public RSS sources and returns third-party headlines, summaries, and links that may be incomplete, misleading, or unsafe to trust directly.

Mitigation: Treat returned headlines and links as untrusted news content, summarize with source attribution, and avoid presenting feed content as verified fact without user-requested follow-up.

Risk: Finance headlines may be time-sensitive or misleading if used as investment guidance.

Mitigation: Present finance items as news signals only and avoid using them as the sole basis for financial decisions.

Risk: The feedparser dependency is not pinned by the artifact.

Mitigation: Install in a virtual environment and pin an approved feedparser version before production use.

Risk: Some configured feeds use HTTP, which weakens transport integrity.

Mitigation: Prefer HTTPS feed URLs where available and review feed sources before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nesdeq/skills/openclaw-feeds)
- [Publisher profile](https://clawhub.ai/user/nesdeq)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Structured JSON from the feed script, typically presented to the user as concise Markdown with source links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Entries include category metadata plus headline, URL, source, date, and summary fields; summaries are stripped of HTML and truncated.]

## Skill Version(s):

3.1.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
