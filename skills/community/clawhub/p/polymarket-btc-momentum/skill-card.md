## Description: <br>
Trades Polymarket Bitcoin 5-minute sprint markets using real-time BTC price momentum from Binance, buying YES when momentum is bullish and NO when bearish. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azvn2610](https://clawhub.ai/user/azvn2610) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading agents use this skill to evaluate short-term BTC momentum, select active Polymarket Bitcoin sprint markets, and run paper or live trades with configured safeguards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Enabling live mode can place automated real-money prediction-market trades that may lose funds. <br>
Mitigation: Run in dry-run mode first, use a restricted Simmer or Polymarket key where possible, keep trade amounts low, and enable --live only after accepting the financial risk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/azvn2610/polymarket-btc-momentum) <br>
- [Binance klines API](https://api.binance.com/api/v3/klines) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Python script and Markdown usage guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY, simmer-sdk, requests, and network access to Binance and Polymarket/Simmer services.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
