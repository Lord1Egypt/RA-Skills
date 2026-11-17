## Description:

Luban Skill helps agents manage Luban game configuration spreadsheets, including CRUD workflows for enums, Beans, data tables, fields, and rows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caixukunmax](https://clawhub.ai/user/caixukunmax)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game configuration engineers use this skill to inspect and edit Luban Excel-based game data, including enums, Beans, table structures, fields, and rows. It guides read operations directly and requires explicit user confirmation before write, update, and delete actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A code-generation command can execute unsafe shell input when untrusted values are passed into gen, --luban-cmd, --output, or --data-dir.

Mitigation: Use only in trusted Luban repositories, avoid passing user-supplied text into those parameters, and replace shell-string execution with argument-list subprocess calls before sensitive use.

Risk: Write, update, and delete operations can permanently change Excel configuration data.

Mitigation: Require explicit user confirmation with the target file and operation details, check references before deletions, avoid --force, keep backups, and validate after changes.

Risk: Dependency drift in openpyxl can change Excel parsing behavior or introduce package supply-chain risk.

Mitigation: Pin openpyxl to a reviewed version and install dependencies from trusted package indexes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/caixukunmax/skills/luban-skill)
- [Command Reference](references/commands.md)
- [Requirements Reference](references/REFERENCE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured operation previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.8+ and openpyxl; write, update, and delete workflows require explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata); artifact frontmatter reports 3.8.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
