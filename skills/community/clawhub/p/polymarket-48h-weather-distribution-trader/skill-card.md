## Description: <br>
Trades mispricings in weather temperature-bin markets by reconstructing the implied probability distribution across bins for the same city and date, detecting sum violations and monotonicity breaks on cumulative markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading-system developers use this skill to analyze Polymarket weather temperature-bin markets, identify distribution-sum or cumulative monotonicity violations, and produce paper or live trade actions through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan verdict is suspicious and calls for human review before installation. <br>
Mitigation: Review the artifact and scan evidence before deployment, and install only when the trading workflow and requested permissions are intentional. <br>
Risk: The skill requires SIMMER_API_KEY, a high-value credential with trading authority. <br>
Mitigation: Use scoped credentials where possible, keep secrets out of prompts and logs, and rotate the key if exposure is suspected. <br>
Risk: Running with --live can place real Polymarket trades with USDC exposure. <br>
Mitigation: Keep the default paper mode until strategy behavior is reviewed, then set conservative position, spread, volume, and open-position tunables before live use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-48h-weather-distribution-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Console text with Simmer market queries and trade API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket execution requires SIMMER_API_KEY and the --live flag.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata; artifact frontmatter says 1.0.0 and clawhub.json says 0.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
