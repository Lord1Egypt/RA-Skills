## Description:

Convert PDF files to JPEG images with pdftoppm, support optional page ranges, and bundle generated JPGs into a zip archive for sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luohongq](https://clawhub.ai/user/luohongq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and other document workflow users use this skill to convert local PDF pages into JPEG files, optionally limiting conversion to a page range and packaging the generated images into a zip archive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow installs and invokes local command-line tools and scripts on user-selected PDFs.

Mitigation: Install poppler-utils from trusted package sources, review the scripts before running them, and process only PDFs the user is comfortable converting locally.

Risk: Generated JPEG files are written beside the source PDF and optional zip archives may be created.

Mitigation: Run the scripts in a controlled working directory and inspect generated files before sharing or archiving them.

Risk: Script prompts and error messages are in Chinese, which may be unclear to some users.

Mitigation: Prefer passing explicit command-line arguments and translate prompts or messages when needed before operational use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and script usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local JPEG files beside the source PDF and can create a zip archive of matching generated images.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
