## Description:

Generate Amazon KDP-compatible e-books from Markdown, low-content book interiors, book covers, cover prompts, publishing metadata, and batch production assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timyljob2011-sudo](https://clawhub.ai/user/timyljob2011-sudo)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and publishing operators use this skill to prepare Amazon KDP publishing assets, including EPUB files, low-content interior PDFs, cover prompts, generated covers, metadata, and batch book production plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated PDFs, EPUBs, HTML metadata reports, prompts, and KDP metadata may be unsuitable for publication without review.

Mitigation: Review all generated publishing artifacts before uploading, publishing, or sharing them.

Risk: Watermark-cropping guidance could be misused to hide provider attribution.

Mitigation: Use licensed, watermark-free images and do not use cropping to obscure attribution or usage restrictions.

Risk: Markdown or metadata from untrusted sources may carry active HTML into generated EPUB or HTML outputs.

Mitigation: Use trusted manuscript and metadata inputs, or inspect and sanitize active HTML before conversion.

Risk: Optional sudo-based font installation can change system-level font state.

Mitigation: Avoid sudo font installation unless intentionally managing system fonts; prefer isolated environments for KDP/book-production work.

## Reference(s):

- [Amazon KDP Help Center](https://kdp.amazon.com/help)
- [KDP Cover Calculator](https://kdp.amazon.com/cover-calculator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, shell commands, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of local PDF, EPUB, image, JSON, and production-list files for KDP workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
