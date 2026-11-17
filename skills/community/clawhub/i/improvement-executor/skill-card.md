## Description:

Applies approved improvement candidates to target files with backup and rollback support for Markdown sections and YAML frontmatter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to apply approved improvement candidates from ranking artifacts to single target files and to restore prior content from receipts or backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify or restore arbitrary local files without enough path checks.

Mitigation: Run it only in a constrained workspace and verify target paths, backup paths, ranking artifacts, and receipts before execution or rollback.

Risk: Safety claims around execute dry-run previews and rollback hash verification are overstated in the release evidence.

Mitigation: Do not rely on execute dry-run behavior or rollback hash verification unless the installed implementation is separately confirmed to enforce them.

Risk: Rollback with execution enabled can overwrite target files from a backup path.

Mitigation: Avoid rollback with --execute unless the backup source and destination target have been manually verified.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/skills/improvement-executor)
- [Publisher Profile](https://clawhub.ai/user/lanyasheng)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON execution receipts, rollback status JSON, Markdown diff previews, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces rollback pointers and file backup paths when execution succeeds.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
