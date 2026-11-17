## Description:

Query real-time and historical financial data for equities, including prices, news, financial statements, metrics, analyst estimates, insider and institutional activity, SEC filings, earnings press releases, segmented revenues, stock screening, and macro interest rates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-research agents use this skill to retrieve equity market data, financial filings, company fundamentals, analyst estimates, ownership activity, stock screens, and macro interest-rate data through the AIsa API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an AISA_API_KEY to call AIsa market-data endpoints.

Mitigation: Use a dedicated least-privilege API key where available, store it in an environment variable or secrets manager, and avoid pasting it into prompts or shared logs.

Risk: Ticker symbols, watchlists, screener filters, and similar market-research parameters are sent to AIsa's API.

Mitigation: Review requests before execution and avoid sending sensitive portfolio notes unless they are necessary for the task.

Risk: Some endpoint coverage is limited, and unsupported tickers can return errors.

Mitigation: Check API responses for errors and verify critical market data against an authoritative source before using it for decisions.

## Reference(s):

- [Marketpulse on ClawHub](https://clawhub.ai/aisadocs/skills/marketpulse)
- [AIsa API Reference](https://aisa.one/docs/api-reference/)
- [AIsa](https://aisa.one)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with shell commands, curl examples, Python CLI usage, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and AISA_API_KEY; API calls send requested market-data parameters to AIsa.]

## Skill Version(s):

1.0.2 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
