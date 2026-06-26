## Description: <br>
Analyzes Java business code to identify monitorable metrics and provide metric definitions, label suggestions, and collection guidance, with optional AOP reference scanning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azrcn](https://clawhub.ai/user/azrcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Java service, controller, manager, and facade code for metric candidates, naming templates, labels, and collection approaches. It can optionally compare existing Aspect, Interceptor, or Filter classes to avoid duplicate metric collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional AOP, Interceptor, and Filter scanning may expose additional project source files to the agent. <br>
Mitigation: Enable optional AOP scanning only for repositories and files the user is comfortable having the agent inspect. <br>
Risk: The release metadata contains unrelated crypto and purchase capability tags that do not match the reviewed markdown behavior. <br>
Mitigation: Treat those tags as metadata cautions for this version and require publisher correction or renewed review before relying on them. <br>
Risk: Metric recommendations are inferred from code patterns and may not match the team's business definitions. <br>
Mitigation: Have developers review and adjust generated metric names, labels, and collection methods before implementation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/azrcn/metric-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analysis report with tables and Java examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides metric name templates, suggested labels, metric types, and collection recommendations for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
