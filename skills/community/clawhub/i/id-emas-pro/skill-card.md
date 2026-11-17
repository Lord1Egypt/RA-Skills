## Description:

Checks Indonesian gold prices, compares supported brands, manages price alerts, tracks portfolios and history, and can request Kimi-based analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rhaone21](https://clawhub.ai/user/rhaone21)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to monitor Indonesian retail gold prices, compare brands, configure threshold alerts, maintain simple portfolio/history records, and request AI-assisted market summaries.

### Deployment Geography for Use:

Global, for users monitoring Indonesian gold markets

## Known Risks and Mitigations:

Risk: Broad local authority could expose more filesystem access than the fixed price, alert, portfolio, and history scripts require.

Mitigation: Grant execution only to the known Node scripts and avoid broad filesystem permissions in shared or multi-user deployments.

Risk: The skill stores user-linked alert thresholds, history, and portfolio records in plaintext runtime files.

Mitigation: Protect the .data directory with restrictive permissions and avoid shared installations for sensitive holdings or alert data.

Risk: AI analysis can send price and history context to Moonshot/Kimi when the AI tier and API key are enabled.

Mitigation: Enable the AI tier only after confirming that this external API use is acceptable, and protect KIMI_API_KEY as a secret.

Risk: Scraped prices can become stale or unavailable if upstream gold-price sites change or are unreachable.

Mitigation: Show scrape time or cache status to users and treat stale fallback prices as informational rather than authoritative trading advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rhaone21/skills/id-emas-pro)
- [API Sources for Gold Prices](references/api-sources.md)
- [Antam Logam Mulia gold prices](https://www.logammulia.com/id/harga-emas-hari-ini)
- [Pegadaian gold prices](https://www.pegadaian.co.id/harga-emas)
- [Harga-Emas.org](https://harga-emas.org/)
- [Moonshot Kimi platform](https://platform.moonshot.cn)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Markdown responses with inline shell commands and JSON records from supporting scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bahasa Indonesia user-facing responses, IDR-per-gram price values, alert notifications, portfolio/history records, and optional Kimi analysis when configured]

## Skill Version(s):

1.3.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
