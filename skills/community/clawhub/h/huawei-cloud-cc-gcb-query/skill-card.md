## Description:

Helps agents inspect Huawei Cloud Cloud Connect Global Connection Bandwidth resources with read-only hcloud CLI queries for GCB details, filtered lists, tenant configuration, and binding eligibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to prepare read-only hcloud CLI commands and parameter guidance for inspecting Huawei Cloud CC GCB resources, quotas, filters, and binding candidates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using an identity with broader permissions than needed could expose more Huawei Cloud resource data than intended.

Mitigation: Use a read-only Huawei Cloud identity where possible, such as CC ReadOnlyAccess or an equivalent least-privilege policy.

Risk: Running an unverified CLI installer could introduce supply-chain risk.

Mitigation: Verify the hcloud installer source before running it and use the official Huawei Cloud KooCLI installation guidance.

Risk: Applying this skill outside Huawei Cloud CC GCB query tasks could produce irrelevant or misleading guidance.

Mitigation: Use the skill only for Global Connection Bandwidth inspection workflows and route unrelated bandwidth or write-operation tasks elsewhere.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cc-gcb-query)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [IAM Policies](references/iam-policies.md)
- [Verification Method](references/verification-method.md)
- [Data Flow Diagram](references/dataflow-diagram.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [API Reference](references/api-reference.md)
- [Huawei Cloud hcloud CLI Quick Start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Huawei Cloud hcloud Installer](https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/hcloud_install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with hcloud CLI command examples and parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only query guidance for Huawei Cloud CC GCB resources; commands require authenticated hcloud CLI access and a domain ID.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
