## Description:

Configure, deploy, and verify Huawei Cloud CCE to CCI 2.0 bursting with VPCEP dependencies, virtual-kubelet, a smoke workload, and readiness checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to prepare Huawei Cloud CCE clusters for CCI 2.0 bursting, validate networking and addon readiness, and run a controlled smoke workload after approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shipped command wrapper exposes broader Huawei Cloud and Kubernetes capabilities than the bursting workflow needs.

Mitigation: Use only the skill-profile actions for this release and review any off-profile dispatcher action separately before invocation.

Risk: Broad AK/SK or root-level cloud credentials could expand the impact of mistakes or misuse.

Mitigation: Use tightly scoped IAM credentials, prefer IAM users over root accounts, and avoid persisting AK/SK values in files, reports, shell history, or Kubernetes Secrets.

Risk: Some mutating operations can create or alter cloud and cluster resources.

Mitigation: Run preview steps first and require explicit user approval with confirm=true before VPCEP creation, addon setup, node-pool changes, or smoke workload deployment.

Risk: Kubeconfig or Kubernetes Secret data exposure could disclose sensitive cluster access material.

Mitigation: Remove or gate kubeconfig and Secret-data export paths before deployment, and review generated outputs for sensitive values.

## Reference(s):

- [Workflow](artifact/references/workflow.md)
- [Risk Rules](artifact/references/risk-rules.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [CCI 2.0 environment configuration](https://support.huaweicloud.com/intl/zh-cn/usermanual-cci2/cci_01_0024.html)
- [CCI 2.0 cloud bursting setup](https://support.huaweicloud.com/intl/zh-cn/usermanual-cci2/cci_01_0025.html)
- [CCE cloud native hybrid deployment addon](https://support.huaweicloud.com/usermanual-cce/cce_10_0135.html)
- [CCI image pulling FAQ](https://support.huaweicloud.com/intl/en-us/cci_faq/cci_faq_0095.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview-first workflow; mutating cloud or cluster actions require explicit confirmation.]

## Skill Version(s):

0.1.1 (source: server release evidence, released 2026-06-16T09:46:22Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
