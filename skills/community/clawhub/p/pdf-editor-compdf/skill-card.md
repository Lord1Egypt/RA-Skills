## Description: <br>
PDF Editor edits and organizes PDF pages with merge, insert, reorder, exchange, crop, split, extract, rotate, convert, optimize, compare, and watermark operations using ComPDF page management capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[compdf-youna](https://clawhub.ai/user/compdf-youna) <br>

### License/Terms of Use: <br>
Proprietary ComPDFKit SDK License <br>


## Use Case: <br>
External users and document-workflow teams use this skill to instruct an agent to prepare, restructure, convert, compress, compare, and watermark PDFs through the ComPDFKit CLI. It is suited to local PDF page-management tasks where the user accepts ComPDF's binary download and trial-license activation flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and runs an unpinned proprietary PDF CLI before first use. <br>
Mitigation: Confirm the download source, install only if the user trusts ComPDF's binary, and avoid using sensitive PDFs unless that trust decision is acceptable. <br>
Risk: Trial license activation sends the user's email address to ComPDF's license endpoint. <br>
Mitigation: Request explicit user confirmation before activation and proceed only with an email address the user is willing to share for licensing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/compdf-youna/skills/pdf-editor-compdf) <br>
- [ComPDFKit Home](https://www.compdf.com/?utm_source=clawhub&utm_medium=skillhub&utm_campaign=pdf_skill_pdf_editor&ref_platform_id=clawhub_skills) <br>
- [ComPDFKit Security Policy](https://www.compdf.com/security) <br>
- [Windows CLI Download](https://download.compdf.com/skills/winCLI/win.zip) <br>
- [Mac CLI Download](https://download.compdf.com/skills/macCLI/mac.zip) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with platform-specific shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides local PDF processing through a downloaded ComPDFKit CLI and can produce edited PDF files on disk.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
