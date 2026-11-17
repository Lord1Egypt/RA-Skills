## Description:

Huawei Cloud RDS for MySQL risk reduction skill that converts a single instance to a primary/standby (HA) instance via the hcloud CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT

## Use Case:

Developers and cloud database administrators use this skill to assess and convert a Huawei Cloud RDS for MySQL single instance to a primary/standby high-availability deployment, including prechecks, cost assessment, monitoring, and result verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database verification or cleanup steps could result in data loss.

Mitigation: Review the documented risk and verification procedures, confirm backup coverage, and follow the skill's checks before cleanup or verification actions.

Risk: Cloud credentials used by the CLI could be exposed.

Mitigation: Use the documented least-privilege IAM permissions and the CLI's configured authentication; keep access keys and tokens out of prompts and command output.

Risk: The conversion cost assessment may not cover all ongoing costs, and prepaid conversion can charge the price difference automatically.

Mitigation: Review the returned quote, storage and backup costs, and prepaid balance before deciding whether to proceed.

Risk: The single-to-HA conversion is irreversible and could be run without informed confirmation.

Mitigation: Review the precheck, target instance and zone, and quoted cost, then provide explicit confirmation before conversion.

## Reference(s):

- [Huawei Cloud RDS Single-to-HA API](https://support.huaweicloud.com/api-rds/rds_01_0103.html)
- [Huawei Cloud RDS Single-to-HA User Guide](https://support.huaweicloud.com/usermanual-rds-mysql/rds_05_0023.html)
- [Huawei Cloud KooCLI Installation](https://support.huaweicloud.com/qs-hcli/hcli_02.html)
- [KooCLI Usage Guide](https://support.huaweicloud.com/usermanual-hcli/hcli_05_01.html)
- [Risks and Impact](artifact/references/risks-and-impact.md)
- [Cost Estimation](artifact/references/cost-estimation.md)
- [IAM Policies](artifact/references/iam-policies.md)
- [Business Verification](artifact/references/business-verification.md)
- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-rds-mysql-replica-promotion)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, JSON, Files]

**Output Format:** [Markdown guidance with tables and shell commands, plus JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local precheck, cost estimate, and monitoring report files; the cloud conversion requires explicit user confirmation.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
