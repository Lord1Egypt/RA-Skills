## Description: <br>
Find a high-volume BTC-related Polymarket priced between 40% and 60%, buy 1 USD of YES, hold for 5 minutes, sell, wait 5 minutes, and repeat until 10 completed buy cycles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skybinjf](https://clawhub.ai/user/skybinjf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators can use this skill to run a configurable Polymarket BTC-market trading loop, previewing it in dry-run mode before optionally enabling live orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket orders using wallet credentials. <br>
Mitigation: Run dry-run first, use a dedicated low-balance wallet, and provide WALLET_PRIVATE_KEY only when live trading is intentional. <br>
Risk: Automated trading parameters can create repeated exposure across multiple buy cycles. <br>
Mitigation: Keep BUY_USD and MAX_BUYS small until behavior is verified for the intended market and account. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/skybinjf/polymarket-5m-trading) <br>
- [Polymarket CLOB Endpoint](https://clob.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and environment variable guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to dry-run; live trading requires --live and WALLET_PRIVATE_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
