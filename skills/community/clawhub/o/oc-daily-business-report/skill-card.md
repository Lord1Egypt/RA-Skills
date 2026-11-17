## Description:

Generate daily business briefings from multiple data sources, aggregating weather, crypto prices, news headlines, system health, and calendar events into a formatted morning report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariusfit](https://clawhub.ai/user/mariusfit)

### License/Terms of Use:

MIT

## Use Case:

Employees, operators, and business teams use this skill to generate scheduled morning briefings or status reports from weather, cryptocurrency, news, quote, and local system-health sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured NewsData.io API key can be stored and printed in plaintext.

Mitigation: Avoid using real API keys until secret handling is improved, or use a low-privilege key and remove it from generated output before sharing.

Risk: Scheduled reports can include local disk and RAM status.

Mitigation: Review cron recipients and sharing destinations before enabling scheduled delivery.

Risk: Reports depend on live third-party public APIs and may contain stale, unavailable, or incomplete data.

Mitigation: Review generated reports before business use and treat failed sections or fallback content as incomplete data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mariusfit/skills/oc-daily-business-report)
- [wttr.in weather endpoint](https://wttr.in/{city}?format=j1)
- [CoinGecko simple price endpoint](https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies={currency}&include_24hr_change=true)
- [NewsData.io latest news endpoint](https://newsdata.io/api/1/latest?apikey={api_key}&country={country}&language=en&size=5)
- [Quotable random quote endpoint](https://api.quotable.io/quotes/random?limit=1)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Plain text, Markdown, or JSON reports; configuration and test commands are provided as shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include live public API data, optional NewsData.io headlines, and local disk/RAM status.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
