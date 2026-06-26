## Description: <br>
Trades Polymarket prediction markets for music streaming milestones, chart performance, awards, tour revenue, and industry deals using entertainment-market signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to discover music and entertainment Polymarket markets, generate buy/sell decisions, and execute paper trades by default or live trades only when explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real-money trading can execute when live mode is explicitly enabled, and server security evidence says the real-money safety limits need review before use. <br>
Mitigation: Start in paper mode, review all tunables yourself, use a limited-balance or scoped key where available, and enable live trading only when prepared for real USDC trades. <br>
Risk: The skill requires a sensitive SIMMER_API_KEY credential. <br>
Mitigation: Keep the credential private, avoid placing live-capable keys in automated environments, and scope or rotate the key according to the trading venue's controls. <br>
Risk: The configured defaults in the artifact and documentation do not fully align for some trading limits. <br>
Mitigation: Set SIMMER_MIN_DAYS, SIMMER_MIN_VOLUME, position limits, and trade thresholds explicitly before scheduling or live execution. <br>


## Reference(s): <br>
- [Spotify Charts](https://charts.spotify.com/charts/overview/global) <br>
- [Billboard Charts](https://www.billboard.com/charts/) <br>
- [Chartmetric](https://chartmetric.com/) <br>
- [RIAA Gold & Platinum Database](https://www.riaa.com/gold-platinum/) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline commands and runtime text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading and uses live trading only when explicitly invoked.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
