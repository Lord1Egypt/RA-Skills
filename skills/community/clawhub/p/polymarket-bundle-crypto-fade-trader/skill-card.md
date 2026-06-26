## Description: <br>
Fades strong directional moves in Polymarket 5-minute BTC, ETH, and SOL interval markets using streak detection and conviction-based position sizing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading-agent operators use this skill to scan Polymarket crypto interval markets for short-horizon momentum-fade opportunities and run the strategy in paper mode or, after explicit opt-in, live mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required SIMMER_API_KEY grants trading authority and live mode can place real-money Polymarket trades. <br>
Mitigation: Keep paper mode enabled until review is complete, protect the credential as sensitive, and only use the --live flag with position, volume, spread, and open-position limits set appropriately. <br>
Risk: Security evidence reports an apparent trade-direction ambiguity that could cause unintended YES or NO actions. <br>
Mitigation: Verify the YES/NO direction mapping in paper mode against known market outcomes before enabling live trading or increasing position size. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/polymarket-bundle-crypto-fade-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk GitHub Repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and runtime configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runtime script prints market-discovery, skip, and trade-status messages and can submit simulated or live trade requests through the configured trading SDK.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
