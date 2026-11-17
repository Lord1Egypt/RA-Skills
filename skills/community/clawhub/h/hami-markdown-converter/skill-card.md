## Description:

Converts PDFs, Office files, web and data files, media files, ZIP archives, YouTube URLs, and EPubs to Markdown with markitdown for LLM processing or text analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicenasa](https://clawhub.ai/user/nicenasa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to convert common document, data, web, archive, media, and URL inputs into Markdown that can be inspected, processed by LLMs, or used for text analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs the currently resolved `markitdown` package rather than a pinned, reviewed package version.

Mitigation: Use a pinned and reviewed markitdown version, especially for sensitive or regulated documents.

Risk: Azure, URL-based conversion, and third-party plugin paths can send content to external services or execute additional plugin code.

Mitigation: Run conversions in an isolated environment, avoid third-party plugins by default, and use Azure or URL-based conversion only when external processing is intended.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Markdown conversion guidance and command examples; converted document content may be written to stdout or output files by markitdown.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
