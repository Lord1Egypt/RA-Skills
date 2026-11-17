## Description:

Queries daily estimated Amazon ASIN unit sales and latest known price through Jungle Scout data across ten marketplaces for a requested date range.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and ecommerce analysts use this skill to estimate daily sales for a single ASIN, monitor competitor sales trends, evaluate product demand, and summarize day-level sales and price data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LinkFox receives ASIN queries and account or authentication data during onboarding.

Mitigation: Install only if this data sharing is acceptable; prefer self-service API-key setup and avoid sharing SMS codes in command lines.

Risk: Quota exhaustion can lead to payment and order requests.

Mitigation: Review plan, price, and payment details before ordering, and proceed only with explicit user consent.

Risk: API keys and query results may be stored locally in environment configuration, cache files, and linkfox session output files.

Mitigation: Avoid shell startup files unless plaintext local storage is acceptable, and treat generated JSON/cache files as sensitive workspace data.

Risk: Automatic feedback behavior may send feedback content to LinkFox.

Mitigation: Review or disable automatic feedback behavior before routine use where user comments or task context may be sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-junglescout-sales-estimates)
- [Jungle Scout ASIN sales estimate API reference](artifact/references/api.md)
- [Authentication and quota onboarding reference](artifact/references/onboarding.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance]

**Output Format:** [JSON response files and stdout summaries, with optional Markdown charts, tables, and setup commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries one ASIN per call, requires marketplace/start/end date inputs, excludes current or future end dates, consumes 64 compute credits, caches matching requests for 24 hours, and writes full responses under a local linkfox session data directory.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
