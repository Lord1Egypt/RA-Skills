## Description: <br>
Oraclaw Simulate runs Monte Carlo simulations for AI agents to model risk, forecast revenue, estimate project timelines, and quantify uncertainty across six distribution types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whatsonyourmind](https://clawhub.ai/user/whatsonyourmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to run Monte Carlo simulations for revenue targets, project timelines, portfolio Value at Risk, sensitivity analysis, and probabilistic forecasts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an ORACLAW_API_KEY for a paid simulation service. <br>
Mitigation: Use a dedicated API key where possible and monitor charges. <br>
Risk: Simulation requests may include confidential financial, trading, or business formulas. <br>
Mitigation: Avoid submitting confidential inputs unless the user is comfortable with OraClaw processing them. <br>
Risk: Monte Carlo results are probabilistic estimates and may be misread as guaranteed outcomes. <br>
Mitigation: Present results as uncertainty estimates with assumptions, percentiles, and scenario context. <br>


## Reference(s): <br>
- [OraClaw Simulate homepage](https://oraclaw.dev/simulate) <br>
- [ClawHub skill page](https://clawhub.ai/whatsonyourmind/oraclaw-simulate) <br>
- [Publisher profile](https://clawhub.ai/user/whatsonyourmind) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Markdown or JSON simulation summaries with mean, standard deviation, percentile results, and histogram data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ORACLAW_API_KEY and uses a paid OraClaw simulation service.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
