## Description:

Guides operators through Huawei Cloud SMS host migration, from pre-migration checks and task creation to progress monitoring and post-migration validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Experienced migration operators use this skill to plan and carry out host migrations to Huawei Cloud SMS, check source and destination readiness, troubleshoot migration issues, and report replication status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Migration credentials may be exposed through a hard-coded helper password or predictable temporary files containing access keys.

Mitigation: Use unique, short-lived credentials or keys and avoid predictable temporary files for AK/SK.

Risk: Broad SSH or migration-port access, or an unintended public IP, may expose migrated systems.

Mitigation: Restrict access to exact trusted CIDRs and require approval before SSH, EIP, or security-group changes.

Risk: Partition, bootloader, or disk repair commands may damage data or prevent the destination from booting.

Mitigation: Back up disks and require explicit approval before partition or bootloader changes.

Risk: Changing the root password or enabling password-based SSH login may weaken access controls.

Mitigation: Require explicit approval for root-password and SSH changes; use short-lived credentials or keys.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-sms-migration-assistant)
- [Migration reference](artifact/references/MIGRATION_REFERENCE.md)
- [Huawei Cloud SMS migration limits](https://support.huaweicloud.com/sms_faq/sms_faq_0007.html)
- [Huawei Cloud SMS API reference](https://support.huaweicloud.com/api-sms/sms_api_0001.html)
- [Huawei Cloud destination setup](https://support.huaweicloud.com/qs-sms/sms3_02_0009.html)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Analysis]

**Output Format:** [Markdown with command examples and check results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes migration status and pre- and post-migration checks.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
