## Description: <br>
Computes portfolio risk and exposure metrics before sizing and rebalance decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ndtchan](https://clawhub.ai/user/ndtchan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and portfolio reviewers use this skill to compute risk, concentration, correlation, benchmark sensitivity, and data-confidence context from local holdings and price-history CSV files before sizing or rebalance review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio holdings and price files can contain sensitive financial information. <br>
Mitigation: Install only when comfortable sharing portfolio details with the agent environment and use local files intentionally. <br>
Risk: Risk analytics can be mistaken for trading or rebalance instructions. <br>
Mitigation: Treat output as risk-management context, verify holdings and prices independently, and do not use the skill to execute trades. <br>
Risk: Missing benchmark data, short price history, or incomplete coverage can make beta, concentration, and confidence claims unreliable. <br>
Mitigation: Downgrade confidence for incomplete inputs and avoid precise beta or relative-risk claims without aligned benchmark data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ndtchan/portfolio-analytics) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown analysis with structured portfolio metrics and optional JSON summary output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local CSV inputs and reports confidence, data gaps, and handoff fields for downstream review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
