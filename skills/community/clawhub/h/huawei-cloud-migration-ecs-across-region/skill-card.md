## Description:

Runs and troubleshoots Huawei Cloud MGC/SMS server migrations with Terraform, including rsync fallback paths and post-migration verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to plan, run, verify, and troubleshoot single-server migrations to Huawei Cloud, including migrations from AWS EC2 and on-premises VMware sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Migration actions can change server access, expose SSH, or switch billing projects beyond stated safeguards.

Mitigation: Have an administrator review before production use; approve exact source and destination server IDs and billing projects, take backups, protect target SSH files, enforce host verification, restrict inbound SSH, and use narrowly scoped credentials.

Risk: An SMS migration can overwrite data on the target ECS.

Mitigation: Confirm the target server and overwrite acceptance with the user before applying the migration, and take backups first.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-migration-ecs-across-region)
- [Migration runbook](references/runbook.md)
- [IAM permissions guidance](references/iam-policies.md)
- [Verification method](references/verification-method.md)
- [Acceptance criteria](references/acceptance-criteria.md)
- [Migration lessons learned](references/lessons-learned.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, JSON]

**Output Format:** [Markdown with shell commands and JSON migration results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate cloud resource changes and produce migration result files after required user confirmation.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
