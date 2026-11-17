## Description:

PDF Editor helps agents edit and organize PDFs with ComPDFKit page-management operations such as merge, split, extract, insert, reorder, rotate, delete, watermark, convert, optimize, and compare.

This skill is ready for commercial/non-commercial use.

## Publisher:

[compdf-youna](https://clawhub.ai/user/compdf-youna)

### License/Terms of Use:

Proprietary ComPDFKit SDK License

## Use Case:

External users and developers use this skill to run local PDF cleanup, restructuring, conversion, watermarking, compression, and comparison tasks through platform-specific ComPDFKit CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs a persistent native ComPDFKit CLI from mutable external URLs without hash or signature verification.

Mitigation: Install only when the publisher and download host are trusted, review the download URL before first use, and run the agent with access limited to the PDFs and output folders needed for the task.

Risk: First-use license activation sends the user's email address to the ComPDFKit license service.

Mitigation: Ask for explicit user confirmation before activation and use an email address appropriate for trial licensing.

Risk: PDF editing commands can overwrite or transform user documents when output paths or overwrite flags are misused.

Mitigation: Prefer working on copies, set explicit output paths, and use overwrite only when the requested replacement is intentional.

## Reference(s):

- [ClawHub PDF Editor skill page](https://clawhub.ai/compdf-youna/skills/pdf-editor-compdf)
- [ComPDFKit homepage](https://www.compdf.com/?utm_source=clawhub&utm_medium=skillhub&utm_campaign=pdf_skill_pdf_editor&ref_platform_id=clawhub_skills)
- [Windows CLI download](https://download.compdf.com/skills/winCLI/win.zip)
- [macOS CLI download](https://download.compdf.com/skills/macCLI/mac.zip)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with platform-specific shell commands and generated PDF files from the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local PDF paths, curl, Windows or macOS, and one-time CLI download and license activation.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
