## Description: <br>
OpenClaw agent skill for converting documents to Markdown, with documentation and utilities for Microsoft's MarkItDown library across PDF, Word, PowerPoint, Excel, images, audio, HTML, and YouTube inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[karmanverma](https://clawhub.ai/user/karmanverma) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to turn local files, web pages, and supported media into Markdown for documentation retrieval, analysis, and batch processing. The skill provides guidance and a batch utility while conversion is performed by Microsoft's MarkItDown CLI or Python package installed separately. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional network, cloud, transcription, and plugin features may send document or media content outside the local environment. <br>
Mitigation: Use local-only conversion for confidential documents, and enable OpenAI, Azure Document Intelligence, audio/YouTube transcription, or plugins only when sharing the content is allowed and the provider or plugin source is trusted. <br>
Risk: The skill depends on the separately installed MarkItDown package and its selected extras. <br>
Mitigation: Install only if the MarkItDown package and dependencies are trusted, and review selected extras before deployment. <br>
Risk: Converting untrusted URLs can introduce avoidable exposure to external content or services. <br>
Mitigation: Avoid untrusted URLs and prefer known local files or trusted sources for conversion. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/karmanverma/markitdown-skill) <br>
- [Skill homepage](https://github.com/karmanverma/markitdown-skill) <br>
- [Microsoft MarkItDown](https://github.com/microsoft/markitdown) <br>
- [Usage guide](USAGE-GUIDE.md) <br>
- [API reference](reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and Python examples; conversion results are Markdown text or .md files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Batch conversion can write .md files; optional cloud, transcription, OCR, and plugin features depend on user-selected MarkItDown extras.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
