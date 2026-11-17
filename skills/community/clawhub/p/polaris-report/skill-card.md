## Description:

Polaris provides verified market and intelligence briefs, search, reports, entity data, and trading-oriented market signals from The Polaris Report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnytarrr](https://clawhub.ai/user/johnnytarrr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Polaris to fetch market intelligence, entity and news search results, ticker data, portfolio-aware briefs, and generated analysis reports from The Polaris Report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User inputs such as research queries, portfolio tickers and weights, strategy JSON, report requests, and submitted URLs are sent to api.thepolarisreport.com.

Mitigation: Avoid entering real portfolio allocations or URLs containing tokens, passwords, signed links, private document identifiers, or session material unless the publisher provides clearer privacy and retention guarantees.

Risk: The documentation says queries are not stored, but server security evidence says privacy and retention guarantees are not clear enough for sensitive inputs.

Mitigation: Review the publisher's privacy policy and restrict use to non-sensitive public research unless stronger retention terms are available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnnytarrr/skills/polaris-report)
- [The Polaris Report](https://thepolarisreport.com)
- [The Polaris Report API Reference](https://thepolarisreport.com/api-reference)
- [The Polaris Report SDKs and Integrations](https://thepolarisreport.com/developers)
- [The Polaris Report Privacy Policy](https://thepolarisreport.com/privacy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style text with command results, report summaries, tables, links, and status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include live API results, market data, generated briefs, report tiers, URLs, and rate-limit notices.]

## Skill Version(s):

2.4.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
