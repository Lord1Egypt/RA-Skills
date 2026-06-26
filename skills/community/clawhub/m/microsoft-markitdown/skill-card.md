## Description: <br>
Use MarkItDown to convert various files (PDF, Word, Excel, PPT, images, audio, HTML, CSV, JSON, etc.) to Markdown format for LLM processing and text analysis. Also supports content extraction from ZIP archives, YouTube videos, and EPUB e-books. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other users use this skill to convert local documents, media, web exports, archives, and selected URLs into Markdown for LLM processing, search, summarization, or text analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional OCR, LLM image description, Azure Document Intelligence, and plugin flows may send document content to external services. <br>
Mitigation: Use local conversion for confidential files, disable plugins unless needed, and review provider data-handling terms before enabling cloud features. <br>
Risk: Installing every optional extra increases the dependency surface for the runtime environment. <br>
Mitigation: Install only the MarkItDown extras needed for the target file types, preferably in a virtual environment from a trusted source. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks; converted content may be returned as Markdown text or as a saved file path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May depend on optional MarkItDown extras, plugins, an OpenAI API key for LLM image descriptions, or Azure Document Intelligence configuration for cloud document processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
