## Description: <br>
Helps an agent manage a Memos note system, including creating, listing, searching, updating, deleting, and organizing memos, attachments, comments, and reactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaomait](https://clawhub.ai/user/xiaomait) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to connect an agent to a self-hosted or hosted Memos instance for personal knowledge management, quick note capture, note search, and note organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to store and use a persistent Memos account token. <br>
Mitigation: Use a dedicated low-privilege or revocable token when available, keep config.json out of version control, and avoid pasting real tokens into chat. <br>
Risk: The skill can delete notes, bulk edit notes, upload files, change visibility, overwrite configuration, and create new access tokens. <br>
Mitigation: Require explicit user confirmation before destructive, bulk, upload, visibility, configuration, or token-creation actions. <br>


## Reference(s): <br>
- [Memos website](https://usememos.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON, JavaScript, HTTP, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include curl commands, config.json examples, API request payloads, memo summaries, tables, or raw JSON responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
