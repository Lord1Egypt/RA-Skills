## Description:

Guides host migration from on-premises and third-party clouds to Huawei Cloud ECS or Flexus X using Server Migration Service (SMS).

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Infrastructure engineers and developers use this skill to assess source hosts, prepare Huawei Cloud migration targets, coordinate replication and cutover, and verify migration outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloaded agent installers or scripts can execute with elevated privileges.

Mitigation: Use verified packages or independently validate downloads before running them with sudo or Administrator rights.

Risk: Migration commands can change infrastructure or delete tasks and templates.

Mitigation: Confirm target identifiers and migration completion before cutover or deletion; review and edit templates before use.

Risk: Cloud access keys may be exposed through shared terminals or logs.

Mitigation: Use least-privilege temporary credentials where possible and keep access keys out of shared terminals and logs.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-sms-host-migrator)
- [Pre-migration checklist](references/pre-migration-checklist.md)
- [Agent deployment guide](references/agent-deployment-guide.md)
- [IAM policies](references/iam-policies.md)
- [Migration verification method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review region, project, network, and server identifiers before executing changes.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
