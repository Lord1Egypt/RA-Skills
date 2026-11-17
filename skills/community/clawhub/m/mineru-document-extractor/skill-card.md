## Description:

MinerU Document Extractor helps agents convert PDFs, scanned documents, images, Word, PowerPoint, Excel, and web pages into Markdown, HTML, LaTeX, DOCX, or JSON using the mineru-open-api CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mineru-extract](https://clawhub.ai/user/mineru-extract)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and data engineers use this skill to extract structured content from documents and web pages, choose between fast token-free extraction and token-authenticated precision extraction, and save results to stdout or files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document or webpage content is transmitted to the MinerU API for server-side extraction.

Mitigation: Use the skill only for content approved for remote processing, and avoid sensitive private documents or internal URLs unless that use is authorized.

Risk: Authenticated modes use a MinerU token that may be provided through command flags, environment variables, or local configuration.

Mitigation: Manage MinerU tokens carefully, prefer environment or config storage over exposing tokens in command history, and review token access before shared or automated use.

Risk: The external mineru-open-api CLI is required to execute document extraction.

Mitigation: Install a pinned or reviewed CLI version where possible and verify the CLI before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mineru-extract/skills/mineru-document-extractor)
- [MinerU CLI reference](https://github.com/opendatalab/MinerU-Ecosystem/tree/main/cli)
- [MinerU API token management](https://mineru.net/apiManage/token)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated extraction outputs such as Markdown, HTML, LaTeX, DOCX, and JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write extraction results to stdout or an output directory; token-authenticated modes can support batch processing and additional formats.]

## Skill Version(s):

0.1.30 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
