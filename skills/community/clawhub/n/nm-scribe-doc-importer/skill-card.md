## Description: <br>
Converts external documents (PDF, DOCX, PPTX, XLSX, HTML) into editable Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and documentation writers use this skill to convert local or URL-based PDF, DOCX, PPTX, XLSX, and HTML sources into editable Markdown for project documentation, rewriting, or integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive source documents may be processed by the configured conversion tools. <br>
Mitigation: Use the skill only with documents the user is comfortable sending through those tools, and avoid sensitive inputs unless the configured processing path is acceptable. <br>
Risk: Converted content may be written to an unintended location. <br>
Mitigation: Review the target output path before writing, and ask the user when the destination is ambiguous. <br>
Risk: Document conversion can produce garbled or unclear sections. <br>
Mitigation: Preserve substantive content, mark unclear sections with REVIEW comments, and inform the user about conversion limitations. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/athola/nm-scribe-doc-importer) <br>
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scribe) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Markdown files with review comments and brief status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include REVIEW comments for unclear conversion artifacts; image files may need separate handling.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
