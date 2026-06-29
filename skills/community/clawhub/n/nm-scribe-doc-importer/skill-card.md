## Description: <br>
Converts external documents (PDF, DOCX, PPTX, XLSX, HTML) into editable markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, documentation authors, and agents use this skill to convert PDF, DOCX, PPTX, XLSX, or HTML content into cleaned, sanitized markdown drafts for project documentation or rewriting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default output path may place a .md draft beside the source document, which could be ambiguous or overwrite an expected draft. <br>
Mitigation: Confirm the destination path before writing, especially when a markdown file may already exist next to the source document. <br>
Risk: External documents may contain embedded instructions, oversized sections, or conversion artifacts that could distort the imported markdown. <br>
Mitigation: Apply the content-sanitization checklist, wrap external content in boundary markers, truncate oversized sections, and mark unclear content for review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-scribe-doc-importer) <br>
- [Scribe plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scribe) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance] <br>
**Output Format:** [Markdown draft with cleanup notes and review markers when conversion artifacts are unclear] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a .md draft beside the source document or to a user-confirmed target path.] <br>

## Skill Version(s): <br>
1.9.13 (source: release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
