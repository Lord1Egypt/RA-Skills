## Description:

Guides an agent through preparing, executing, and reporting on Huawei Cloud RDS high-availability failover drills with risk checks and safety gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud operators, and database reliability engineers use this skill to plan and run controlled Huawei Cloud RDS primary-standby failover drills, inspect risk signals, and produce readiness or execution reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live failover may be run against an unintended Huawei Cloud RDS instance if the configuration is not reviewed.

Mitigation: Set config/config.json to the exact target region and instance, then inspect experiment.json and risk_assessment.json before any --yes execution.

Risk: The execute phase can perform a real primary-standby role switch and may be unsafe when risk checks report serious or stale conditions.

Mitigation: Use prepare first, review the risk assessment, and avoid --force or live execution outside an approved test or maintenance window.

Risk: Overbroad cloud credentials could expand the impact of a mistaken failover run.

Mitigation: Use a least-privilege hcloud profile scoped to the intended RDS instance and the documented IAM actions.

## Reference(s):

- [huawei-cloud-rds-failover on ClawHub](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-rds-failover)
- [CLI installation guide](references/cli-installation-guide.md)
- [IAM policies](references/iam-policies.md)
- [Risk model](references/risk-model.md)
- [Verification method](references/verification-method.md)
- [Acceptance criteria](references/acceptance-criteria.md)
- [Huawei Cloud RDS product documentation](https://support.huaweicloud.com/productdesc-rds/zh-cn_topic_dashboard.html)
- [RDS API reference: StartFailover](https://support.huaweicloud.com/api-rds/rds_05_0013.html)
- [Huawei Cloud RDS CES metrics](https://support.huaweicloud.com/usermanual-rds-mysql/rds_06_0001.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration files, and generated HTML or Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces preparation artifacts, risk assessment JSON, execution results, and failover reports when run in the target environment.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
