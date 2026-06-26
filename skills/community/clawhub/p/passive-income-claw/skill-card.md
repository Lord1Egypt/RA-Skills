## Description: <br>
Binance passive income assistant that scans Simple Earn opportunities, recommends direct and borrow-to-earn strategies, and can execute subscriptions or redemptions within configured limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pipi6688](https://clawhub.ai/user/pipi6688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ClawHub/OpenClaw users use this skill to connect Binance API credentials, scan Earn products, compare direct and borrow-to-earn paths, and manage subscribe or redeem actions under local authorization limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Binance API credentials to subscribe, redeem, and optionally create margin borrowing exposure. <br>
Mitigation: Use API keys with withdrawals, futures, and spot trading disabled; enable margin only when borrowing risk is intentional. <br>
Risk: Auto mode can execute recommended Earn subscriptions from scheduled scans. <br>
Mitigation: Keep confirm-first mode unless automated execution is desired, and review single-operation limits, daily limits, allowed operations, and the asset whitelist before enabling auto mode. <br>
Risk: Borrow-to-earn paths can lose money through variable borrow rates, collateral price drops, liquidation risk, or failed chained execution. <br>
Mitigation: Require positive net yield, margin level above 2.0, dual authorization checks for borrow and subscribe, and immediate repayment handling if borrowing succeeds but Earn subscription fails. <br>
Risk: Local profile, snapshot, and execution-log files affect what the agent can recommend or execute. <br>
Mitigation: Review the local profile limits, snapshot, cron configuration, and execution log regularly. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/pipi6688/passive-income-claw) <br>
- [Publisher profile](https://clawhub.ai/user/pipi6688) <br>
- [Binance API management](https://www.binance.com/en/my/settings/api-management) <br>
- [Binance API endpoint](https://api.binance.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local profile, snapshot, and execution-log files; deterministic helper scripts emit JSON to stdout and errors to stderr.] <br>

## Skill Version(s): <br>
0.7.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
