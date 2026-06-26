## Description: <br>
Trade Polymarket markets based on valuation divergence. When your probability model differs from Polymarket's price by >threshold, enter using Kelly sizing. Works with any probability model (Simmer AI consensus, user model, external API). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adlai88](https://clawhub.ai/user/adlai88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading operators use this skill to scan Polymarket markets, compare market prices against a probability model, and prepare or execute Kelly-sized trades when the configured edge threshold is met. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real Polymarket trades when run with live mode. <br>
Mitigation: Start with dry runs, confirm the account and market behavior, and use live mode only after reviewing the configured position and trade limits. <br>
Risk: Unattended live execution can continue trading without immediate human review. <br>
Mitigation: Avoid unattended `--live --quiet` use unless monitoring and loss controls are in place. <br>
Risk: Poor model calibration, market movement, or liquidity can turn an apparent edge into losses. <br>
Mitigation: Review `max_position_usd`, `max_trades_per_run`, edge thresholds, and safeguards before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adlai88/polymarket-valuation-divergence) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code, guidance] <br>
**Output Format:** [Console text and Markdown documentation with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run mode reports candidate trades; live mode can submit trades through the configured Simmer/Polymarket account.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
