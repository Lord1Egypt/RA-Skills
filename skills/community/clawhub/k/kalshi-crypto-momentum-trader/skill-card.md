## Description: <br>
Uses 7-day and 30-day price trend extrapolation to trade crypto year-end price target markets on Kalshi. Requires SIMMER_API_KEY and simmer-sdk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to identify and optionally execute Kalshi crypto year-end target trades based on 7-day and 30-day momentum signals. It is dry-run by default and requires live credentials before real trades can execute. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real trades and uses high-value trading and wallet credentials. <br>
Mitigation: Start in dry-run mode, use a dedicated low-balance wallet and limited trading API key for live runs, and pass --live only after reviewing the configuration. <br>
Risk: Automated trading behavior depends on the simmer-sdk dependency and configurable position and trade limits. <br>
Mitigation: Review or pin simmer-sdk, keep max position and max trades conservative, and adjust tunables before enabling live trading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/kalshi-crypto-momentum-trader) <br>
- [Publisher profile](https://clawhub.ai/user/diagnostikon) <br>
- [Simmer skills homepage](https://simmer.markets/skills) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output, JSON automaton reports, and Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run by default; live execution requires --live plus SIMMER_API_KEY and SOLANA_PRIVATE_KEY credentials.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
