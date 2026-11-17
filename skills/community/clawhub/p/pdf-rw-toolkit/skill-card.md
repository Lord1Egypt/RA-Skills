## Description:

Read, extract, and generate PDF files. Use when user asks to read PDF content, extract text/tables, merge PDFs, fill forms, or generate PDFs from HTML/Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[droba07](https://clawhub.ai/user/droba07)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect PDF content, extract text or tables, combine and split documents, and generate PDFs from trusted HTML or Markdown sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML-to-PDF generation can fetch local files or network resources when processing untrusted HTML, Markdown, or CSS.

Mitigation: Use the generation path only with trusted inputs, or run it in a sandbox that blocks file:// access and private or internal network fetches.

Risk: Extracted tables from complex PDF layouts may be incomplete or misstructured.

Mitigation: Review extracted CSV or JSON before using it for decisions or downstream automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/droba07/skills/pdf-rw-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and generated files such as PDF, CSV, or JSON outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 with pdfplumber, pypdf, and weasyprint for the bundled scripts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
