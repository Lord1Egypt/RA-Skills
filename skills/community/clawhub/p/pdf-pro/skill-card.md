## Description:

Pdf Pro provides PDF editing tools for merging, splitting, rotating, compressing, converting, encrypting, decrypting, extracting pages, and viewing PDF metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document operators use this skill to perform local PDF maintenance tasks such as combining, splitting, extracting, rotating, compressing, converting, encrypting, decrypting, and inspecting PDF files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF passwords may be exposed when provided on the command line or entered in recorded or shared terminals.

Mitigation: Avoid passing passwords on the command line and avoid recorded or shared terminal sessions when encrypting or decrypting PDFs.

Risk: PDF decryption can be used on documents the user is not authorized to modify.

Mitigation: Use the skill only on PDFs you own or are explicitly authorized to decrypt or modify.

Risk: Unpinned PDF-processing dependencies can change document handling behavior across installations.

Mitigation: Install dependencies in a virtual environment with pinned versions where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sxliuyu/skills/pdf-pro)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and file paths; commands produce PDF, image, or metadata outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operates on local PDF and image files and may read or write document metadata and password-protected PDFs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
