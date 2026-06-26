## Description: <br>
此技能用于创建符合中国政府及央企规范的Word文档(.docx)。当用户要求创建公文、国央企文档、规范文书、正式报告等需要特定中国公文格式的文档时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a-lhliang](https://clawhub.ai/user/a-lhliang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, analysts, and developers use this skill to generate formal Chinese government and state-owned-enterprise Word documents with prescribed page layout, fonts, heading levels, tables, images, page numbers, and signature blocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI writes a .docx file to the output path supplied by the user. <br>
Mitigation: Choose a non-sensitive destination and avoid filenames that would overwrite important local documents. <br>
Risk: Marketplace capability tags mention wallet or sensitive credential use even though the reviewed artifacts do not support that behavior. <br>
Mitigation: Treat the skill as a local Word document formatting helper and do not provide wallet details, credentials, or other secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a-lhliang/gov-doc-writing) <br>
- [Publisher profile](https://clawhub.ai/user/a-lhliang) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples and local .docx file generation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces user-requested Word .docx files at caller-specified local output paths.] <br>

## Skill Version(s): <br>
1.10.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
