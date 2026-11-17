## Description:

Obsidian Sheet Plus helps agents read, write, format, filter, and manage Obsidian spreadsheet data through the Sheet Plus plugin REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljcoder2015](https://clawhub.ai/user/ljcoder2015)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Obsidian users use this skill to automate spreadsheet workflows in Obsidian, including reading workbook data, updating ranges, applying formulas and formatting, managing filters, and creating or restructuring sheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read or change workbook data through a local REST API that may run without authentication.

Mitigation: Enable the API key option when available, keep the service bound to localhost, and install the skill only for intentional Obsidian Sheet Plus automation.

Risk: Workbook edits such as overwrites, clears, deletes, merges, and bulk formatting can have high impact if applied to the wrong sheet or range.

Mitigation: Require explicit confirmation for full-workbook export and destructive or bulk operations, and verify sheet names and ranges before execution.

## Reference(s):

- [Source repository](https://github.com/ljcoder2015/obsidian-sheet-plus-skill)
- [ClawHub skill page](https://clawhub.ai/ljcoder2015/skills/obsidian-sheet-plus-skill)
- [Publisher profile](https://clawhub.ai/user/ljcoder2015)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with curl examples, JSON request bodies, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides an agent to call a local Obsidian Sheet Plus REST API and to verify API availability and target sheet names before operations.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
