## Description: <br>
Builds OpenClaw projects: coordinated multi-agent team setups for shared work across software, marketing, real estate, content, sales, operations, research, customer success, and similar team workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[encryptshawn](https://clawhub.ai/user/encryptshawn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to interview for, review, and set up OpenClaw multi-agent project teams with task-manager coordination, shared project files, message queues, and agent workspace references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent project files and OpenClaw configuration changes can route work between agents incorrectly if the setup plan is wrong. <br>
Mitigation: Review the generated team plan, participating agents, task-manager project, repository URLs, and dependency skills before approving setup. <br>
Risk: Shared project files, queue files, and memory documents can expose project context or secret names if users put sensitive material in them. <br>
Mitigation: Keep actual secrets out of project files, queue files, and shared memory; store secret values in the user's secret management system and pass only environment variable names. <br>
Risk: Task-manager access depends on separately installed Asana or ClickUp skills and their credentials. <br>
Mitigation: Verify the task-manager dependency skill is installed and authenticated on each participating agent before running the project smoke test. <br>


## Reference(s): <br>
- [OpenClaw Projects skill definition](artifact/SKILL.md) <br>
- [Project Files Reference](artifact/references/project-files.md) <br>
- [Workflow Reference](artifact/references/workflow.md) <br>
- [Interview Question Banks](artifact/references/interview-questions.md) <br>
- [Team Archetypes](artifact/references/team-archetypes.md) <br>
- [Templates](artifact/references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance plus generated OpenClaw project files and configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates persistent project coordination files only after a user-reviewed plan and smoke test.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
