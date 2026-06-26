## Description: <br>
Trades distribution-sum violations and local anomaly signals in social media post-count range markets on Polymarket. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and developers use this skill to evaluate and automate a configurable Polymarket strategy for social media post-count range markets. It supports paper trading by default and can place live USDC trades only when explicitly launched in live mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades using USDC. <br>
Mitigation: Keep the skill in paper mode until reviewed, and use live mode only when prepared for real trades. <br>
Risk: SIMMER_API_KEY grants trading authority and is a sensitive credential. <br>
Mitigation: Store the key securely and use the least-privileged Simmer key available. <br>
Risk: Automated strategy settings can create unintended position or liquidity exposure. <br>
Mitigation: Review tunables such as max position, max open positions, minimum volume, spread, and trade thresholds before live trading. <br>


## Reference(s): <br>
- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [Simmer SDK GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and Python runtime output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading unless live mode is explicitly enabled.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
