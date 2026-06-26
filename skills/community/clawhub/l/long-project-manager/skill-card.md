## Description: <br>
Create and maintain a persistent file-based workspace for long-running, multi-session, or interruption-sensitive work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TianxiangMa](https://clawhub.ai/user/TianxiangMa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, writers, planners, and operations teams use this skill to keep durable project state for work that spans multiple sessions. It helps agents create and update project notes, task lists, decisions, logs, references, and handoff files so work can resume after interruptions or context loss. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill deliberately writes durable project notes to disk, which may preserve sensitive project, personal, or business context across sessions. <br>
Mitigation: Choose the project location deliberately, review STATUS.md and HANDOFF.md before relying on them, and avoid recording secrets or sensitive personal information unless future sessions should read it. <br>
Risk: Outdated or vague project notes can cause later sessions to resume from incorrect assumptions. <br>
Mitigation: Refresh STATUS.md and HANDOFF.md before pausing, and make the next action and first files to read explicit. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TianxiangMa/long-project-manager) <br>
- [Packaged README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown project files and concise chat guidance, with occasional shell commands for creating or copying workspace templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates durable local project files such as README.md, STATUS.md, TODO.md, DECISIONS.md, LOG.md, REFERENCES.md, and HANDOFF.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
