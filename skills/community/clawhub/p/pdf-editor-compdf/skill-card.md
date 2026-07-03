## Description: <br>
PDF Editor helps agents edit and organize PDFs through ComPDFKit CLI commands for page management, conversion, optimization, comparison, and watermarking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[compdf-youna](https://clawhub.ai/user/compdf-youna) <br>

### License/Terms of Use: <br>
ComPDFKit SDK License Agreement <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to prepare or clean up local PDF files: split or merge documents, extract, rotate, delete, or insert pages, convert standards, optimize files, compare revisions, or manage watermarks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and runs a proprietary ComPDFKit CLI executable before use. <br>
Mitigation: Review the publisher and source before installation, inform the user before download, and run it only in environments where executing that local binary is acceptable. <br>
Risk: License activation sends the user's email address to ComPDF's license endpoint. <br>
Mitigation: Request the email only after user confirmation and use extra caution with sensitive PDFs unless the binary and publisher are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/compdf-youna/skills/pdf-editor-compdf) <br>
- [ComPDF homepage](https://www.compdf.com/?utm_source=clawhub&utm_medium=skillhub&utm_campaign=pdf_skill_pdf_editor&ref_platform_id=clawhub_skills) <br>
- [ComPDF security policy](https://www.compdf.com/security) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Files, Guidance] <br>
**Output Format:** [Markdown guidance with platform-specific shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or modifies local PDF files through a downloaded ComPDFKit CLI; first use may require CLI download and email-based trial license activation.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
