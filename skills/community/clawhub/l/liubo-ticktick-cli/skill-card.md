## Description: <br>
Ticktick Cli helps agents manage TickTick and dida365 tasks and projects through a command-line interface with OAuth2 authentication, task updates, batch operations, reminders, priorities, tags, due dates, project management, and file attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuboacean](https://clawhub.ai/user/liuboacean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent workflows use this skill to create, list, update, complete, abandon, and attach files to TickTick tasks from shell commands or JSON-oriented automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires TickTick OAuth credentials and may store TickTick tokens, client secrets, and session cookies locally. <br>
Mitigation: Install only if local credential storage is acceptable, restrict the credential file permissions, and avoid sharing credential file contents. <br>
Risk: Task-changing commands can complete, abandon, update, or batch-abandon TickTick tasks. <br>
Mitigation: Use exact task IDs for destructive or bulk actions and confirm the target project and task list before execution. <br>
Risk: Attachment commands upload local files to TickTick. <br>
Mitigation: Attach only files intentionally selected for upload and avoid files containing unrelated sensitive data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liuboacean/liubo-ticktick-cli) <br>
- [TickTick Developer Center](https://developer.ticktick.com/manage) <br>
- [TickTick Open API v1](https://developer.ticktick.com/api) <br>
- [dida365](https://dida365.com) <br>
- [GitHub: liuboacean/ticktick-cli](https://github.com/liuboacean/ticktick-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can read and write TickTick task data and may upload user-selected attachment files.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata; artifact pyproject.toml reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
