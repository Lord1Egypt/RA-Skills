## Description: <br>
Compares CME FedWatch implied rate probabilities to Kalshi Fed rate decision market prices and trades when divergence exceeds threshold. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and advanced trading agents use this skill to compare FedWatch-implied rate-cut probabilities with Kalshi Fed rate market prices, surface divergence, and optionally place constrained trades. It is intended for users who can manage real-money prediction-market and wallet risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real USDC trades through the configured trading venue. <br>
Mitigation: Start in dry-run mode, use --live only intentionally, and use a dedicated low-balance wallet with a scoped Simmer API key. <br>
Risk: The default FedWatch probabilities are static and may become stale. <br>
Mitigation: Verify or replace the FedWatch probability inputs before live use. <br>
Risk: The skill depends on simmer-sdk and external market APIs for discovery, context, and execution. <br>
Mitigation: Review simmer-sdk and required credentials if full auditability is needed before deploying with live funds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/kalshi-fed-futures-arb-trader) <br>
- [Publisher profile](https://clawhub.ai/user/diagnostikon) <br>
- [Simmer skills homepage](https://simmer.markets/skills) <br>
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>
- [simmer-sdk PyPI package](https://pypi.org/project/simmer-sdk/) <br>
- [CME FedWatch Tool](https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Console text with optional JSON automaton report and Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to dry-run mode; live execution requires an explicit --live flag and configured credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
