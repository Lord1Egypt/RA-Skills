## Description: <br>
将 Markdown 文档转换为 Word 文档，专为中文文档设计，支持常见 Markdown 语法并统一使用仿宋字体。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AndyRong](https://clawhub.ai/user/AndyRong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, office workers, and technical writers use this skill to convert Chinese Markdown reports, daily updates, weekly updates, and similar office documents into formatted Word documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing dependencies from an untrusted package source could introduce supply-chain risk. <br>
Mitigation: Install python-docx from a trusted package index or approved internal mirror. <br>
Risk: Using an existing output path can overwrite a Word document. <br>
Mitigation: Choose a deliberate output path and confirm whether an existing file should be replaced before running the converter. <br>
Risk: Processing unintended Markdown files may expose or transform content the user did not mean to handle. <br>
Mitigation: Run the converter only on Markdown files the user intends to process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AndyRong/md2word-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [DOCX file plus concise command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a UTF-8 Markdown input path and writes a Word document to the requested output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
