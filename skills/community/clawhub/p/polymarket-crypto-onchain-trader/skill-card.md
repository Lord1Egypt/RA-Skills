## Description: <br>
Trades Polymarket prediction markets on Bitcoin, Ethereum, Solana price milestones, ETF inflows, halving events, and DeFi protocol milestones, using ETF flow timing, BTC halving cycle phase, and Asian regulatory session windows to size conviction without an external data API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a configurable Polymarket crypto trading agent that discovers relevant markets, sizes positions from documented strategy heuristics, and places paper trades by default. Live trading is available only when the user explicitly enables it and provides the required Simmer API credential. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real USDC trades on Polymarket when enabled. <br>
Mitigation: Start in paper mode, review tunables, and use --live only after accepting the financial risk. <br>
Risk: SIMMER_API_KEY grants trading authority and is a sensitive credential. <br>
Mitigation: Use a revocable least-privilege key if available and store it only in the intended runtime secret environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-crypto-onchain-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Console logs, command-line execution, tunable configuration, and Simmer/Polymarket trade API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live trading requires SIMMER_API_KEY and the explicit --live flag.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
