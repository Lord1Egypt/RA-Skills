## Description: <br>
Diagnoses Huawei Cloud CCE autoscaling failures across HPA, CCE elastic engine or Cluster Autoscaler, metrics, resource requests, Pending Pods, scheduling constraints, node pool limits, subnet IP, quota, and IAM permission signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site reliability engineers use this skill to diagnose Huawei Cloud CCE autoscaling failures, gather HPA, Cluster Autoscaler, node pool, Pod, event, and metric evidence, and produce a Markdown report with conclusions, confidence, data gaps, and recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled dispatcher exposes broader cloud administration, credential-return, secret-reading, and state-changing actions beyond the advertised read-only autoscaling diagnosis behavior. <br>
Mitigation: Review the dispatcher surface before installation, allow only the intended diagnosis actions, and run with least-privilege, preferably read-only Huawei Cloud/IAM credentials. <br>
Risk: The skill requires sensitive Huawei Cloud credentials, and broad production AK/SK credentials would increase impact if misused. <br>
Mitigation: Use scoped IAM users or temporary credentials, avoid broad production AK/SK values, and do not expose credentials in commands, logs, files, or responses. <br>
Risk: Recommendations or generated configuration previews could be applied incorrectly and affect workload scaling, node pool capacity, cost, or availability. <br>
Mitigation: Treat remediation as a separate reviewed change: require explicit customer approval, validate business impact and rollback plans, and prefer preview or manual change workflows. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Output Schema](references/output-schema.md) <br>
- [Capability Map](references/capability-map.md) <br>
- [Risk Rules](references/risk-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown diagnosis report with structured evidence and optional JSON response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include HPA, Cluster Autoscaler, node pool, Pod, event, metric, issue, confidence, recommendation, and data-gap details.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
