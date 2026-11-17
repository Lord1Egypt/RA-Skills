## Description:

Helps manage Huawei Cloud APIG dedicated instances, APIs, groups, publishing, policies, and public access through the hcloud CLI, with read-only diagnostics for access and policy effectiveness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inspect and manage dedicated Huawei Cloud API Gateway instances, APIs, publishing, access policies, and public ingress, and to diagnose configuration and policy issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required quality-reporting wrapper can send unredacted cloud command output and local agent session metadata to a remote service.

Mitigation: Review reporting before installation; avoid secret-returning operations through the wrapper and set SKILL_QUALITY_REPORT=0 if reporting is not wanted.

Risk: Installation modifies shell startup files and leaves a persistent wrapper in ~/.local/bin.

Mitigation: Review the installation steps and persistent PATH changes before running the installer.

Risk: Management and deletion commands can alter or remove cloud resources.

Mitigation: Use a least-privilege Huawei Cloud account, preview changes, and require explicit confirmation before destructive operations.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-apig-instance-management)
- [Huawei Cloud APIG documentation](https://support.huaweicloud.com/apig/)
- [IAM policies and least privilege](references/iam-policies.md)
- [CLI installation guide](references/cli-installation-guide.md)
- [Verification method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with CLI commands and diagnostic guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mutating operations require user confirmation; results are checked against read-back queries.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
