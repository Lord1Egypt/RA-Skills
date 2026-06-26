## Description: <br>
Diagnoses metric fluctuations by identifying contributing factors, dimensions, and external events, then produces a consolidated attribution report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackyujun](https://clawhub.ai/user/jackyujun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business analysts, data teams, and agents use this skill to investigate why a metric changed by querying CAN Gateway metrics, decomposing contributing factors, drilling into dimensions, correlating external events, and writing an attribution diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires CAN_API_KEY access and outbound network calls to query business metrics. <br>
Mitigation: Use a least-privilege API key limited to the metrics and dimensions needed for the intended analysis. <br>
Risk: Broad trigger phrases may cause the skill to run on ambiguous metric-change questions. <br>
Mitigation: Confirm the metric, comparison baseline, and analysis scope before issuing CAN Gateway requests. <br>
Risk: Attribution results can be mistaken for causal proof when they are based on metric decomposition and event correlation. <br>
Mitigation: Label conclusions by confidence and distinguish observed contribution patterns from causal claims. <br>


## Reference(s): <br>
- [Aloudata](https://aloudata.com/) <br>
- [ClawHub skill listing](https://clawhub.ai/jackyujun/metric-attribution) <br>
- [CAN Gateway metrics query API](https://gateway.can.aloudata.com/api/metrics/query) <br>
- [CAN Gateway metrics search API](https://gateway.can.aloudata.com/api/metrics/search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Files, Guidance] <br>
**Output Format:** [Markdown diagnostic report with inline API calls, JSON request bodies, Python snippets, and optional chart image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a waterfall chart image when factor decomposition applies.] <br>

## Skill Version(s): <br>
1.0.4 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
