## Description:

Skill for using the command-line tool pdftk (PDFtk Server) for working with PDF files. Use when asked to merge PDFs, split PDFs, rotate pages, encrypt or decrypt PDFs, fill PDF forms, apply watermarks, stamp overlays, extract metadata, burst documents into pages, repair corrupted PDFs, attach or extract files, or perform any PDF manipulation from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

GPL-2.0

## Use Case:

Developers, engineers, and document operations users use this skill to produce command-line guidance for PDFtk Server workflows such as merging, splitting, rotating, encrypting, decrypting, filling forms, watermarking, stamping, repairing, and extracting PDF metadata or attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF passwords or confidential file paths entered directly in shell commands can be exposed through shell history, logs, or process listings.

Mitigation: Avoid placing real PDF passwords directly in commands; use safer local secret-handling practices and review generated commands before execution.

Risk: Decrypted PDFs, extracted attachments, metadata reports, and repaired outputs may contain sensitive content.

Mitigation: Treat all generated or extracted files as sensitive, store them in controlled locations, and remove temporary outputs when no longer needed.

Risk: PDFtk's encryption examples may not satisfy modern confidentiality requirements for highly sensitive documents.

Mitigation: Prefer modern encryption tools for confidential documents and use PDFtk encryption only when it matches the user's security requirements.

Risk: Building PDFtk from downloaded source archives can introduce supply-chain risk.

Mitigation: Verify source archives and installation sources before building or installing PDFtk.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jhauga/skills/pdftk-server)
- [PDFtk Server Manual Reference](references/pdftk-man-page.md)
- [PDFtk CLI Examples](references/pdftk-cli-examples.md)
- [Download](references/download.md)
- [PDFtk Server License](references/pdftk-server-license.md)
- [Third-Party Materials](references/third-party-materials.md)
- [PDFtk Server Manual](https://www.pdflabs.com/docs/pdftk-man-page/)
- [PDFtk Version History](https://www.pdflabs.com/docs/pdftk-version-history/)
- [PDFtk License Information](https://www.pdflabs.com/docs/pdftk-license/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate on local PDF files and may create modified PDFs, metadata reports, or extracted attachments.]

## Skill Version(s):

1.0.1 (source: server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
