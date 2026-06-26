## Description: <br>
Classifies agent tasks into 4 risk tiers (GREEN/YELLOW/RED/CRITICAL). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to label implementation tasks by risk, decide which verification gates apply, and route higher-risk work to stronger review before completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic trigger words such as risk, safety, and verification may activate the skill more often than needed. <br>
Mitigation: Use the skill when classifying code or configuration changes, and treat unrelated or purely exploratory work as out of scope. <br>
Risk: High-risk task labels may be wrong if heuristic file patterns miss context or overstate impact. <br>
Mitigation: Use the documented RED and CRITICAL gates, including reversibility scoring, full tests, review, and human approval for critical work. <br>
Risk: The full upstream workflow references companion skills and configuration that may not be installed. <br>
Mitigation: Confirm the required companion skills and the night-market.error-patterns configuration are available before relying on the complete workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-leyline-risk-classification) <br>
- [OpenClaw metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with task metadata examples and tiered verification checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces risk tiers, risk reasons, readiness levels, verification gates, and parallel execution guidance; it does not execute commands or access external services.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
