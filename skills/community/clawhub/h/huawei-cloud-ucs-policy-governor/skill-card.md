## Description:

Huawei Cloud UCS (Ubiquitous Cloud Native Service) policy governance and compliance management skill using hcloud CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and cloud administrators use this skill to manage Huawei Cloud UCS policy instances, policy definitions, policy enforcement, and fleet compliance audits through hcloud CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live Huawei Cloud UCS mutations, including create, update, delete, enable, and disable operations.

Mitigation: Use it only for UCS administration, require explicit human confirmation before write actions, and prefer read-only checks when the goal is compliance review.

Risk: Credential and kubeconfig handling can expose sensitive cloud or cluster access if stored or echoed carelessly.

Mitigation: Use least-privilege IAM, prefer temporary credentials, avoid printing secrets, and avoid storing kubeconfig or AK/SK files unless operationally necessary.

Risk: Audit workflows include remediation steps that may apply changes to live clusters.

Mitigation: Review proposed kubectl apply or policy mutation commands before execution and validate target cluster or fleet identifiers first.

## Reference(s):

- [Huawei Cloud UCS Policy Governor](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-ucs-policy-governor)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [IAM Permission Policies](references/iam-policies.md)
- [Task: Policy Management](references/task-policy-management.md)
- [Task: Compliance Audit](references/task-compliance-audit.md)
- [UCS Policy API Reference Guide](references/ucs-policy-api-guide.md)
- [Verification Method](references/verification-method.md)
- [Common Pitfalls & Solutions](references/common-pitfalls.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [hcloud CLI installer](https://obs.cn-north-4.myhuaweicloud.com/hcloud/client/hcloud_install.sh)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with hcloud CLI command blocks and JSON policy examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create, update, delete, enable, or disable Huawei Cloud UCS policy resources and may require explicit confirmation before execution.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
