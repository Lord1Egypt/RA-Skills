## Description:

Excel全能工具箱 helps agents inspect, read, write, convert, merge, split, clean, validate, analyze, chart, pivot, compare, and protect Excel, CSV, TSV, and JSON spreadsheet files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muippt](https://clawhub.ai/user/muippt)

### License/Terms of Use:

MIT

## Use Case:

Employees, business analysts, HR and operations teams, and developers use this skill to automate local spreadsheet workflows such as previewing files, merging reports, cleaning and validating data, creating charts and pivot summaries, filling templates, and protecting sensitive workbooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic dependency installation can change the local Python environment.

Mitigation: Install the pinned requirements manually in a dedicated environment before running the skill.

Risk: Spreadsheet scripts can read, write, encrypt, decrypt, or overwrite files supplied by the user.

Mitigation: Use explicit separate output paths, confirm backups, and keep independent copies before write, protection, cleaning, splitting, or merge operations.

Risk: Passwords and sensitive spreadsheet data may be exposed through command-line arguments or agent conversation.

Mitigation: Avoid command-line passwords when possible and only process sensitive workbook contents with an approved local environment and agent provider.

## Reference(s):

- [API Reference](references/api-reference.md)
- [Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/muippt/skills/mu-excel-toolbox)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands; tool outputs may be JSON, CSV, Markdown, terminal tables, or spreadsheet files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local Python spreadsheet utilities; dependencies are pinned in scripts/requirements.txt and may be installed before execution.]

## Skill Version(s):

1.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
