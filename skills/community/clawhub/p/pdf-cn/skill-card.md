## Description: <br>
PDF 文档处理 | PDF Document Processing. 读取、提取、合并、分割 PDF | Read, extract, merge, split PDFs. 支持文本提取、表格识别、注释 | Supports text extraction, table recognition, annotations. 触发词：PDF、pdf. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohongbin-git](https://clawhub.ai/user/guohongbin-git) <br>

### License/Terms of Use: <br>
Anthropic Terms of Service <br>


## Use Case: <br>
Developers and document-processing users use this skill to guide PDF reading, text and table extraction, page conversion, merging, splitting, annotation, and form-filling workflows. It provides practical Python and command-line patterns plus helper scripts for local PDF tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local PDF operations can overwrite or alter important documents if input and output paths are chosen carelessly. <br>
Mitigation: Use copies for important documents and review output paths before running the helper scripts or command-line tools. <br>
Risk: Password-protected PDFs may contain sensitive or restricted content. <br>
Mitigation: Only decrypt or process password-protected PDFs when you have permission to access them. <br>
Risk: The skill relies on local PDF tooling and files selected by the user. <br>
Mitigation: Install and use it only when comfortable allowing the agent to run local PDF tools on chosen files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/guohongbin-git/pdf-cn) <br>
- [Publisher Profile](https://clawhub.ai/user/guohongbin-git) <br>
- [PDF Processing Guide](artifact/SKILL.md) <br>
- [PDF Form Filling Guide](artifact/forms.md) <br>
- [PDF Processing Advanced Reference](artifact/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline Python, JavaScript, shell commands, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify local PDF, image, JSON, text, spreadsheet, and annotation output files when the user runs the referenced tools.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
