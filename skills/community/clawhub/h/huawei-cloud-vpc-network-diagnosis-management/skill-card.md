## Description:

Helps agents inspect, diagnose, create, update, and delete Huawei Cloud VPCs and subnets, including network and port connectivity and CIDR conflict analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers use this skill to inspect Huawei Cloud VPC resources, investigate connectivity and address conflicts, and manage VPCs and subnets with confirmation before changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default quality reporting can send cloud command results, credential-derived authentication data, and local agent session metadata to Huawei endpoints.

Mitigation: Review the reporting behavior before installing and set SKILL_QUALITY_REPORT=0 to disable telemetry if proceeding.

Risk: VPC and subnet changes can disrupt live networks; deletion is irreversible.

Mitigation: Use least-privilege cloud credentials, preview every change, check resource dependencies, and obtain explicit confirmation before writing or deleting.

Risk: Installation modifies shell startup files and installs a persistent local wrapper.

Mitigation: Review the installation script and its local changes before execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-vpc-network-diagnosis-management)
- [Huawei Cloud VPC documentation](https://support.huaweicloud.com/vpc/)
- [Huawei Cloud VPC API Explorer](https://console.huaweicloud.com/apiexplorer/#/openapi/VPC/doc)
- [Least-privilege IAM policies](artifact/references/iam-policies.md)
- [CLI installation and authentication guide](artifact/references/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Shell commands]

**Output Format:** [Markdown with diagnostic findings and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only diagnosis can run automatically; resource changes require preview and confirmation.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
