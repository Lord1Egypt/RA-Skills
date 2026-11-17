## Description:

Pdf Toolkit helps agents run local PDF merge, split, compression, conversion, and text extraction workflows without network access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newaiguy](https://clawhub.ai/user/newaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document automation agents use this skill to process PDFs locally, including merging, splitting, compressing, converting between PDFs and images, and extracting text. It is intended for offline document utility workflows where files remain on the user's machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell command construction can allow crafted filenames or page ranges to affect local command execution.

Mitigation: Use only trusted file paths and validated page-range inputs, and run the skill without elevated privileges.

Risk: The documentation recommends changing the global ImageMagick PDF policy, which can weaken host-wide PDF handling protections.

Mitigation: Avoid relaxing the global policy unless the host impact is understood and the change can be reversed.

Risk: PDF passwords passed directly in shell commands may be exposed through command history or process listings.

Mitigation: Do not put real PDF passwords directly in shell commands; use safer secret-handling patterns outside this skill when sensitive documents are involved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/newaiguy/skills/openclaw-pdf-tools)
- [ClawHub publisher profile](https://clawhub.ai/user/newaiguy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown instructions with JavaScript CLI commands and generated PDF, image, or text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally using system PDF utilities such as Poppler, Ghostscript, ImageMagick, img2pdf, or pdftk when installed.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill frontmatter, and manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
