## Description:

Creates Huawei Cloud OBS buckets and provides guidance on bucket properties, access settings, and the creation process.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and developers use this skill to create, list, and inspect Huawei Cloud OBS buckets, including setting the region, storage class, and access permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags an unverified telemetry tool around credential-related commands; its data handling could not be verified from this release.

Mitigation: Review the reporting implementation and downloaded tool before use, use narrowly scoped cloud credentials, and configure credentials outside the telemetry wrapper. The documented SKILL_QUALITY_REPORT=0 setting is available, but its effectiveness was not verified.

Risk: Bucket creation can use public access settings, which may expose stored data.

Mitigation: Keep the private ACL by default and require explicit approval before enabling public access.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-obs-bucket-create)
- [OBS regions and endpoints](https://developer.huaweicloud.com/intl/en-us/endpoint)
- [KooCLI Installation Guide](https://support.huaweicloud.com/cli-koocli/koocli_01_0001.html)
- [CLI Installation Guide](artifact/references/cli-installation-guide.md)
- [Common Errors and Solutions](artifact/references/trouble-shooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can create one or more OBS buckets and set bucket options.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
