## Description: <br>
Manage Obsidian tasks via obsidian-cli. List, toggle, create, and update tasks from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boyd4y](https://clawhub.ai/user/boyd4y) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, note-takers, and Obsidian users use this skill to list, create, and update tasks in an Obsidian vault from an agent-assisted terminal workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task toggle, done, todo, and append actions can modify notes in the user's Obsidian vault. <br>
Mitigation: Ask for a preview or confirmation before executing write actions, especially on important notes or bulk task lists. <br>
Risk: The skill depends on the local obsidian CLI and an enabled Obsidian command line interface. <br>
Mitigation: Verify Obsidian 1.12+, Catalyst CLI access, and `obsidian version` before relying on task operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/boyd4y/obsidian-task) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that read or edit Obsidian vault tasks; write actions should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
