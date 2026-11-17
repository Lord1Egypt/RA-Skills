## Description:

Converts Huawei Cloud CCE remediation requests into preview-first, confirm-required execution plans with post-action verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operations and SRE teams use this skill to prepare and run confirmed Huawei Cloud CCE remediation actions, including workload rollback or scaling, node operations, cluster hibernate or awake, traffic changes, and HSS vulnerability status updates. It is intended for cases where a diagnosis or explicit operator request already identifies a remediation target.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad cloud-management and secret-access actions may exceed the stated CCE remediation purpose.

Mitigation: Review before installation, use a skill-specific action allowlist, and do not grant Kubernetes Secret access or undeclared provisioning permissions unless explicitly required.

Risk: Remediation actions can mutate or delete workloads, nodes, clusters, network bindings, ECS instances, and vulnerability state.

Mitigation: Use narrowly scoped, temporary Huawei Cloud credentials and require preview, explicit per-target confirmation, and read-only post-execution verification for every mutation.

Risk: TLS verification and temporary credential or certificate-file handling may need hardening before privileged deployment.

Mitigation: Fix TLS verification behavior and temporary file cleanup before privileged use, and prevent credential values from appearing in logs or responses.

## Reference(s):

- [Workflow](references/workflow.md)
- [Risk Rules](references/risk-rules.md)
- [Output Schema](references/output-schema.md)
- [Huawei Cloud CCE Documentation](https://support.huaweicloud.com/cce/index.html)
- [Huawei Cloud Python SDK Documentation](https://support.huaweicloud.com/api-cce/cce_02_0113.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON remediation previews and execution records, with optional Markdown execution reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview records include confirmation state, trace ID, risk level, target, impact scope, rollback notes, and post-execution verification.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
