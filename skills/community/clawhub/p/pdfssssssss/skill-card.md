## Description:

Use this skill whenever the user wants to do anything with PDF files, including extracting text or tables, merging, splitting, rotating, watermarking, creating PDFs, filling forms, encrypting or decrypting, extracting images, and OCR on scanned PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mockerzxy](https://clawhub.ai/user/mockerzxy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect, transform, create, and fill PDF documents with Python libraries, command-line tools, and bundled helper scripts. It supports workflows that produce local PDFs, extracted text, structured JSON, tables, and page images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF parsing and OCR workflows may process untrusted or malformed documents.

Mitigation: Treat untrusted PDFs as hostile parser inputs and process them in an isolated environment when possible.

Risk: Some examples and helper scripts create or overwrite local PDF, JSON, text, and image outputs.

Mitigation: Work on copies of important documents and review output paths before running commands.

## Reference(s):

- [PDF form processing guide](forms.md)
- [PDF processing advanced reference](reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline code and shell commands, plus generated local PDF, JSON, text, and image files when helper scripts are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Works locally on user-provided PDF files and may require optional PDF, OCR, image, and command-line dependencies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
