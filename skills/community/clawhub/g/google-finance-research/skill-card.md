## Description:

Retrieves Google Finance quotes, company details, charts, financials, news, related instruments, and market snapshots through Crawlora for sourced market research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and developers use this skill to gather source-attributed public market snapshots and compare identified instruments. It does not place trades or manage portfolios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup terms and the API key are sent to Crawlora's API.

Mitigation: Use only for public market research; omit personal, account, portfolio, and confidential business information from queries, and use a key only if comfortable with this transfer.

Risk: Market snapshots may be stale or mistaken for actionable trading guidance.

Mitigation: Preserve source and collection times, mark unknown freshness, and do not use this skill for trades or account actions.

## Reference(s):

- [Google Finance endpoint reference](artifact/reference/endpoints.md)
- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/google-finance-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Markdown market briefs and comparison tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source attribution, exchange-qualified identifiers, collection times, and missing-data or freshness caveats where relevant.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
