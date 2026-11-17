## Description:

Converts document attachments into Markdown so text-only agents can read, summarize, quote, or store their contents, with optional OCR for scanned PDFs and images when an OpenAI-compatible vision key is configured.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keepyaoung](https://clawhub.ai/user/keepyaoung)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of text-only agents use this skill to convert PDFs, Office documents, spreadsheets, web and structured data files, EPUBs, ZIPs, and Markdown into agent-readable Markdown. When OCR credentials are intentionally configured, they can also extract text from scanned PDFs and image-based inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run unpinned third-party code.

Mitigation: Pin package versions or commit SHAs before use and install only in a constrained environment.

Risk: The converter can read local documents accessible to its process.

Mitigation: Limit runtime access to the specific input document and output directory, and avoid broad filesystem mounts.

Risk: Optional OCR may use API credentials and process sensitive image-based content.

Mitigation: Provide OCR credentials only when vision OCR is intentionally needed, and avoid persisting converted sensitive documents unless the user explicitly requests it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/keepyaoung/skills/markitdown-skill-for-non-multimodal-agent)
- [Microsoft MarkItDown](https://github.com/microsoft/markitdown)
- [Self-made-Orange MarkItDown Fork](https://github.com/Self-made-Orange/markitdown)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces converted document text for agent use; optional OCR requires an API key and may incur vision-model costs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
