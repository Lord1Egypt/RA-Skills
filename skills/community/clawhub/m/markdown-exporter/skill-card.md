## Description: <br>
Converts Markdown files into DOCX, PPTX, XLSX, PDF, PNG, HTML, notebooks, data formats, and extracted code files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bowenliang123](https://clawhub.ai/user/bowenliang123) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and other users use this skill to ask an agent to convert Markdown files into document, presentation, spreadsheet, image, web, notebook, structured data, or source-code outputs with the markdown-exporter CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or overwrite files at output paths selected by the user. <br>
Mitigation: Use a dedicated output folder, verify input and output paths before running commands, and avoid pointing outputs at important existing files unless replacement is intended. <br>
Risk: The skill depends on the third-party md-exporter package and markdown-exporter binary. <br>
Mitigation: Install only if you trust the md-exporter package and publisher. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bowenliang123/markdown-exporter) <br>
- [Markdown Exporter project homepage](https://github.com/bowenliang123/markdown-exporter) <br>
- [md-exporter PyPI package](https://pypi.org/project/md-exporter/) <br>
- [Pandoc slide show syntax](https://pandoc.org/MANUAL.html#slide-shows) <br>
- [Markdown table syntax](https://www.markdownguide.org/extended-syntax/#tables) <br>
- [Markdown fenced code blocks](https://www.markdownguide.org/extended-syntax/#fenced-code-blocks) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands; generated artifacts may be DOCX, PPTX, XLSX, PDF, PNG, HTML, IPYNB, Markdown, CSV, JSON, JSONL, XML, LaTeX, ZIP, or extracted code files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [All commands use file paths for inputs and outputs; some conversions can create multiple output files.] <br>

## Skill Version(s): <br>
3.6.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
