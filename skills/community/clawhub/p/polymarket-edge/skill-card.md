## Description: <br>
Trade and analyse Polymarket prediction markets with a 5-minute BTC EMA crossover strategy. Browse markets, read order books, run signals, manage a live auto-trader, and view portfolio positions. Billed per-call via SkillPay.me (0.001 USDT / call, BNB Chain USDT). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icloud-git](https://clawhub.ai/user/icloud-git) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use this skill to inspect Polymarket prediction markets, retrieve market data, run BTC EMA crossover signals, and optionally operate a live auto-trader with billing enforced per API call. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes an embedded SkillPay billing API key. <br>
Mitigation: Remove the embedded key, rotate it before use, and require billing credentials to come only from secure environment configuration. <br>
Risk: Automated trading can place real-money market orders when live trading is enabled. <br>
Mitigation: Keep auto_trade disabled unless wallet isolation, spend limits, monitoring, and a clear stop procedure are in place. <br>
Risk: Exposing the FastAPI service to untrusted callers could allow billed requests or trading controls to be invoked by others. <br>
Mitigation: Run the service behind trusted access controls and avoid public exposure without authentication and operational safeguards. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/icloud-git/polymarket-edge) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/icloud-git) <br>
- [SkillPay billing API](https://skillpay.me/api/v1/billing) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>
- [Polymarket CLOB API](https://clob.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, api responses, market analysis, trading guidance] <br>
**Output Format:** [JSON API responses with market data, order book details, strategy signals, auto-trader status, billing balances, and portfolio summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Billed endpoints require a user_id; optional live trading requires an EVM private key and separate order-placement setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
