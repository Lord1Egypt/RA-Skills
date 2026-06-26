## Description: <br>
Convert various document formats (PDF, Word, PowerPoint, Excel, images, audio, HTML, etc.) to Markdown using Microsoft's markitdown tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to install and run Microsoft's MarkItDown tooling for converting documents, images, audio, HTML, and supported URLs into Markdown for LLM and text analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL and YouTube conversion can involve upstream network behavior from MarkItDown or its dependencies. <br>
Mitigation: Review upstream behavior before converting remote URLs and prefer local files when network access is not required. <br>
Risk: Document, image, and audio conversion may expose confidential content to processing workflows. <br>
Mitigation: Avoid using confidential inputs unless the processing path and dependency behavior are understood. <br>
Risk: Broad Python dependency installation can increase local environment exposure. <br>
Mitigation: Install with pipx or a virtual environment and use minimal MarkItDown extras when only specific formats are needed. <br>


## Reference(s): <br>
- [Microsoft MarkItDown GitHub repository](https://github.com/microsoft/markitdown) <br>
- [MarkItDown on PyPI](https://pypi.org/project/markitdown/) <br>
- [MarkItDown MCP server](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown with command examples and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Converted content may be written to files or stdout depending on MarkItDown options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
