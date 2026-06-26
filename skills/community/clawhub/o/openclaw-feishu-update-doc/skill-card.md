## Description: <br>
更新飞书云文档，支持追加、覆盖、定位替换、全文替换、前后插入和删除等 7 种更新模式。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenfa188](https://clawhub.ai/user/chenfa188) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users editing Feishu cloud documents use this skill to update targeted document sections, append content, replace text, delete ranges, and optionally rename documents. It is most useful when precise document IDs, modes, and selections are available for controlled edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Overwrite, delete_range, replace_all, and title updates can remove or broadly change document content. <br>
Mitigation: Provide exact document IDs and precise selections, prefer localized edits, and manually review high-impact operations before execution. <br>
Risk: Full-document overwrite can lose rich Feishu content such as images, comments, whiteboards, spreadsheets, or tasks that cannot be reconstructed from markdown. <br>
Mitigation: Avoid overwrite unless the document can be safely rebuilt, and target plain-text ranges around non-reconstructable content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenfa188/openclaw-feishu-update-doc) <br>
- [Publisher profile](https://clawhub.ai/user/chenfa188) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides Feishu document edit operations and describes success, asynchronous task, warning, and error response shapes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
