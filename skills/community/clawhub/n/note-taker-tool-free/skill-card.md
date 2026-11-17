## Description: <br>
笔记记录器基础版 helps an agent manage local notes and to-do tasks through command-line style actions such as add, list, complete, prioritize, remind, view, and export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and lightweight workflow users use this skill to ask an agent to add, list, prioritize, complete, remind, view, and export personal notes or tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task or note content may contain sensitive information, and the security review notes local-only privacy claims alongside callback, API, and network paths. <br>
Mitigation: Review before installation, use only with explicit note or task requests, avoid callback URLs or external API settings unless acceptable, and choose export paths carefully. <br>
Risk: Create, update, delete, reminder, and export actions can change or expose local task data. <br>
Mitigation: Confirm before create, update, delete, reminder, or export actions and keep backups of local note data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/note-taker-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON or text task results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local task data, execution logs, reminders, and export guidance depending on the user request.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
