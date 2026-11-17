## Description:

Guides Teradata-to-Huawei Cloud DWS migration, including pre-checks, schema and data conversion, and validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to plan and run migrations from Teradata to Huawei Cloud DWS, convert database objects and data, and check migration results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Functional validation can execute stored procedures on the source Teradata system, contrary to the stated read-only expectation.

Mitigation: Use a read-only Teradata account without permission to execute write-capable procedures; run validate_functional.py with --skip-procs unless procedures have been reviewed.

Risk: Forcing schema changes or truncating target tables can overwrite existing DWS data.

Mitigation: Avoid --force and --truncate-before-import without backups and explicit approval of the target changes.

Risk: Incorrect DWS or OBS endpoints or credentials can direct migration data to unintended destinations.

Mitigation: Verify DWS and OBS endpoints, access permissions, and credentials before migration.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-dws-migration-teradata-to-dws)
- [Huawei Cloud DWS data type mapping](https://support.huaweicloud.com/migration-dws/dws_15_0131.html)
- [Migration guide](artifact/references/migration-guide.md)
- [Verification methods](artifact/references/verification-method.md)
- [Forbidden operations](artifact/references/forbidden-operations.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code]

**Output Format:** [Markdown with inline commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Migration scripts can produce JSON validation reports.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
