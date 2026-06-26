## Description: <br>
Find arbitrage opportunities across Polymarket and Kalshi prediction markets via AIsa API by scanning sports markets for cross-platform price discrepancies, comparing real-time odds, and checking orderbook liquidity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to inspect prediction market pricing across Polymarket and Kalshi, identify possible arbitrage spreads, and review liquidity before deciding whether an opportunity is actionable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports under-disclosed wallet and financial lookup commands beyond the advertised arbitrage workflow. <br>
Mitigation: Review commands before use, run only the market or wallet queries needed for the task, and query wallet addresses only when authorized. <br>
Risk: Queries and wallet identifiers supplied by the user are sent to api.aisa.one. <br>
Mitigation: Use a limited AIsa API key, avoid submitting sensitive or unauthorized wallet data, and expect provided query values to be processed by AIsa. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/prediction-market-arbitrage-api) <br>
- [AIsa API Reference](https://docs.aisa.one/reference/) <br>
- [AIsa](https://aisa.one) <br>
- [Polymarket](https://polymarket.com) <br>
- [Kalshi](https://kalshi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; commands query the AIsa API over HTTPS and do not execute trades.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
