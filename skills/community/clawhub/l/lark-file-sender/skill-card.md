## Description: <br>
Sends documents, images, PDFs, archives, code files, and other local files to Feishu/Lark users or groups with guidance for path validation, target selection, and message formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timyljob2011-sudo](https://clawhub.ai/user/timyljob2011-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare Feishu/Lark message-tool calls for sending selected local files to users or group chats, including generated reports, documents, images, spreadsheets, archives, and code files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send local files to Feishu/Lark recipients, including sensitive reports, invoices, credentials, personal data, or batch-send outputs. <br>
Mitigation: Before each send, verify the exact file path, recipient user or chat, and message text; avoid sending sensitive files unless the user explicitly approves the destination and content. <br>
Risk: Generated command examples may include local code execution as part of preparing files for delivery. <br>
Mitigation: Treat generation-command examples as proposals and run local code only when the user explicitly requested that generation step. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/timyljob2011-sudo/lark-file-sender) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline message-tool command examples and optional Python helper output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should identify the file path, optional caption, and optional user or chat target before sending.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
