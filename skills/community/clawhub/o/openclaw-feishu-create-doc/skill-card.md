## Description: <br>
Creates Feishu cloud documents from Lark-flavored Markdown and supports folders, wiki nodes, and wiki spaces as creation targets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenfa188](https://clawhub.ai/user/chenfa188) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to create formatted Feishu cloud documents from Markdown and place them in a personal space, folder, wiki node, or wiki space. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Feishu app with broad credentials could create documents in locations beyond the intended workspace area. <br>
Mitigation: Use a least-privilege Feishu app and confirm the target folder, wiki node, or wiki space before creating documents. <br>
Risk: Untrusted external media URLs in Markdown may be fetched and uploaded into Feishu documents. <br>
Mitigation: Only include media URLs that the user trusts and intends to add to the target Feishu workspace. <br>
Risk: Very long documents may fail or produce partial content when created in one request. <br>
Mitigation: Create long documents in smaller sections and use append-style updates when appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenfa188/openclaw-feishu-create-doc) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API calls, JSON] <br>
**Output Format:** [JSON result after creating a Feishu document from Lark-flavored Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns document identifiers and a document URL; Feishu permissions determine valid creation targets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
