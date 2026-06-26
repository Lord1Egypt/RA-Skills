## Description: <br>
Convert documents and files to Markdown using markitdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niceNASA](https://clawhub.ai/user/niceNASA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and analysts use this skill to convert documents, spreadsheets, web/data files, media, archives, and selected URLs into Markdown for LLM processing or text analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an external converter through `uvx markitdown`, so conversion behavior depends on that package source and runtime dependency resolution. <br>
Mitigation: Install and run it only where the package source and execution environment are trusted. <br>
Risk: Optional Azure Document Intelligence, remote URL conversion, and third-party plugins can expose sensitive documents or depend on services and plugins outside the artifact. <br>
Mitigation: Use cloud processing, remote URLs, and `--use-plugins` only when the relevant service, source URL, and installed plugins are intentionally trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/niceNASA/hami-markdown-converter) <br>
- [Publisher profile](https://clawhub.ai/user/niceNASA) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Converted output may preserve headings, tables, lists, links, and extracted metadata where supported by markitdown.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
