## Description: <br>
Analyzes cross-domain Huawei Cloud CCE incidents across alarms, workload rollout, pod events and logs, recent changes, topology, nodes, network, and metrics to produce root-cause reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to investigate Huawei Cloud CCE incidents, correlate multi-domain evidence, rank likely root causes, and prepare remediation handoff without directly applying changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled dispatcher exposes high-impact Huawei Cloud and Kubernetes administration actions beyond root-cause reporting. <br>
Mitigation: Install only when broad operational authority is intended; use least-privilege read-only IAM and RBAC credentials where possible, avoid mutation actions, and review any confirm=true operation before execution. <br>
Risk: Root-cause conclusions can be misleading if based on a single alarm or incomplete timeline. <br>
Mitigation: Require a timeline or evidence chain, include counter-evidence and data gaps for each candidate cause, and label low-confidence conclusions clearly. <br>
Risk: Cloud credentials and temporary Kubernetes certificates may be exposed if handled carelessly during diagnosis. <br>
Mitigation: Do not persist or print AK, SK, security tokens, or certificate values; delete temporary certificate files immediately after use. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Output Schema](references/output-schema.md) <br>
- [Risk Rules](references/risk-rules.md) <br>
- [Huawei Cloud CCE Documentation](https://support.huaweicloud.com/cce/index.html) <br>
- [Huawei Cloud Python SDK Documentation](https://support.huaweicloud.com/api-cce/cce_02_0113.html) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown root-cause report with structured JSON action results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes investigation steps, timeline, evidence chain, impact scope, Top3 causes, confidence, counter-evidence, and remediation handoff.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
