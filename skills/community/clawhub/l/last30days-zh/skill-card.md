## Description:

Aggregates recent results from Reddit, X/Twitter, YouTube, TikTok, Instagram, Hacker News, Polymarket, and web search into a last-30-days research brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research people, companies, products, markets, tools, or trends across recent social, community, prediction-market, and grounded web sources. It is suited for release reactions, competitor comparisons, community sentiment, and recent-dynamics summaries over a configurable lookback window.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics and selected result context may be sent to AISA and public source APIs.

Mitigation: Install only where that data sharing is acceptable for the user's topic and organization.

Risk: API keys can be exposed if passed directly on the command line or stored in overly permissive files.

Mitigation: Store AISA_API_KEY in ./.last30days-data/config.env with restrictive permissions, such as chmod 600.

Risk: Recent web and social snippets can be incomplete, biased, or misleading.

Mitigation: Treat generated briefs as research aids and verify important claims against primary sources before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/last30days-zh)
- [Publisher profile](https://clawhub.ai/user/bibaofeng)
- [AISA homepage](https://aisa.one)
- [AISA API endpoint](https://api.aisa.one)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON research brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include query plans, ranked candidates, clusters, and items grouped by source when JSON output is requested.]

## Skill Version(s):

1.0.9 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
