## Description: <br>
Diagnoses Huawei Cloud CCE and Kubernetes storage failures such as PVC Pending, mount failures, EVS disk issues, CSI driver errors, and capacity or binding problems using a Python SDK dispatcher. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to diagnose Huawei Cloud CCE storage incidents, collect Kubernetes and cloud-side storage evidence, and produce a Markdown report with findings, confidence, and remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dispatcher exposes broad Huawei Cloud and Kubernetes administration actions beyond the advertised storage-diagnosis workflow. <br>
Mitigation: Deploy only with tightly scoped read-only credentials and restrict execution to the documented storage-diagnosis actions. <br>
Risk: Credentials with delete or write permissions could allow destructive or credential-sensitive operations through the shipped dispatcher. <br>
Mitigation: Avoid granting delete or write permissions, rotate credentials after testing, and review requested actions before execution. <br>
Risk: Unlisted dispatcher actions may remain available attack surface until the package is split or allowlisted. <br>
Mitigation: Treat undocumented actions as unavailable in production and enforce an external allowlist for approved read-only diagnostic commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pintudeyudi/huawei-cloud-cce-storage-failure-diagnoser) <br>
- [Workflow reference](references/workflow.md) <br>
- [Output schema](references/output-schema.md) <br>
- [Risk rules](references/risk-rules.md) <br>
- [Huawei Cloud Python SDK Documentation](https://doc.huihua.com/api/sdk/python.html) <br>
- [Huawei Cloud API Explorer](https://support.huaweicloud.com/apiexplorer/index.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Structured JSON with an embedded Markdown diagnosis report, evidence summary, findings, confidence, and remediation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Huawei Cloud and Kubernetes evidence collected through the dispatcher; credentials and permissions should be scoped read-only.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
