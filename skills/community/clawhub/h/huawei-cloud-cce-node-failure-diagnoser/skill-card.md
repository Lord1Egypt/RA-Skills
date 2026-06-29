## Description: <br>
Diagnoses Huawei Cloud CCE/Kubernetes node failures by collecting node status, lease, event, pod, metric, and security evidence and producing a Markdown diagnosis report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and cloud operations teams use this skill to investigate Huawei Cloud CCE node NotReady states, resource pressure, liveness issues, workload impact, and related security findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the release includes broad live cluster administration and credential-revealing capabilities under a read-only node-diagnosis description. <br>
Mitigation: Install only for operators who need broad Huawei Cloud and Kubernetes operational access, and prefer least-privilege read-only credentials. <br>
Risk: The skill requires sensitive Huawei Cloud credentials. <br>
Mitigation: Use HUAWEI_AK and HUAWEI_SK environment variables, avoid passing credentials as command parameters, and do not expose or log credential values. <br>
Risk: Some actions may involve confirmation-gated cluster changes or sensitive raw data access outside the normal diagnosis path. <br>
Mitigation: Do not invoke raw kubeconfig, secret, or log actions unless explicitly needed, and review any action involving confirm=true or cluster changes before execution. <br>


## Reference(s): <br>
- [Diagnosis Workflow](references/workflow.md) <br>
- [Output Schema](references/output-schema.md) <br>
- [Risk Rules](references/risk-rules.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [IAM Policies](references/iam-policies.md) <br>
- [Common Pitfalls](references/common-pitfalls.md) <br>
- [Huawei Cloud Python SDK Documentation](https://doc.huihua.com/api/sdk/python.html) <br>
- [Huawei Cloud API Explorer](https://support.huaweicloud.com/apiexplorer/index.html) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, guidance] <br>
**Output Format:** [Markdown diagnosis report with structured evidence and optional JSON fields from dispatcher actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Primary diagnosis output includes report_markdown plus evidence, node, lease, liveness, root_category, confidence, pod_summary, health_items, events, and metrics fields.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
