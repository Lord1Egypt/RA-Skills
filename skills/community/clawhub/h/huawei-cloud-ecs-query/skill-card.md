## Description:

Queries Huawei Cloud ECS instances and status in read-only mode, with optional extended operational details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and engineers use this skill to inspect Huawei Cloud ECS instance lists, individual instance details, and instance status across configured regions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required quality wrapper is downloaded and installed, and its data handling and persistent behavior are not established by the package evidence.

Mitigation: Review the wrapper before installation or supplying credentials; prefer a release that removes it or makes an authenticated, pinned wrapper optional with clear data controls.

Risk: The configuration can contain sensitive cloud credentials.

Mitigation: Use dedicated read-only credentials, protect the configuration file, and have an administrator handle IAM grants separately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-ecs-query)
- [Huawei Cloud ECS API reference](artifact/references/api-reference.md)
- [CLI installation guide](artifact/references/cli-installation-guide.md)
- [IAM policies](artifact/references/iam-policies.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [Verification method](artifact/references/verification-method.md)
- [KooCLI official documentation](https://support.huaweicloud.com/usermanual-hcli/hcli_01_001.html)

## Skill Output:

**Output Type(s):** [Text, Tabular data, JSON]

**Output Format:** [Markdown table or JSON instance query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instance inventory, status, and details; extended fields depend on available read-only permissions.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
