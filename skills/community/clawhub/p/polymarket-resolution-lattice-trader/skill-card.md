## Description: <br>
Trades Polymarket markets by detecting logical inconsistencies between related contracts such as earlier-vs-later deadlines and prerequisite-vs-downstream event chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading agents use this skill to identify cross-market probability inconsistencies on Polymarket and run a configurable strategy that defaults to paper trading. It is intended for users who can review market logic, tune risk parameters, and explicitly approve any live execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can spend real USDC on Polymarket. <br>
Mitigation: Keep the skill in paper mode during review and require explicit human approval before any run with --live. <br>
Risk: SIMMER_API_KEY grants trading authority and is a high-value credential. <br>
Mitigation: Store the key only in the intended secret manager or runtime environment and avoid exposing it in logs, prompts, or shared files. <br>
Risk: Cross-market parsing and logical rules may identify false inconsistencies or undesirable trades. <br>
Mitigation: Review the strategy behavior in paper mode, tune position, spread, volume, and threshold parameters, and monitor orders before enabling live execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-resolution-lattice-trader) <br>
- [Simmer SDK on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [Simmer SDK on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON configuration metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce paper-trading or live-trading actions depending on runtime flags and credentials; defaults to paper mode.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
