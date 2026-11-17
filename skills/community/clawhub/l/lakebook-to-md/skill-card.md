## Description:

Converts Yuque .lakebook exports into organized Markdown documents, Excel workbooks for laketable content, downloaded resources, and a conversion report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luhuiwang](https://clawhub.ai/user/luhuiwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base operators use this skill to convert Yuque Lakebook exports into local Markdown folders, Excel files for database-table documents, downloaded attachments or images, and a summary report for manual follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted Lakebook archives and metadata may overwrite files or trigger unsafe parsing behavior.

Mitigation: Run the skill only in a disposable sandbox or isolated workspace, and process only Lakebook exports from trusted sources.

Risk: Automatic image and attachment downloads may make unexpected network requests or fetch untrusted content.

Mitigation: Disable downloads unless required, review downloaded files before opening them, and prefer URL allowlisting or a reviewed fork for sensitive use.

Risk: The startup path may install Python dependencies into the active environment.

Mitigation: Use a virtual environment or disposable Python environment before running the startup script.

## Reference(s):

- [Lakebook To Md ClawHub release](https://clawhub.ai/luhuiwang/skills/lakebook-to-md)
- [YuqueExportToMarkdown upstream project](https://github.com/PZh101/YuqueExportToMarkdown)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with command examples; generated conversion output includes Markdown documents, Excel workbooks, downloaded resource files, and a Markdown conversion report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform network downloads for images or attachments and may install Python dependencies when invoked through the startup script.]

## Skill Version(s):

1.1.0 (source: server release metadata, SKILL.md frontmatter, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
