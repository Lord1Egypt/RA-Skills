## Description:

Organize and standardize Obsidian vaults for reliability and long-term maintainability. Use when designing or cleaning vault folder structure, enforcing file naming conventions, migrating messy vaults, reducing duplicate/ambiguous notes, or creating repeatable audit-and-fix workflows for Obsidian notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge workers, and agents maintaining Obsidian vaults use this skill to audit vault structure, propose deterministic folder and file naming changes, and guide migrations with dry-run and confirmation safeguards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The apply script can recursively rename Markdown files under any supplied path without enforcing that the path is an Obsidian vault.

Mitigation: Run the audit in dry-run mode first, confirm the exact intended vault path, avoid broad paths, create a fresh backup, and use --apply only after reviewing the proposed renames.

Risk: Bulk vault renames or moves can cause data loss or broken links if performed without a current backup and review.

Mitigation: Create a fresh local backup before bulk operations, inspect proposed changes, and pause when link integrity is uncertain.

Risk: Vault notes may contain private journals, credentials, or other sensitive content.

Mitigation: Keep operations local, avoid transmitting vault content to external services, and use the skill to identify deletion candidates rather than deleting notes automatically.

## Reference(s):

- [Folder Structure Standard](references/folder-structure.md)
- [Migration Checklist](references/migration-checklist.md)
- [File Naming Rules](references/naming-rules.md)
- [Safety Evaluation](SAFETY.md)
- [ClawHub Skill Page](https://clawhub.ai/snazar-faberlens/skills/obsidian-organizer-hardened)
- [Faberlens Guardrail Evidence](https://faberlens.ai/explore/obsidian-organizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces dry-run-first organization plans and local audit guidance; apply operations require explicit confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
