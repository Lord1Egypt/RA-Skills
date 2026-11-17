## Description:

Helps administrators inspect and manage Huawei Cloud IAM users, groups, policies, agencies, login settings, and access keys with confirmation before changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and developers use this skill to review IAM access and manage identities, permissions, and credentials in a Huawei Cloud account. Write and delete operations require explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Password handling through shared temporary files may expose credentials.

Mitigation: Avoid password operations until the workflow no longer uses shared temporary files; meanwhile use only a sandbox or tightly controlled account.

Risk: The skill installs a persistent telemetry CLI without pinning or verifying its downloads; reporting is enabled by default.

Mitigation: Review before installation, pin and verify CLI downloads, and set SKILL_QUALITY_REPORT=0 to disable telemetry.

Risk: IAM writes and deletes can grant broad access or remove identities and credentials.

Mitigation: Preview every change, verify affected resources, and require explicit confirmation before write or delete actions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-iam-manage)
- [Huawei Cloud IAM API reference](https://support.huaweicloud.com/api-iam/iam_18_0001.html)
- [Huawei Cloud KooCLI installation](https://support.huaweicloud.com/cli/index.html)
- [IAM least-privilege policies](references/iam-policies.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with command previews and JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows the secret access key only once when creating an access key.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
