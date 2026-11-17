## Description:

Diagnoses Huawei Cloud CCE Pod failures by gathering Pod status, Kubernetes Events, logs, and optional metrics to identify likely causes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to diagnose Huawei Cloud CCE Pods in CrashLoopBackOff, ImagePullBackOff, OOMKilled, Pending, Evicted, or frequent restart states. It builds an evidence chain from Pod status, Events, logs, and metrics, then returns likely causes and read-only next checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is advertised as read-only Pod diagnosis, but the included dispatcher can expose broader Huawei Cloud administration and mutation actions.

Mitigation: Review and restrict the action surface before installation; remove or disable undocumented mutation, EIP, remediation, and broad infrastructure actions when the release is intended only for Pod diagnosis.

Risk: Huawei Cloud credentials can grant access beyond the diagnostic use case if broad or production-admin identities are used.

Mitigation: Use a least-privilege Huawei IAM identity limited to the documented read-only diagnostic permissions and avoid production admin credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pintudeyudi/skills/huawei-cloud-cce-pod-failure-diagnoser)
- [Workflow](references/workflow.md)
- [Risk Rules](references/risk-rules.md)
- [Output Schema](references/output-schema.md)
- [Verification Method](references/verification-method.md)
- [Common Pitfalls](references/common-pitfalls.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON diagnostic summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sanitized log excerpts, Kubernetes Events, metrics, ranked causes, and read-only recommended checks.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
