## Description:

Enterprise document automation suite for AI Agents. Generate professional Word contracts and Excel reports with one function call. Built-in 10 contract templates, 6 Excel templates, and report templates. No external template files required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deki18](https://clawhub.ai/user/deki18)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use Office Pro to generate Chinese-language business contracts, reports, and Excel workbooks from built-in templates with a simplified Python API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe output filenames may overwrite arbitrary writable paths.

Mitigation: Only allow trusted output filenames, reject absolute paths and parent-directory components, and write generated files inside a dedicated output directory.

Risk: Untrusted spreadsheet cell values may introduce unsafe or misleading workbook content.

Mitigation: Use trusted data sources for spreadsheet generation and review generated workbooks before sharing or opening in sensitive environments.

Risk: Generated contracts, rosters, invoices, and reports may contain sensitive business or personal data.

Mitigation: Apply normal document access controls and storage retention practices before distributing generated files.

## Reference(s):

- [Office Pro Skill Page](https://clawhub.ai/deki18/skills/office-pro)
- [README](artifact/README.md)
- [Skill Manifest](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [DOCX and XLSX files with returned output path strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files may include contracts, reports, spreadsheets, charts, or styled Word documents.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
