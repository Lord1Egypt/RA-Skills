## Description:

Lists Huawei Cloud VPC subnets by region or VPC and returns a full-field table, JSON array, or names-only output through KooCLI with an SDK fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inventory Huawei Cloud VPC subnets, inspect their attributes, and retrieve subnet IDs, CIDRs, or gateway addresses for network operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says subnet inventory requires additional telemetry software without explaining what it collects or where it sends the data.

Mitigation: Before installation, request an optional telemetry workflow, a reviewed pinned package, and clear disclosure of collected data and its destination.

Risk: Subnet inventory requires cloud credentials with permission to read subnet information.

Mitigation: Use narrowly scoped credentials with only the required vpc:subnets:list permission, and configure credentials outside the agent conversation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/wlc-dev/skills/huawei-cloud-vpc-subnet-list)
- [KooCLI installation and credential guide](artifact/references/cli-installation-guide.md)
- [Least-privilege IAM policy](artifact/references/iam-policies.md)
- [Verification method and API details](artifact/references/verification-method.md)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Full-field text table, raw JSON array, or subnet name list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports region and VPC ID filters; paginates results automatically.]

## Skill Version(s):

1.0.9 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
