## Description: <br>
A bilingual Polymarket prediction-market toolkit for market scanning, probability assessment, order-book analysis, live trading, position monitoring, resolution tracking, backtesting, and portfolio review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donkeylmx](https://clawhub.ai/user/donkeylmx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill bundle to analyze Polymarket opportunities, simulate or execute trades, review portfolio exposure, monitor positions, and track market resolution criteria. It is appropriate only when the user intentionally wants agent-assisted prediction-market trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The toolkit can place real-money Polymarket trades, including autonomous trading through the danger auto-trade workflow. <br>
Mitigation: Use dry-run or paper-trading mode first, set low per-trade and total limits, and avoid unattended live trading unless explicitly intended. <br>
Risk: Trading workflows require wallet private keys, funder addresses, and may use CLOB credentials. <br>
Mitigation: Use a dedicated low-balance wallet, keep credentials out of shared logs and prompts, and rotate or revoke credentials if exposure is suspected. <br>
Risk: Cancel-all and live order operations can affect existing market positions and pending orders. <br>
Mitigation: Review order IDs, portfolio state, and cancel-all behavior before execution, especially when multiple active orders exist. <br>
Risk: The toolkit persists trading reports, portfolio data, monitoring output, and history under local Polymarket report paths. <br>
Mitigation: Treat generated files as sensitive financial records and remove or protect them when sharing the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/donkeylmx/polymarket-trade-assistant) <br>
- [ClawHub package homepage](https://clawhub.ai/skills/polymarket-trade-skills) <br>
- [CLOB trading API reference](artifact/api-trade-polymarket/references/clob-trading-api.md) <br>
- [Environment setup reference](artifact/api-trade-polymarket/references/env-setup.md) <br>
- [Auto-trade risk controls](artifact/danger-auto-trade-polymarket/references/risk-controls.md) <br>
- [Market pulse analysis framework](artifact/polymarket-market-pulse/references/analysis-framework.md) <br>
- [Position alert thresholds](artifact/poly-position-monitor/references/alert-thresholds.md) <br>
- [Resolution trackability framework](artifact/poly-resolution-tracking/references/trackability-framework.md) <br>
- [Paper-trading portfolio schema](artifact/polymarket-paper-trading/references/portfolio-schema.md) <br>
- [Portfolio review framework](artifact/portfolio-review-polymarket/references/review-framework.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON command results, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local Polymarket report, portfolio, monitoring, and trading-history files.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
