## Description:

OKX Exchange is a quantitative trading agent for OKX that supports market data queries, account and portfolio views, order execution, automated strategies, risk monitoring, performance reports, and liquidation alerts across spot, USDT-M perpetual swaps, and coin-M futures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lk2023060901](https://clawhub.ai/user/lk2023060901)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to operate OKX trading workflows through an agent, including market analysis, portfolio inspection, order placement, strategy execution, monitoring, and reporting. It can affect real trading accounts when configured with live credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle live OKX API credentials and place real trades.

Mitigation: Start in demo mode, use withdrawal-disabled and IP-restricted API keys, keep live credentials separate, and confirm all live-mode changes before use.

Risk: Automated execution can bypass prompts through auto-trading settings or no-confirm flags.

Mitigation: Keep `auto_trade` disabled and avoid `--no-confirm` unless independent order, position, and daily trade limits are configured and reviewed.

Risk: Scheduled monitoring jobs can repeatedly scan markets or close positions without an interactive review.

Mitigation: Review every cron job before enabling it, use conservative intervals, and tear down scheduled jobs when active monitoring is no longer intended.

Risk: Changing `OKX_API_URL` can redirect API traffic away from the standard OKX endpoint.

Mitigation: Leave `OKX_API_URL` unset unless the endpoint has been independently verified and the environment file is access-controlled.

## Reference(s):

- [OKX API V5 Documentation](https://www.okx.com/docs-v5/en/)
- [OKX API Base URL](https://www.okx.com)
- [ClawHub Skill Page](https://clawhub.ai/lk2023060901/skills/okx-exchange)
- [Trading Rules](artifact/docs/trading-rules.md)
- [Decision Engine Guide](artifact/docs/decision-engine-guide.md)
- [Learning System Data Management](artifact/docs/learning-system-data-management.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with command examples, configuration snippets, and script-generated trading reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live OKX account data, market data, trade execution results, monitoring output, and generated reports when credentials are configured.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
