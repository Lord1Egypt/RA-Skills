## Description: <br>
View, extract, edit, and manipulate PDF files, including text extraction, text overlay and replacement, merging, splitting, rotating pages, and PDF metadata retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cmpdchtr](https://clawhub.ai/user/cmpdchtr) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, engineers, and document-focused agents use this skill to inspect PDF content, extract text, add overlays, reorganize pages, combine documents, split sections, rotate pages, and retrieve metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Accidental overwriting or unwanted changes to important PDFs when users choose unsafe output paths. <br>
Mitigation: Work on copies of important PDFs and use explicit new output filenames. <br>
Risk: PDF byte-level text replacement can be unreliable and may produce unexpected document changes. <br>
Mitigation: Prefer text overlays or extract-edit-regenerate workflows, and review generated PDFs before use. <br>
Risk: Dependency installation can affect the host Python environment. <br>
Mitigation: Install pdfplumber, PyPDF2, and reportlab in a virtual environment. <br>


## Reference(s): <br>
- [PDF Libraries Reference](references/libraries.md) <br>
- [ClawHub Release Page](https://clawhub.ai/cmpdchtr/pdf-tools) <br>
- [Publisher Profile](https://clawhub.ai/user/cmpdchtr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, PDF files, JSON, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, text or JSON command output, and generated PDF or text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local PDF files and caller-selected output paths; page numbers are 1-indexed.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
