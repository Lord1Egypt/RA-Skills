## Description: <br>
Tracks stock prices and company news from Google Finance on a schedule, with watchlists, alerts, and heuristic BUY/HOLD/SELL signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mli-cj](https://clawhub.ai/user/mli-cj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to monitor a stock watchlist, fetch Google Finance quote data, review price changes and company news, and produce informational stock reports or scheduled alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker symbols are queried against public finance sites and saved in a local OpenClaw state file. <br>
Mitigation: Install only when that data handling is acceptable, and review or delete the local watchlist state when it is no longer needed. <br>
Risk: BUY/SELL signals are heuristic informational output and may be incorrect or misleading. <br>
Mitigation: Treat reports as non-financial-advice summaries and verify decisions with independent financial analysis. <br>
Risk: Cron or Slack reporting can create recurring stock reports after setup. <br>
Mitigation: Enable scheduled reports only intentionally and review the configured cadence and recipients before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mli-cj/google-finance) <br>
- [Google Finance](https://finance.google.com) <br>
- [Stock Analysis Framework](references/analysis-framework.md) <br>
- [Data Sources Reference](references/data-sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, CLI text output, and optional JSON from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include price, change percentage, signal, confidence, score, factors, optional headlines, and a not-financial-advice disclaimer.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
