## Description:

Extracts clean, readable text from PDF files at the command line using PyPDF2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to extract plain text from PDFs for downstream processing, summarization, or archiving. It is suitable for reports, articles, and forms where command-line text output is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF text can contain confidential or sensitive information that may be exposed through terminal logs or shared output paths.

Mitigation: Use trusted local paths, avoid shared terminals or logs for confidential documents, and handle extracted text according to the document's sensitivity.

Risk: Choosing an existing output filename can overwrite that file.

Mitigation: Verify the output path before running the command and use a new filename when preserving existing content matters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/albionaiinc-del/skills/pdf-text-extract)
- [Publisher Profile](https://clawhub.ai/user/albionaiinc-del)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text or Markdown with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print extracted text to stdout or write it to a selected output file.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
