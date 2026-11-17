## Description:

Huawei Cloud UCS cluster onboarding, lifecycle, and fleet management via hcloud CLI, including cluster registration, querying, removal, fleet groups, kubeconfig retrieval, and quota checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud platform engineers use this skill to administer Huawei Cloud UCS clusters with hcloud CLI guidance, including onboarding CCE or self-managed clusters, managing fleet groups, obtaining kubeconfigs, checking quotas, and handling common UCS failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide sensitive Huawei Cloud UCS administration, including cluster registration, deregistration, fleet changes, quota checks, and kubeconfig retrieval.

Mitigation: Use a least-privilege IAM user, prefer temporary credentials, confirm every paid or destructive command before execution, and install the skill only for UCS administration use cases.

Risk: Kubeconfig files, access tokens, AK/SK values, and security tokens are sensitive and may grant cluster or cloud access.

Mitigation: Treat generated kubeconfig files and credential values as secrets, avoid printing them in conversation or logs, and rotate credentials according to the organization's policy.

## Reference(s):

- [UCS Cluster Onboarding API Reference Guide](references/ucs-cluster-onboarding-api-guide.md)
- [Task: Cluster Registration & Deregistration](references/taREDACTED-SECRET.md)
- [Task: Fleet Management](references/task-fleet-management.md)
- [Task: Access Management](references/task-access-management.md)
- [IAM Permission Policies - UCS Cluster Onboarding Manager Skill](references/iam-policies.md)
- [Parameter Reference](references/parameter-reference.md)
- [Common Pitfalls & Solutions](references/common-pitfalls.md)
- [Verification Method - UCS Cluster Onboarding Manager Skill](references/verification-method.md)
- [UCS Cluster Onboarding Manager - Output Format](references/output-format.md)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [KooCLI Command Format Standard](references/kocli-command-format.md)
- [Acceptance Criteria](references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Huawei Cloud CLI commands and kubeconfig handling guidance; generated kubeconfig material and credential values should be treated as sensitive.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
