## Description:

Migrates WorkBuddy, QwenWork, and DuMate experts or expert suites into OfficeAce-compatible expert cards, skill directories, and teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to migrate packaged experts and expert suites from WorkBuddy, QwenWork, or DuMate into OfficeAce, then inspect whether the migrated files and registrations are ready to use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious due to reported package-boundary, overwrite, account-isolation, installation-scope, and confirmation concerns; its scan was incomplete.

Mitigation: Review the source package and destination before installation, use the default dry-run and verification steps, and follow the skill's cross-machine confirmation gate before any install.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-officeace-expert-migration)
- [Format mapping](references/format-mapping.md)
- [OfficeAce format](references/officeace-format.md)
- [Verification method](references/verification-method.md)
- [IAM policies](references/iam-policies.md)

## Skill Output:

**Output Type(s):** [Configuration, Files, Markdown, Shell commands]

**Output Format:** [OfficeAce expert and team configuration, skill Markdown, and migration or verification reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run by default; installation can create or update files and registrations.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
