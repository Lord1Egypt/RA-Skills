## Description:

Uses the MinerU Agent lightweight API to convert PDFs, Word documents, PowerPoint files, Excel files, and images into Markdown without requiring an API token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haxck](https://clawhub.ai/user/haxck)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to parse user-provided documents or document URLs into Markdown for downstream extraction, OCR, table analysis, and summarization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents and URLs are sent to MinerU and its upload storage for parsing.

Mitigation: Use only documents and links that are appropriate to share with that service, and avoid confidential, regulated, internal, secret-bearing, or pre-signed URLs unless an explicit review permits it.

Risk: The workflow trusts service-provided upload and Markdown download URLs.

Mitigation: Add user confirmation, URL allowlisting, destination validation, and request timeouts before routine or automated use.

## Reference(s):

- [MinerU Agent API documentation](https://mineru.net/apiManage/docs)
- [MinerU Agent API endpoint](https://mineru.net/api/v1/agent)
- [ClawHub skill page](https://clawhub.ai/haxck/skills/mineru-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown text written to stdout or an output file, with status messages on stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports URL or local-file input, language selection, optional PDF page ranges, and a polling timeout.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
