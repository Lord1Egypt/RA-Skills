## Description:

Read-only Interactive Brokers (IBKR) diagnostics as portable AI-agent skills: account health, positions, daily P&L, trade history, dividends, options Greeks, and a P0-P3 graded portfolio report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luyangkk](https://clawhub.ai/user/luyangkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers with Interactive Brokers accounts use this skill to configure read-only access, inspect account, position, P&L, trade, dividend, and options data, and generate portfolio diagnostics without placing orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flex history and dividend workflows can expose sensitive Flex tokens, Query IDs, or account details if credentials are passed through command text, environment variables, logs, or screenshots.

Mitigation: Use the stdin-based Flex configurator, avoid command-line or environment-variable token handling, and never echo or share tokens, Query IDs, account numbers, raw XML, or service URLs.

Risk: Local configuration, snapshots, reports, and raw Flex output may contain sensitive financial data.

Mitigation: Keep `.ib-suite/config.yaml`, data lake files, generated reports, and Flex output in ignored workspace-local storage and review carefully before sharing or committing anything.

Risk: The release security evidence flags unsafe Flex credential handling that needs review before installation.

Mitigation: Review the Flex workflows before installing, avoid the documented `ib-gateway` Python one-liner for Flex, and prefer the safer trade-history or dividend configurator flow.

Risk: Dependency versions and Flex download host validation may need additional hardening for production use.

Mitigation: Add dependency locks, review dependencies before installation, and validate Flex Web Service hosts before using the online retrieval paths.

Risk: Enabling option market-data retrieval for Greeks or implied volatility may incur IBKR snapshot charges for symbols without a real-time subscription.

Mitigation: Keep option market-data fetching disabled unless the user explicitly accepts the cost risk and understands the account's IBKR market-data subscriptions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luyangkk/skills/ib-suite)
- [Trade History Flex Query Setup](artifact/ib-trade-history/flex-query-setup.md)
- [Dividend Income Flex Query Setup](artifact/ib-dividend-income/flex-query-setup.md)
- [IBKR Activity Flex Query Guide](https://www.ibkrguides.com/clientportal/performanceandstatements/activityflex.htm)
- [IBKR Flex Web Service Setup](https://www.ibkrguides.com/brokerportal/performanceandstatements/flex-web-service.htm)
- [IBKR Flex Web Service API](https://www.interactivebrokers.com/campus/ibkr-api-page/flex-web-service/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON, Markdown, files]

**Output Format:** [Markdown guidance with bash commands, JSON results, report files, and charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include sensitive financial account data and should remain workspace-local.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
