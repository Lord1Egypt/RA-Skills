## Description: <br>
Trades Polymarket prediction markets focused on supply chain disruptions, port congestion, shipping delays, commodity prices, and logistics outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to discover and optionally trade supply-chain, logistics, shipping, commodity, and related prediction markets on Polymarket through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This is live-capable financial trading automation, and the security review notes that its documented safety limits do not match the runnable code. <br>
Mitigation: Use paper mode first, verify the actual Simmer tunables, and do not enable live trading until documented and runnable limits are reconciled. <br>
Risk: The skill requires a Simmer API key that may authorize trading activity. <br>
Mitigation: Keep the credential private, avoid live-capable keys in shared environments, and provide only the minimum authority needed for the intended mode. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-supply-chain-trader) <br>
- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [Simmer SDK source](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Console text, environment configuration, and Simmer SDK trading calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading unless live execution is explicitly requested.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata; artifact frontmatter says 1.0 and clawhub.json says 0.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
