## Description: <br>
Trades cross-asset correlation divergences in 5-minute crypto "Up or Down" markets on Polymarket. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to scan short-duration Polymarket crypto markets for cross-asset divergence signals, then produce simulated or live trade actions according to configured limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place autonomous real-money USDC trades when run with --live. <br>
Mitigation: Start in paper mode, use conservative position limits, and enable --live only when real-money trading is intended. <br>
Risk: SIMMER_API_KEY grants trading authority. <br>
Mitigation: Use a dedicated least-privilege key where available and protect it as a sensitive credential. <br>
Risk: SIMMER_MIN_VOLUME is declared as a tunable, but the reviewed code does not appear to enforce a volume check. <br>
Mitigation: Do not rely on SIMMER_MIN_VOLUME as an active liquidity guard; review market liquidity separately or update the implementation before live use. <br>


## Reference(s): <br>
- [Polymarket 24h Cross Asset Sync Trader](https://clawhub.ai/diagnostikon/polymarket-24h-cross-asset-sync-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Console text and trade API requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading unless explicitly run with --live.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
