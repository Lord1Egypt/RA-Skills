## Description:

Use when a local PDF, JPG/JPEG, PNG, DOCX, PPTX, or XLSX must be parsed through PDRouter into Markdown, result.json, and images, or when later reading, extraction, search, summary, or Q&A depends on that parse. Triggers include NanoDoc parse, /openapi/nanodoc/parse, and PAODINGAI_API_KEY. Do not use for the direct nanodoc.ai API, unsupported file types, or knowledge-base chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paodingai](https://clawhub.ai/user/paodingai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing agents use this skill to parse one supported local document through PDRouter, then read its Markdown or structured JSON for extraction, search, summarization, or question answering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks this release suspicious because its installer uses an unpinned package and repository reference, and part of its executable script could not be fully inspected.

Mitigation: Pin and verify package and repository sources, review the complete executable before use, and limit the environment to only the credentials and access required.

## Reference(s):

- [NanoDoc--Parse on ClawHub](https://clawhub.ai/paodingai/skills/nanodoc-parse)
- [PDRouter platform](https://platform.paodingai.com)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files]

**Output Format:** [Extracted Markdown, result.json, figure images, and a JSON summary of output paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One supported document per invocation; extracted results may include images.]

## Skill Version(s):

1.5.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
