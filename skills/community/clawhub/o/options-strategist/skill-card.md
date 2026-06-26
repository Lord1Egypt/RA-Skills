## Description: <br>
Analyze options chains, compute implied volatility rank, and select optimal multi-leg strategies based on market conditions via the Finskills API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finskills](https://clawhub.ai/user/finskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze live options chains, compare implied and historical volatility, and generate options strategy reports with Greeks, profit/loss metrics, and risk-management guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Finskills API key for market-data lookups. <br>
Mitigation: Store FINSKILLS_API_KEY as an environment variable or managed secret, and do not paste it into prompts or commit it to source control. <br>
Risk: Options calculations or strategy recommendations may be incorrect, stale, or unsuitable for a user's financial situation. <br>
Mitigation: Verify prices, Greeks, volatility metrics, and risk calculations before making any trading decision, and consult a licensed financial advisor where appropriate. <br>
Risk: The skill depends on external Finskills market data and plan availability. <br>
Mitigation: Use the skill only if the user is comfortable with Finskills lookups, and confirm that the configured plan provides the required options-chain data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/finskills/options-strategist) <br>
- [Skill homepage](https://github.com/finskills/options-strategist) <br>
- [Finskills API](https://finskills.net) <br>
- [Finskills registration](https://finskills.net/register) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown strategy report with options-chain analysis, calculations, and risk notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY for Finskills market-data lookups.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
