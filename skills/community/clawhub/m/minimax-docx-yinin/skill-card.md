## Description: <br>
Creates, edits, formats, previews, and validates DOCX documents using OpenXML SDK (.NET) workflows, CLI commands, C# examples, and document-design references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinin2005](https://clawhub.ai/user/yinin2005) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, document automation users, and agents use this skill to create new Word documents, edit or fill existing DOCX files, and apply template formatting with validation. It is suited to reports, proposals, contracts, forms, academic documents, and CJK document layouts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document requests can trigger local setup commands, dependency installation, and persistent environment changes. <br>
Mitigation: Review setup.sh before running it, prefer minimal setup where possible, and require confirmation before installing dependencies or modifying the environment. <br>
Risk: The skill can read arbitrary local paths and change existing documents while processing DOCX tasks. <br>
Mitigation: Limit operations to user-approved files and directories, keep backups of source documents, and confirm before overwriting or altering existing files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yinin2005/minimax-docx-yinin) <br>
- [Scenario A: Creating a New DOCX from Scratch](references/scenario_a_create.md) <br>
- [Scenario B: Editing / Filling Content in Existing DOCX](references/scenario_b_edit_content.md) <br>
- [Scenario C: Apply Template Formatting](references/scenario_c_apply_template.md) <br>
- [XSD Validation Guide](references/xsd_validation_guide.md) <br>
- [OpenXML Child Element Ordering Rules](references/openxml_element_order.md) <br>
- [OpenXML Unit Conversion Quick Reference](references/openxml_units.md) <br>
- [Typography Guide](references/typography_guide.md) <br>
- [CJK Typography Guide](references/cjk_typography.md) <br>
- [Design Principles for Document Typography](references/design_principles.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, C# code snippets, and DOCX files when the workflows are executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install or require local dependencies such as .NET SDK, NuGet packages, pandoc, or LibreOffice; workflows can read, create, and modify DOCX-related files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, artifact metadata, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
