## Description: <br>
Word文档处理工具套件，提供Word文档的创建、读取、内容提取和基本处理功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanghao20150901](https://clawhub.ai/user/wanghao20150901) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create Word documents, read existing .docx files, extract text, and handle simple table-based document workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local Word documents, so sensitive document contents may be exposed to the agent during extraction or summarization. <br>
Mitigation: Use it only on documents the agent is authorized to access, and avoid processing confidential files unless the workspace and agent policy permit it. <br>
Risk: The skill can write Word documents to local paths, which could overwrite existing files if paths are chosen carelessly. <br>
Mitigation: Use explicit output directories, review destination paths before execution, and keep backups for important documents. <br>
Risk: The skill depends on python-docx for document processing. <br>
Mitigation: Install python-docx from a trusted package source and keep the dependency current according to the runtime environment's package policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanghao20150901/openclawkit-word) <br>
- [Publisher profile](https://clawhub.ai/user/wanghao20150901) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, read, or extract local Word documents through python-docx when the agent runs the provided Python code.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
