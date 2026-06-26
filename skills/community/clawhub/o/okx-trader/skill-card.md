## Description: <br>
Automated OKX trading skill with dual-grid strategies, auto-rescaling, and account reporting for managing exchange orders and monitoring performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[esojourn](https://clawhub.ai/user/esojourn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and trading operators use this skill to maintain configured OKX grid strategies, generate PnL reports, and record daily account snapshots. It is intended for users who understand exchange API keys and the financial risks of automated crypto trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically place and cancel real OKX exchange orders, and live trading is the default when simulation is not enabled. <br>
Mitigation: Start with OKX_IS_SIMULATION=true, verify grid_settings.json instruments and order sizes, and enable schedules only after testing behavior. <br>
Risk: Exchange API credentials are required for account and trading operations. <br>
Mitigation: Use a trade-only OKX subaccount API key with withdrawals disabled and rotate credentials if they may have been exposed. <br>
Risk: Automated crypto grid strategies can lose money during volatile or trending markets. <br>
Mitigation: Limit maxPosition and grid sizes, monitor reports and snapshots, and trade only funds the operator can afford to lose. <br>


## Reference(s): <br>
- [OKX Trader on ClawHub](https://clawhub.ai/esojourn/okx-trader) <br>
- [Publisher profile](https://clawhub.ai/user/esojourn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON files, API calls] <br>
**Output Format:** [Markdown and console text reports, with JSON snapshot and audit files written under okx_data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OKX API credentials and local grid_settings.json to read market/account state and place or cancel configured orders.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
