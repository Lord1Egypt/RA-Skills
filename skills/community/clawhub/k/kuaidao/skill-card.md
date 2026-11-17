## Description:

快导(KD) helps agents generate and manage batches of short-video scripts for multiple platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitgily](https://clawhub.ai/user/gitgily)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operations teams use this skill to search trend inputs, apply platform rules, generate differentiated short-video scripts, write them to an Excel copy library, and produce execution reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Feishu setup requests broad workspace permissions.

Mitigation: Use local-only reports unless a tightly scoped Feishu app is required, and do not bulk-import the bundled permission set as-is.

Risk: The workflow can modify Excel copy-library files and includes rollback/delete behavior after failed verification.

Mitigation: Point configured paths only at files you control, keep backups, and confirm rollback or delete actions before running them.

Risk: Generated spreadsheet content may contain formula-like cell values.

Mitigation: Treat generated workbooks as untrusted until cell values are reviewed or sanitized before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gitgily/skills/kuaidao)
- [References directory overview](artifact/references/README.md)
- [Platform rules index](artifact/references/platform_rules/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, Python commands, configuration snippets, generated script text, Excel workbook updates, and local report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and openpyxl; uses web search for trend collection and optional Feishu/Lark tooling for report workflows.]

## Skill Version(s):

1.0.4 (source: server release metadata; packaged SKILL.md frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
