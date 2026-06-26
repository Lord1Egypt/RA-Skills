## Description: <br>
Prediction quality scoring for AI agents. Brier score, log score, and multi-source convergence analysis. Know if your forecasts are accurate and if your data sources agree. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whatsonyourmind](https://clawhub.ai/user/whatsonyourmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to score prediction accuracy, compare forecast quality, evaluate prediction market positions, and detect disagreement or outliers across multiple sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OraClaw API key and sends forecast data to an external service. <br>
Mitigation: Install only if the OraClaw service is acceptable for the intended data, and avoid sending sensitive proprietary forecasts unless approved. <br>
Risk: Each scoring call has disclosed usage pricing. <br>
Mitigation: Confirm expected call volume and billing tolerance before enabling routine use. <br>


## Reference(s): <br>
- [OraClaw Calibrate homepage](https://oraclaw.dev/calibrate) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Text or JSON scoring results with calibration metrics and convergence analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ORACLAW_API_KEY; disclosed pricing is $0.02 per scoring call with a free tier of 3,000 calls/month.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
