## Description: <br>
Diagnoses Huawei Cloud CCE Pod failures such as CrashLoopBackOff, ImagePullBackOff, OOMKilled, Pending, Evicted, restart storms, log issues, events, and Pod resource usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operators, SREs, and developers use this skill to diagnose failing Huawei Cloud CCE Pods by collecting Pod status, Kubernetes Events, current and previous logs, optional metrics, and ranked likely causes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged dispatcher exposes privileged Huawei Cloud and Kubernetes actions beyond pod diagnosis, including actions that may reveal secrets or change infrastructure. <br>
Mitigation: Review and constrain the dispatcher actions before installation; disable or remove kubeconfig, secret, export, mutation, and subagent actions when only pod diagnosis is needed. <br>
Risk: Cloud credentials and operational data such as logs, audit records, raw reports, and kubeconfig output may be sensitive. <br>
Mitigation: Use least-privilege Huawei IAM credentials, avoid passing AK/SK values as command-line parameters, and treat diagnostic outputs as sensitive operational data. <br>
Risk: Remediation suggestions for scaling, deletion, drain, reboot, or rebuild operations could affect production workloads if executed directly. <br>
Mitigation: Keep this skill limited to read-only diagnosis and hand off mutation proposals for explicit review before execution. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Risk Rules](references/risk-rules.md) <br>
- [Output Schema](references/output-schema.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Common Pitfalls](references/common-pitfalls.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and structured JSON diagnosis reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Diagnosis reports include status summaries, affected Pods, issues, evidence, top causes, recommended actions, warnings, and optional next-skill handoff.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
