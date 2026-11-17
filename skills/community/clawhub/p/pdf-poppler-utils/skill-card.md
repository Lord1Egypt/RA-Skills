## Description:

A collection of PDF manipulation tools from the poppler-utils package for extracting text, images, metadata, splitting, merging, converting formats, managing attachments, and verifying signatures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xlionjuan](https://clawhub.ai/user/xlionjuan)

### License/Terms of Use:


## Use Case:

Developers and document-processing users use this skill to choose and run Poppler PDF utilities for metadata inspection, text and image extraction, page splitting and merging, format conversion, attachment handling, and signature checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes guidance that can change the user's Homebrew environment by unlinking Homebrew curl.

Mitigation: Require explicit user permission, confirm the exact curl conflict, and establish a rollback plan before running environment-changing commands.

Risk: Poppler options can bypass PDF owner restrictions, extract hidden content or attachments, sign documents, or fetch certificate data online.

Mitigation: Use these options only on PDFs the user is authorized to process, and avoid bypass, signing, extraction, or online certificate-fetching behavior unless the user explicitly requests it.

Risk: Several utilities create output files and can write many files from a single PDF.

Mitigation: Direct file-producing commands to an explicit output directory and review target filenames before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xlionjuan/skills/pdf-poppler-utils)
- [Debian poppler-utils manpages](https://manpages.debian.org/testing/poppler-utils/index.html)
- [Homebrew](https://brew.sh)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce file paths or PDF-derived files when the generated Poppler commands are executed by an agent.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
