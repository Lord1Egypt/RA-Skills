## Description: <br>
Trades distribution-sum violations in chess tournament winner markets on Polymarket where player winner probabilities should sum to about 100%. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external trading-agent operators use this skill to discover chess tournament winner markets, check whether player probabilities violate the expected distribution total, and run simulated or explicitly enabled live Polymarket trades through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades using USDC. <br>
Mitigation: Start in paper mode, enable --live deliberately, keep position limits small, and use a low-funded or scoped key where possible. <br>
Risk: SIMMER_API_KEY is a sensitive trading credential. <br>
Mitigation: Store the key securely, avoid sharing it in prompts or logs, rotate it if exposed, and grant only the access needed for the intended trading mode. <br>
Risk: The documented SIMMER_MIN_VOLUME setting is declared but not enforced in the reviewed code. <br>
Mitigation: Manually check market liquidity before live use and keep trade sizes conservative until the volume gate is enforced. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-ladder-chess-tournament-trader) <br>
- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [Simmer SDK source repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls] <br>
**Output Format:** [Plain text execution logs and configured Python script behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live trading requires the --live flag and a SIMMER_API_KEY credential.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence; artifact frontmatter says 1.0.0 and clawhub.json says 0.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
