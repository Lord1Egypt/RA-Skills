## Description: <br>
Skill for using the command-line tool pdftk (PDFtk Server) for working with PDF files. Use when asked to merge PDFs, split PDFs, rotate pages, encrypt or decrypt PDFs, fill PDF forms, apply watermarks, stamp overlays, extract metadata, burst documents into pages, repair corrupted PDFs, attach or extract files, or perform any PDF manipulation from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhauga](https://clawhub.ai/user/jhauga) <br>

### License/Terms of Use: <br>
GNU General Public License (GPL) Version 2 <br>


## Use Case: <br>
Developers, operators, and document-processing teams use this skill to draft and adapt PDFtk shell commands for PDF manipulation tasks such as merging, splitting, rotating, encrypting, decrypting, filling forms, watermarking, and extracting metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing PDFtk from untrusted sources could introduce compromised binaries. <br>
Mitigation: Install only from trusted package managers or official PDFtk sources. <br>
Risk: Generated PDFtk commands can operate on the wrong files or paths if copied without review. <br>
Mitigation: Confirm input and output paths before running examples, and review generated PDFs before sharing them. <br>
Risk: Real PDF passwords can be exposed through shared chat transcripts or shell history. <br>
Mitigation: Avoid sharing real PDF passwords in prompts or commands that may be logged. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jhauga/pdftk-server) <br>
- [PDFtk Server Manual Reference](references/pdftk-man-page.md) <br>
- [PDFtk CLI Examples](references/pdftk-cli-examples.md) <br>
- [Download](references/download.md) <br>
- [PDFtk Server Manual](https://www.pdflabs.com/docs/pdftk-man-page/) <br>
- [PDFtk Version History](https://www.pdflabs.com/docs/pdftk-version-history/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include installation commands, PDFtk command examples, and cautions about paths, generated PDFs, and password handling.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and release changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
