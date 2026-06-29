## Description: <br>
Detects logically linked Polymarket markets whose mutually exclusive YES prices do not sum to about 1 and, in sim by default, can trade the cheap or rich legs back toward coherence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bridgeaisocial](https://clawhub.ai/user/bridgeaisocial) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and prediction-market operators use this skill to monitor Polymarket market sets for price-coherence gaps, test the logic in simulation, and optionally run guarded live trades after reviewing financial-risk settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real Polymarket trades when explicitly launched with live options. <br>
Mitigation: Run in dry-run first, require explicit live launch settings, and use conservative MAX_TRADE_USD and DAILY_BUDGET_USD limits before enabling live trading. <br>
Risk: COHERENCE_GROUPS are trusted as user-supplied mutually exclusive market groups. <br>
Mitigation: Only configure market groups whose exclusivity has been independently reviewed, and keep unconfirmed or partial groups in alert-only workflows. <br>
Risk: The skill reads a Simmer API key and writes local position and exposure state. <br>
Mitigation: Protect SIMMER_API_KEY as a sensitive credential and review local state files before changing venues or switching from dry-run to live operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bridgeaisocial/polymarket-coherence-arb) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Console text, environment-variable configuration, Polymarket or simulation trade calls, and local JSON state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to dry-run simulation and separates dry-run state from live state.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
