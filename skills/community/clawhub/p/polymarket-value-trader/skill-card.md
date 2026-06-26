## Description: <br>
Trade prediction markets on Simmer/Polymarket using value-based analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[czm200](https://clawhub.ai/user/czm200) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to analyze Simmer and Polymarket prediction markets, check positions, identify value opportunities, and prepare trades with explicit reasoning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to place or cancel prediction-market trades, including real-money Polymarket trades. <br>
Mitigation: Keep TRADING_VENUE set to sim unless real USDC trading is deliberately enabled, and require explicit approval before each trade, venue change, or order cancellation. <br>
Risk: A SIMMER_API_KEY may authorize trading actions if exposed or misused. <br>
Mitigation: Use a restricted and revocable API key when available, keep it in workspace secrets, and set hard spending limits outside the skill. <br>
Risk: Market recommendations can be wrong, stale, or based on ambiguous resolution criteria. <br>
Mitigation: Review market context, warnings, resolution criteria, and the proposed thesis before execution; pass on markets where the thesis or resolution is unclear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/czm200/polymarket-value-trader) <br>
- [Simmer Markets](https://simmer.markets) <br>
- [Simmer API base URL](https://api.simmer.markets) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to the sim venue unless real trading is deliberately enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
