## Description:

Lists Huawei Cloud VPCs and peering connections through read-only queries, with filtering and multiple output formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inventory Huawei Cloud VPCs and peering connections by region, filter results, and export VPC inventories as Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may install the separate skill-quality-cli tool from a remote release source.

Mitigation: Review the installer and release source, and verify the installer checksum before running it.

Risk: Environment-controlled command settings could undermine the intended read-only limits if untrusted parties can set them.

Mitigation: Run in a trusted environment and check command-related environment settings before execution.

Risk: The security scan was incomplete and does not establish that all components were inspected.

Mitigation: Review the supplied scripts before installation or use, especially the dependency setup and command execution paths.

## Reference(s):

- [KooCLI installation and credential guide](references/cli-installation-guide.md)
- [Least-privilege IAM policies](references/iam-policies.md)
- [API verification method](references/verification-method.md)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [ClawHub release page](https://clawhub.ai/wlc-dev/skills/huawei-cloud-vpc-list)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Shell commands]

**Output Format:** [Human-readable tables or name lists, JSON arrays, and local Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only VPC and peering inventory; paginated results and optional VPC filters.]

## Skill Version(s):

1.0.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
