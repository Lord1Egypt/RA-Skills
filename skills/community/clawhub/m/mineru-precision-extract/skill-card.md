## Description:

MinerU Precision Extract helps agents convert PDFs, scanned documents, images, office documents, HTML files, and URLs into Markdown, HTML, LaTeX, DOCX, or JSON with table recognition, formula recognition, OCR, batch processing, and web crawling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mineru-extract](https://clawhub.ai/user/mineru-extract)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, researchers, and document-processing teams use this skill to guide high-accuracy extraction, OCR, table parsing, formula recognition, batch conversion, and web-page conversion workflows through the MinerU Open API CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local documents may be sent to an external MinerU API for processing.

Mitigation: Avoid confidential, regulated, or proprietary documents unless the processing location, service terms, and data handling are approved.

Risk: Authentication tokens can be supplied through environment variables or stored in local configuration.

Mitigation: Protect MINERU_TOKEN and ~/.mineru/config.yaml, remove unused tokens, and avoid exposing token values in logs or shared shells.

Risk: Global installation of the CLI package trusts the selected package source.

Mitigation: Install only from trusted package sources and consider pinning or separately verifying the CLI package before deployment.

Risk: Extraction outputs may include sensitive document content and extracted images on disk.

Mitigation: Use an explicit output directory with appropriate access controls and clean up generated files when they are no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mineru-extract/skills/mineru-precision-extract)
- [MinerU Homepage](https://mineru.net)
- [Metadata-Listed Source](https://github.com/MinerU-Extract/mineru-precision-extract)
- [MinerU Open API CLI](https://github.com/opendatalab/MinerU-Ecosystem/tree/main/cli)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides document extraction to stdout or output files; multi-format and binary outputs require an explicit output path.]

## Skill Version(s):

0.2.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
