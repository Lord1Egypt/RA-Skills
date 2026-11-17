## Description:

PDF to DOCX helps agents convert PDF documents into editable Word (.docx) files through MinerU, with support for local files, URLs, OCR, VLM mode, page ranges, and batch conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill when they need an agent to convert PDFs into editable Word documents while preserving text, tables, images, and layout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential PDFs may be processed through an external MinerU API workflow.

Mitigation: Do not convert sensitive documents unless the user accepts MinerU API handling of the document contents and token-protected requests.

Risk: Installing or running an unexpected mineru-open-api package could expose the environment to untrusted package behavior.

Mitigation: Install only from expected MinerU package sources, prefer a pinned version, and use an isolated environment.

Risk: DOCX conversion cannot stream to stdout, so missing output paths can cause failed or misplaced conversion results.

Mitigation: Always pass an explicit output directory with -o and verify the generated .docx file before using it.

## Reference(s):

- [MinerU homepage](https://mineru.net)
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU)
- [MinerU API token management](https://mineru.net/apiManage/token)
- [ClawHub skill page](https://clawhub.ai/mzlzyca/skills/pdf-to-docx)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands; conversion output is a .docx file written to an output directory.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mineru-open-api, MINERU_TOKEN authentication, and an explicit output directory because DOCX output cannot stream to stdout.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
