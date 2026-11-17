## Description:

Professional DOCX document creation, editing, and formatting using the OpenXML SDK (.NET), with pipelines for new documents, content editing, and template formatting with validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinin2005](https://clawhub.ai/user/yinin2005)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document automation agents use this skill to create, edit, fill, format, preview, and validate Microsoft Word DOCX documents. It is especially suited to formal reports, proposals, contracts, academic documents, CJK documents, and template-based formatting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow may install system packages, download and run Microsoft's .NET installer, update shell startup files, and restore NuGet packages.

Mitigation: Review setup scripts before installation, run setup manually where possible, use --minimal when appropriate, and avoid installing in sensitive environments unless those host changes are acceptable.

Risk: The skill may generate or modify DOCX files through local scripts and .NET/OpenXML tooling, so incorrect instructions or validation gaps could produce malformed or misleading documents.

Mitigation: Use the skill's preview, diff, merge-runs, XSD validation, business-rule validation, and gate-check steps before relying on generated documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinin2005/skills/minimax-docx-yinin)
- [OpenXML element order](references/openxml_element_order.md)
- [OpenXML units](references/openxml_units.md)
- [Scenario A: create documents](references/scenario_a_create.md)
- [Scenario B: edit content](references/scenario_b_edit_content.md)
- [Scenario C: apply template](references/scenario_c_apply_template.md)
- [Typography guide](references/typography_guide.md)
- [CJK typography](references/cjk_typography.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and C# code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to run local shell scripts and .NET/OpenXML tooling that produce or modify DOCX files.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
