## Description: <br>
MetricHub 指标平台 helps agents guide MetricHub users through metric catalog browsing, query construction, visualization recommendations, dashboard orchestration, and workspace Gateway configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
MetricHub users and workspace operators use this skill to navigate a multi-tenant metrics platform, construct valid metric queries, choose visualizations, compose dashboards, and configure Gateway access for trusted workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide actions that use tenant credentials, execute metric queries, or create persistent dashboards in MetricHub workspaces. <br>
Mitigation: Use it only in trusted workspaces, keep API keys scoped per workspace, and confirm before changing Gateway settings or creating persistent dashboards. <br>
Risk: Incorrect query construction can produce misleading metric results, especially for time windows, proportions, rankings, or ambiguous business terms. <br>
Mitigation: Review generated query JSON against the skill's query rules and require clarification when metric context, dimensions, or time constraints are insufficient. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/metric-platform) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with JSON and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MetricHub routes, Gateway query JSON, chart recommendations, dashboard instructions, and workspace configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
