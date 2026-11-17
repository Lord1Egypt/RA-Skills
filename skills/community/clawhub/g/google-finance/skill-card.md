## Description:

Track stock prices and company news from Google Finance on a schedule for watchlists, alerts, and heuristic BUY/HOLD/SELL signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mli-cj](https://clawhub.ai/user/mli-cj)

### License/Terms of Use:


## Use Case:

Developers and external OpenClaw users use this skill to monitor stock watchlists, fetch Google Finance price data, generate heuristic BUY/HOLD/SELL reports, and set scheduled stock alerts. Its outputs are informational and not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock symbols requested by the user are sent to Google Finance and possibly fallback finance or news sources described in the references.

Mitigation: Install only if that disclosure is acceptable, and review configured fallback sources before use.

Risk: BUY/HOLD/SELL signals, stop-loss values, and target prices are simple heuristics that may be incorrect or misleading.

Mitigation: Treat outputs as informational only, not as professional financial advice or automated trading instructions.

Risk: Cron and Slack announcement examples can distribute stock reports automatically.

Mitigation: Review schedules, channels, recipients, and generated command text before enabling recurring reports.

## Reference(s):

- [Stock Analysis Framework](references/analysis-framework.md)
- [Data Sources Reference](references/data-sources.md)
- [Google Finance](https://finance.google.com)
- [Google Finance quote endpoint pattern](https://www.google.com/finance/quote/*)
- [ClawHub skill page](https://clawhub.ai/mli-cj/skills/google-finance)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style stock reports and optional JSON output; setup guidance includes shell commands for scheduled checks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include symbol, price, percent change, heuristic signal, confidence, score, alerts, and a financial-advice disclaimer.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
