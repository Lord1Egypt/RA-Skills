## Description:

Helps agents find and summarize financial and crypto news, market signals, and company information through the OpenNews API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[infra403](https://clawhub.ai/user/infra403)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts, traders, and other agents use this skill to look up market-moving news, crypto signals, company filings, and strategy-triggered events. Free news categories and hot-news feeds work without a token; expanded searches and strategy history require an OpenNews token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market-news searches, company identifiers, wallet addresses supplied for lookup, and authenticated requests are sent to the external OpenNews API.

Mitigation: Avoid entering sensitive identifiers or addresses; use the token-free curated news endpoints when full search is not needed.

Risk: Authenticated strategy queries may expose saved strategy names and triggered-history results in agent responses.

Mitigation: Request strategy history only when needed and review responses before sharing them.

## Reference(s):

- [Opennews release on ClawHub](https://clawhub.ai/infra403/skills/opennews-2)
- [OpenNews token and API access](https://6551.io/mcp)
- [OpenNews API](https://ai.6551.io)
- [Strategy management](https://www.newsliquid.com/strategy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries and guidance with optional API commands and structured news details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source links, impact scores, trading signals, and bilingual summaries when available.]

## Skill Version(s):

0.1.1 (source: ClawHub release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
