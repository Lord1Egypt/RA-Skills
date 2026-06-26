## Description: <br>
Detects cross-asset divergence in Polymarket crypto 5-minute interval markets and trades follower-coin convergence toward BTC direction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading automation developers use this skill to monitor Polymarket crypto interval markets for BTC-versus-follower-coin candle divergence and place simulated or explicitly enabled live convergence trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades and create financial loss. <br>
Mitigation: Start in paper mode, enable --live only intentionally, and keep position limits at amounts the user is prepared to risk. <br>
Risk: SIMMER_API_KEY grants trading authority and is a high-value credential. <br>
Mitigation: Store the key only in a protected runtime environment, avoid logging it, and rotate it if exposure is suspected. <br>
Risk: The skill depends on simmer-sdk for market access and trade execution. <br>
Mitigation: Review and install the dependency from trusted package sources before running trading automation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/polymarket-candle-cross-asset-divergence-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub Repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Console logs with Simmer market queries and simulated or live trade API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket trades require SIMMER_API_KEY and the --live flag.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
