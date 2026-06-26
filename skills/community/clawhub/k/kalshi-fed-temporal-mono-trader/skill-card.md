## Description: <br>
Scans Kalshi Fed rate markets for temporal monotonicity violations and can propose or execute bounded trades through Simmer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading automation operators use this skill to inspect Kalshi Fed rate markets for date-ordering price inconsistencies, run dry-run opportunity checks, and optionally execute live trades after configuring credentials and risk limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can spend real USDC and requires sensitive trading and wallet credentials. <br>
Mitigation: Run in dry-run mode first, use a dedicated low-balance wallet and restricted trading key, and enable live mode only after reviewing position limits and exit behavior. <br>
Risk: The skill depends on simmer-sdk for trading integration. <br>
Mitigation: Review the simmer-sdk dependency before providing live credentials. <br>
Risk: Automated scheduling could repeatedly act on market signals if configured for live operation. <br>
Mitigation: Do not pass --live or configure scheduling unless the configured trade caps, slippage limit, and exit threshold match the operator's risk tolerance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/kalshi-fed-temporal-mono-trader) <br>
- [Simmer skills homepage](https://simmer.markets/skills) <br>
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>
- [simmer-sdk PyPI package](https://pypi.org/project/simmer-sdk/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API calls, shell commands, configuration] <br>
**Output Format:** [Console text with optional automaton JSON status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run output is available by default; live execution can place real USDC trades when explicitly enabled.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
