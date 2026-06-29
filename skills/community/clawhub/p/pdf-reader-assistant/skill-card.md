## Description: <br>
PDF阅读助手 helps an agent extract, OCR, analyze, compare, and batch-process PDF documents, producing summaries, keywords, tables, image notes, and statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guipi888](https://clawhub.ai/user/guipi888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect user-provided PDFs, including ordinary and scanned documents. It supports text and table extraction, OCR-assisted reading, structured summaries, document comparison, and folder-level batch analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads PDF files or folders explicitly provided by the user, which can expose sensitive document contents to the agent. <br>
Mitigation: Only point the skill at PDFs or folders intended for analysis, and avoid broad or sensitive directories. <br>
Risk: Temporary extraction output may remain at /tmp/pdf_extract.json after analysis. <br>
Mitigation: Delete /tmp/pdf_extract.json after use when the agent creates it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guipi888/skills/pdf-reader-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown reports with JSON extraction data and optional shell or Python commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create /tmp/pdf_extract.json during analysis; optional OCR and table extraction depend on installed PDF libraries.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
