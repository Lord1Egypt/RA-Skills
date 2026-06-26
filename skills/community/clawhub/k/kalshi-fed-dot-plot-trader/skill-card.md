## Description: <br>
Trades Fed rate markets on Kalshi by comparing market prices with FOMC dot-plot-implied cut or hike probabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to evaluate Kalshi Fed rate markets, run dry-run opportunity checks, and optionally execute constrained live trades when configured with credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real-money Kalshi trades using wallet and trading credentials. <br>
Mitigation: Run dry-run first, enable --live only intentionally, and use a dedicated low-balance wallet with a constrained API key. <br>
Risk: The skill depends on simmer-sdk and market execution services before using live credentials. <br>
Mitigation: Review or pin simmer-sdk before supplying credentials, and keep position size, max trades, slippage, and liquidity limits conservative. <br>
Risk: The default strategy uses a static dot plot signal that can become stale or diverge from current market expectations. <br>
Mitigation: Review and update the dot plot assumptions with current SEP, Fed funds futures, or OIS-implied data before relying on live trades. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/kalshi-fed-dot-plot-trader) <br>
- [Simmer Markets Skills](https://simmer.markets/skills) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk Repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [CLI text output with optional JSON automaton reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to dry-run; live trading requires --live, SIMMER_API_KEY, and SOLANA_PRIVATE_KEY.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
