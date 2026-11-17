## Description:

Helps plan and audit password-manager migrations and vault merges using counts and metadata rather than passwords or vault files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

People and teams migrating between password managers or merging vaults use this skill to choose an import route, map fields, inventory TOTP and attachment gaps, and audit item counts after import without sharing secrets with the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual password-manager exports may expose plaintext credentials.

Mitigation: Keep exports local and offline outside synced folders, avoid unnecessary copies, and delete temporary exports after confirming the import; never supply passwords or vault files to the skill.

Risk: Imports may silently omit TOTP seeds, attachments, or vault items.

Mitigation: Inventory TOTP entries and attachments, compare pre- and post-import counts, verify access and re-enrollment, and retain the old vault read-only until checks are complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/voronindenis5/skills/password-manager-migrator)
- [Route Matrix](references/route-matrix.md)
- [Audit Worksheet](references/audit-worksheet.md)

## Skill Output:

**Output Type(s):** [Guidance, JSON, CSV worksheet]

**Output Format:** [Markdown guidance and structured JSON containing a CSV field-mapping worksheet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses only supplied counts and metadata; does not read vault files or passwords.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
