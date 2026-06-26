## Description: <br>
Builds a custom fear index from Polymarket markets by aggregating geopolitical escalation, falling crypto, extreme weather, and disease signals, then uses the index to identify oversold or overpriced prediction markets for paper or explicit live trading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading automation operators use this skill to evaluate Polymarket markets through a macro fear-index strategy, tune risk controls, and run simulated trades by default or live trades only when explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket trades and create financial exposure. <br>
Mitigation: Run in paper mode first and use --live only when the operator accepts real trading risk. <br>
Risk: The skill requires a sensitive SIMMER_API_KEY credential. <br>
Mitigation: Use a limited or segregated API key where possible and keep the credential private. <br>
Risk: The runtime depends on simmer-sdk for market access and trade execution. <br>
Mitigation: Review the simmer-sdk dependency before trusting live credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-macro-fear-index-trader) <br>
- [Publisher profile](https://clawhub.ai/user/diagnostikon) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk source](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation, Python command-line execution, and runtime trade logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading unless --live is supplied.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
