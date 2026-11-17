## Description:

Use when parsing PDFs, DOCX, PPTX, XLSX, or images locally. Supports text extraction, JSON output with bounding boxes, batch processing, and page screenshots. No cloud dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricanwarfare](https://clawhub.ai/user/ricanwarfare)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate the local LiteParse CLI for document text extraction, JSON parsing with bounding boxes, selective page processing, batch parsing, and screenshot generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the LiteParse CLI through Homebrew depends on external package provenance.

Mitigation: Review the Homebrew package source and install path before using the CLI in managed environments.

Risk: Parsing and screenshot commands can write output files and may overwrite existing files at chosen paths.

Mitigation: Direct outputs to intentional or disposable directories and review target paths before batch processing.

## Reference(s):

- [LiteParse Document Parser on ClawHub](https://clawhub.ai/ricanwarfare/skills/liteparse-docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced CLI may produce text, JSON with bounding boxes, and page screenshots from local documents.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
