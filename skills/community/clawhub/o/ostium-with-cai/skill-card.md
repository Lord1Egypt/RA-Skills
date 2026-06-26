## Description: <br>
Trade Ostium RWA perps on Arbitrum via CAI using defi_markets, defi_preflight, defi_trade, defi_order_status, and hosted enrollment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bernardtai](https://clawhub.ai/user/bernardtai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide agents through CAI-managed Ostium RWA perpetual trading on Arbitrum, including enrollment, market lookup, preflight validation, trade placement, order status checks, and position close flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides live real-money perpetual trading and the security evidence says it does not clearly warn users or require confirmation before risky trade actions. <br>
Mitigation: Require explicit confirmation of each trade's asset, size, leverage, network, wallet authority, fees, liquidation exposure, and loss risk before allowing trade placement. <br>
Risk: Automated trade placement can use broad CAI API authority and affect a custodial wallet. <br>
Mitigation: Store CAI_API_KEY only in the agent secret store, prefer the narrowest usable scope, rotate keys when no longer needed, and do not allow unattended trading. <br>
Risk: Incorrect order flow can place or close the wrong Ostium position. <br>
Mitigation: Use defi_preflight before placement, resolve pair_id from defi_markets instead of hardcoding it, use action=close for closes, and poll defi_order_status until is_terminal is true. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bernardtai/skills/ostium-with-cai) <br>
- [CAI canonical skill reference](https://cai.com/skill.md) <br>
- [CAI tools manifest](https://cai.com/specs/cai-tools.manifest.json) <br>
- [CAI developers](https://cai.com/developers.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API call parameters] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-like API parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a CAI_API_KEY with platform or full scope; live trade actions should require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.17 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
