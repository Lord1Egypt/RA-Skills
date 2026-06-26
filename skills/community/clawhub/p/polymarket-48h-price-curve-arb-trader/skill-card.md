## Description: <br>
Trades structural mispricings in crypto price-threshold markets by reconstructing the implied probability distribution curve across multiple strike levels and detecting mathematical violations such as monotonicity breaks and range-sum inconsistencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading automation developers use this skill to scan Polymarket crypto price-threshold markets for internally inconsistent probability curves and place paper or explicitly live trades through Simmer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real-money Polymarket trades when run with --live. <br>
Mitigation: Test in paper mode first and use --live only after deliberately accepting live trading risk. <br>
Risk: SIMMER_API_KEY grants trading authority and is a sensitive credential. <br>
Mitigation: Protect and scope the credential before deployment. <br>
Risk: The skill depends on simmer-sdk for market access and trade execution. <br>
Mitigation: Review or pin simmer-sdk before live use. <br>
Risk: The documented minimum-volume control appears declared but not implemented in the script. <br>
Mitigation: Review the volume filter behavior before relying on it as a live trading safeguard. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-48h-price-curve-arb-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk source repository](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console text with trading decisions, skip reasons, and order status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to paper trading unless run with --live.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
