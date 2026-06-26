## Description: <br>
知识蒸馏归档工具，将讨论成果按5类分类写入对应知识文档。支持小龙虾命令记忆库、专业工作知识、工作外知识、讨论过程、思维蒸馏五类归档。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mwangxiang](https://clawhub.ai/user/mwangxiang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers use this skill to distill conversation results into a local knowledge base, classify notes across five knowledge documents, and preserve concise conclusions after preview and confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can archive sensitive or private discussion content into local Markdown files. <br>
Mitigation: Review the preview and destination before confirming a save, and set KNOWLEDGE_BASE_PATH to a private folder for sensitive notes. <br>
Risk: Incorrectly distilled notes could make the knowledge base misleading or harder to audit. <br>
Mitigation: Confirm the proposed additions or edits before writing, and keep only concise final conclusions in the destination documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mwangxiang/knowledge-distill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mwangxiang) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration instructions] <br>
**Output Format:** [Markdown notes and preview text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local Markdown knowledge-base files only after user preview and confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
