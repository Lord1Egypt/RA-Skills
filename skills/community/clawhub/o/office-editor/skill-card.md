## Description:

Create or modify Word (.docx), Excel (.xlsx), and PowerPoint (.pptx) files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noah-wu66](https://clawhub.ai/user/noah-wu66)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create or edit Word documents, Excel workbooks, and PowerPoint presentations while checking required Python Office libraries before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Office files may contain unintended or incomplete content if the requested document details are ambiguous.

Mitigation: Review generated .docx, .xlsx, and .pptx files before sharing or relying on them.

Risk: Important local documents could be changed unexpectedly if an output path is unclear.

Mitigation: Use explicit output filenames and preserve originals by default; overwrite only when the user explicitly asks for it.

Risk: Missing Office libraries can prevent document creation or editing.

Mitigation: Check required imports first and report missing packages instead of attempting automatic installation.

## Reference(s):

- [python-docx API Summary](references/docx_api_summary.md)
- [python-pptx API Quick Reference](references/pptx_api_reference.md)
- [PowerPoint Chart Creation Guide](references/pptx_chart_guide.md)
- [Excel Charts Reference](references/xlsx_charts.md)
- [Excel Advanced Features Reference](references/xlsx_features.md)
- [Pandas & NumPy Integration](references/xlsx_pandas.md)
- [ClawHub Skill Page](https://clawhub.ai/noah-wu66/skills/office-editor)
- [Publisher Profile](https://clawhub.ai/user/noah-wu66)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with Python code and generated .docx, .xlsx, or .pptx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes concrete Office files to local target filenames and defaults edited documents to updated_* outputs unless overwrite is explicitly requested.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
