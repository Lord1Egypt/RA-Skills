## Description:

OpenNews helps agents query real-time crypto, equities, macro, and financial market news and signals from the 6551 API, including AI impact scores, trading signals, and bilingual summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[infra403](https://clawhub.ai/user/infra403)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to retrieve market-moving news, financial events, company and holdings evidence, and strategy-triggered updates through OpenNews/6551 endpoints. It is intended for time-sensitive market research workflows, not as a substitute for independent financial or compliance review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run curl commands against OpenNews/6551 endpoints using OPENNEWS_TOKEN.

Mitigation: Install only when that API access is intended, keep OPENNEWS_TOKEN scoped and private, and review generated commands before execution.

Risk: The documented WebSocket connection places OPENNEWS_TOKEN in the URL query string.

Mitigation: Avoid printing, logging, sharing, or saving WebSocket URLs that include the token.

Risk: The release requests local read access even though the security summary identifies it as unnecessary.

Mitigation: Prefer an updated version that removes unused local read permission or limits file reads to explicit user-selected paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/infra403/skills/opennews-mcp)
- [OpenNews token page](https://6551.io/mcp)
- [OpenNews API base URL](https://ai.6551.io)
- [News sources endpoint](https://ai.6551.io/open/news_type)
- [News search endpoint](https://ai.6551.io/open/news_search)
- [Strategy management page](https://www.newsliquid.com/strategy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples, JSON request examples, and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call OpenNews/6551 API endpoints with curl; authenticated search is documented with a maximum of 100 results per request, while free endpoints provide limited curated results.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
