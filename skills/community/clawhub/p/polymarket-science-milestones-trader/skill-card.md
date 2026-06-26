## Description: <br>
Trades Polymarket prediction markets on scientific breakthroughs, Nobel Prizes, physics discoveries, and research milestones. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading agents use this skill to discover science-related Polymarket markets, apply configurable conviction and risk filters, and produce paper or explicitly enabled live trade decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real USDC trades when live mode is explicitly enabled. <br>
Mitigation: Start in paper mode, keep position limits conservative, and use --live only when intentionally accepting real trading risk. <br>
Risk: SIMMER_API_KEY grants trading authority and is a sensitive credential. <br>
Mitigation: Store SIMMER_API_KEY securely, limit access to trusted runtime environments, and rotate it if exposure is suspected. <br>
Risk: The skill depends on simmer-sdk for market access and trade execution. <br>
Mitigation: Review the simmer-sdk dependency before deployment and monitor dependency updates as part of normal release hygiene. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/polymarket-science-milestones-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub Repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console text and trading actions through simmer-sdk, with configuration via environment variables and tunables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket trading requires the --live flag and SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
