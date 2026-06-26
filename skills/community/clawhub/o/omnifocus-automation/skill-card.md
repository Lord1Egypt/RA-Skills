## Description: <br>
Manage OmniFocus tasks, projects, and folders via Omni Automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Coyote-git](https://clawhub.ai/user/Coyote-git) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent read, create, update, organize, and complete OmniFocus tasks, projects, folders, tags, due dates, and recurring task settings on macOS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify local OmniFocus tasks, including notes that may contain sensitive information. <br>
Mitigation: Install it only when local OmniFocus automation is intended, grant macOS Automation access deliberately, and avoid storing secrets in task notes. <br>
Risk: Task mutations such as delete, move, note replacement, due date changes, and completion changes can alter personal task data. <br>
Mitigation: Ask the agent to show the target task details before important mutations, especially permanent delete or note replacement. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Coyote-git/omnifocus-automation) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands that return JSON from OmniFocus automation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS with OmniFocus installed and macOS Automation permission granted deliberately.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
