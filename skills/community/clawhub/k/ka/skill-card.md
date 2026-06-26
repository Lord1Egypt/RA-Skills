## Description: <br>
Feishu document read/write operations. Activate when user mentions Feishu docs, cloud docs, or docx links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KaRi-code](https://clawhub.ai/user/KaRi-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to read, create, update, and append Feishu Docx documents, including block, table, image, and file operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite, update, or delete Feishu document content. <br>
Mitigation: Require explicit confirmation before overwrite, update, and deletion actions, naming the exact document token, block ID, and intended change. <br>
Risk: The skill can upload local files or URL-sourced content into Feishu documents. <br>
Mitigation: Require explicit confirmation before uploads, naming the exact local file path or URL and destination document or block. <br>


## Reference(s): <br>
- [Feishu Block Types Reference](references/block-types.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Files, Configuration] <br>
**Output Format:** [JSON action payloads and Markdown document content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports Feishu Docx document and block operations; uploads require exactly one URL or local file path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
