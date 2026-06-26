## Description: <br>
Identifies and trades structural pricing inconsistencies between Dota 2 best-of-three winner, game winner, and handicap markets on Polymarket. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to monitor Dota 2 BO3 market bundles, detect mathematical inconsistencies, and optionally execute Polymarket trades. It starts in paper mode and requires an explicit live flag before real USDC trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SIMMER_API_KEY is a sensitive credential with trading authority. <br>
Mitigation: Store it as a secret, scope it narrowly where possible, and rotate it if exposure is suspected. <br>
Risk: Live mode can place real USDC trades on Polymarket. <br>
Mitigation: Start in paper mode, keep position and spread limits conservative, and use --live only after deliberate review. <br>
Risk: The skill depends on the third-party simmer-sdk package. <br>
Mitigation: Review and scan the dependency before deployment, and pin or control the installed version in production environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diagnostikon/polymarket-bundle-dota2-bo3-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, configuration, shell commands, guidance] <br>
**Output Format:** [Console text and trading API actions controlled by environment configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; defaults to paper trading unless run with --live.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
