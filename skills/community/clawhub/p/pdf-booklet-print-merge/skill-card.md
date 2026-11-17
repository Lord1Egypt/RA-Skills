## Description:

Merge PDF files and create booklet-ready 2-up duplex output for saddle-stitch printing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninjahwdragon](https://clawhub.ai/user/ninjahwdragon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-preparation users use this skill to merge local PDF files and generate booklet-ready 2-up duplex output for saddle-stitch, center-fold printing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Processing sensitive PDFs with an unpinned local dependency can introduce dependency supply-chain risk.

Mitigation: Use a virtual environment and install pypdf from a trusted index with a pinned or hash-checked dependency before processing sensitive PDFs.

Risk: Booklet imposition changes page order and may add blank padding pages.

Mitigation: Review the generated booklet PDF before printing or distributing it.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create booklet-imposed PDF files and optional sequentially merged PDF files through the bundled Python script.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
