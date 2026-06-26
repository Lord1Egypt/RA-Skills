## Description: <br>
使用微软 markitdown 库将多种文档格式（PDF、DOCX、PPTX、XLSX、XLS、CSV、JSON、TXT、EPUB、HTML等）转换为 Markdown，支持批量转换、保留格式和图片提取。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mapleshadow](https://clawhub.ai/user/mapleshadow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, document-maintenance teams, and agent users use this skill to convert PDFs, Office files, spreadsheets, HTML, text files, and ebooks into Markdown, either one file at a time or in batches. It can also extract document images into a selected local output directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency installation and optional system package commands can modify the runtime environment. <br>
Mitigation: Install MarkItDown in a virtual environment or with pipx, and run sudo package-install commands only when intentionally modifying the system. <br>
Risk: Batch conversion and image extraction create Markdown and image files and may overwrite same-named outputs. <br>
Mitigation: Use a dedicated output folder and review output paths before running conversion or extraction scripts. <br>


## Reference(s): <br>
- [Microsoft MarkItDown](https://github.com/microsoft/markitdown) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; scripts produce Markdown files and extracted image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local file outputs may be created or overwritten at the selected output paths.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
