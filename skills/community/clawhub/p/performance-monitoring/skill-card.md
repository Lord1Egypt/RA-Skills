## Description: <br>
Monitors agent scheduling, execution, memory, retrieval, and token-efficiency metrics, records logs, detects bottlenecks, raises alerts, and suggests performance optimizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daxiangnaoyang](https://clawhub.ai/user/daxiangnaoyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor agent performance trends, identify scheduling and memory bottlenecks, configure alerts, and guide optimization work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Performance metrics and alerts may expose sensitive operational details if sent to an overly broad Feishu destination. <br>
Mitigation: Confirm the Feishu destination and access controls before use, and record only aggregate metrics that exclude prompts, secrets, user content, customer data, and sensitive task details. <br>
Risk: The configured hourly collection interval and 30-day retention period may conflict with an organization's monitoring or data-retention requirements. <br>
Mitigation: Review and adjust the collection interval and retention setting for the deployment environment before enabling the skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/daxiangnaoyang/performance-monitoring) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and PowerShell code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces performance metric logs, threshold configuration, Feishu alert guidance, trend analysis, and optimization recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
