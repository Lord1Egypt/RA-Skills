## Description: <br>
Trades a Simmer-indexed market when your estimated probability diverges from the live market price, with dry-run on sim by default, context checks, reasoning tags, and optional live execution on Polymarket through ClawHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssj124](https://clawhub.ai/user/ssj124) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading agents use this skill to wrap an existing probability estimate for a Simmer-indexed market with market context checks, threshold-based trade discipline, and dry-run-first execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place live prediction-market trades when live execution is enabled, and security guidance calls out checking venue coverage before installation. <br>
Mitigation: Confirm the manifest and runtime options list all permitted live venues, review credentials and order controls, and keep dry-run mode until the operator intentionally enables live trading. <br>
Risk: Market context warnings, flip-flop risk, or high slippage can make an otherwise profitable-looking divergence unsafe to trade. <br>
Mitigation: Fetch market context before deciding, hold when alerts are present, and review the operator summary before relying on any trade decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ssj124/polymarket-divergence-trader) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Plain text operator summary with optional JSON trade result output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and market inputs; defaults to dry-run unless live execution is explicitly enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
