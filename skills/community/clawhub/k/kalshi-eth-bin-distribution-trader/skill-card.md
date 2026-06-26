## Description: <br>
Trades ETH price bin markets on Kalshi by identifying bin groups whose probabilities deviate from the 100% sum constraint and trading mispriced bins toward rebalance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading agents use this skill to analyze Kalshi ETH price bin markets, surface mispricing from distribution-sum deviations, and optionally execute trades with configured risk limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real financial trades using sensitive trading credentials. <br>
Mitigation: Start in dry-run mode, review the skill and dependency behavior before using --live, and use limited credentials with a dedicated low-balance wallet. <br>
Risk: The skill depends on simmer-sdk and requires SIMMER_API_KEY, with SOLANA_PRIVATE_KEY needed for live trading. <br>
Mitigation: Review the dependency source before providing live credentials and keep credentials private, scoped, and separate from primary accounts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/kalshi-eth-bin-distribution-trader) <br>
- [Simmer Skills](https://simmer.markets/skills) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API calls, Guidance] <br>
**Output Format:** [Console text with optional JSON automaton summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to dry-run mode; live trading requires explicit --live plus configured trading credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
