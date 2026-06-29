## Description: <br>
Analyzes recent Huawei Cloud CCE workload, configuration, node, network, and security-policy changes to produce evidence-based incident attribution reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to investigate whether recent CCE changes contributed to an incident and to generate a timeline, evidence matrix, blast-radius assessment, risk score, conclusions, and data gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled dispatcher exposes cloud and Kubernetes administration actions beyond the advertised read-only change analysis workflow. <br>
Mitigation: Review and constrain allowed actions before installation, and expose only the read-only analysis actions needed for the workflow. <br>
Risk: The skill requires sensitive Huawei Cloud credentials and can inspect CCE resources, including security-relevant configuration. <br>
Mitigation: Use least-privilege read-only credentials, avoid cluster-admin or write IAM permissions, and prevent credentials or tokens from being logged or persisted. <br>
Risk: Kubeconfig export, Secret data access, output file paths, and any confirm=true invocation can increase operational or data exposure. <br>
Mitigation: Require explicit human approval for those operations and review requested output paths before execution. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Capability Map](references/capability-map.md) <br>
- [Output Schema](references/output-schema.md) <br>
- [Risk Rules](references/risk-rules.md) <br>
- [Huawei Cloud CCE Documentation](https://support.huaweicloud.com/cce/index.html) <br>
- [Huawei Cloud Python SDK Documentation](https://support.huaweicloud.com/api-cce/cce_02_0113.html) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Markdown, Files, Guidance] <br>
**Output Format:** [Structured JSON with embedded Markdown report and optional Markdown report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes an analysis trace ID, analysis window, scoped CCE resources, top changes, risk scoring, evidence, data-source status, and capture metadata.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
