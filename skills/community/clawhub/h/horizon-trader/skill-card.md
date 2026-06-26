## Description: <br>
Horizon SDK helps agents inspect and trade prediction markets, manage orders and risk controls, discover markets, and run portfolio, arbitrage, and quantitative analytics through a CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jesusmanuelrg](https://clawhub.ai/user/Jesusmanuelrg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading-focused agents use this skill to query prediction-market positions, orders, fills, market data, and wallet analytics, and to prepare or execute trading, arbitrage, risk-management, and quantitative-analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit or cancel real prediction-market orders and change trading controls. <br>
Mitigation: Use paper mode or read-only credentials where possible, and require explicit human confirmation before order, cancellation, arbitrage, kill-switch, stop-loss, take-profit, or runtime-parameter changes. <br>
Risk: The skill depends on an external horizon-sdk package and uses HORIZON_API_KEY for authenticated actions. <br>
Mitigation: Review or pin horizon-sdk before granting trading authority, and keep HORIZON_API_KEY least-privileged. <br>


## Reference(s): <br>
- [Horizon SDK ClawHub documentation](https://docs.openclaw.ai/tools/clawhub) <br>
- [Horizon SDK ClawHub release page](https://clawhub.ai/Jesusmanuelrg/horizon-trader) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON command output with Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HORIZON_API_KEY for authenticated account actions; market and analytics commands accept CLI arguments and JSON configuration values.] <br>

## Skill Version(s): <br>
0.5.5 (source: server release metadata; artifact frontmatter reports 0.4.16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
