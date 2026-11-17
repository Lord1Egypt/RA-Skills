## Description:

Slices long images and screenshots into overlapping segments, adds sequence numbers, and arranges one or more source images into paginated PDFs with gaps and page numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wux818738-alt](https://clawhub.ai/user/wux818738-alt)

### License/Terms of Use:

GPL-3.0

## Use Case:

Legal professionals and agents assisting them use this skill to convert long chat, contract, email, SMS, or document screenshots into numbered, paginated PDFs for review, filing, printing, or archiving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer fetches mutable remote code and installs unpinned Python packages.

Mitigation: Review the release before installation, install from a pinned or reviewed local copy, and use an isolated virtual environment with pinned dependencies.

Risk: The skill instructions ask the agent to open generated PDFs automatically.

Mitigation: Ask the agent not to open generated PDFs unless explicit user confirmation is given.

Risk: Generated PDFs depend on the completeness and ordering of the source screenshots.

Mitigation: Verify source screenshot completeness, page order, and numbering before relying on the PDF for legal filing or archival use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with shell commands and generated PDF files when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports configurable tiling, overlap, grid layout, margins, page numbering, and optional cleanup of intermediate tile images.]

## Skill Version(s):

2.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
