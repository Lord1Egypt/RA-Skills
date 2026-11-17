## Description:

Convert various document formats (PDF, Word, PowerPoint, Excel, images, audio, HTML, etc.) to Markdown using Microsoft's markitdown tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert PDFs, Office documents, images, audio, HTML, YouTube URLs, archives, and text-based files into Markdown for LLM workflows and text analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned installation examples can install different MarkItDown or dependency versions over time.

Mitigation: Install in a dedicated virtual environment or container and pin reviewed versions before production use.

Risk: Document, media, or URL conversion can expose confidential content to local converters or remote-fetch behavior.

Mitigation: Avoid converting confidential documents or private media unless the execution environment and converter behavior are trusted.

## Reference(s):

- [Microsoft MarkItDown GitHub Repository](https://github.com/microsoft/markitdown)
- [Microsoft MarkItDown PyPI Package](https://pypi.org/project/markitdown/)
- [MarkItDown MCP Server](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp)
- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/skills/ms-markitdown)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and Python code examples; converted outputs are Markdown, JSON, HTML, or text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write converted files to a requested output path or return converted content to stdout.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
