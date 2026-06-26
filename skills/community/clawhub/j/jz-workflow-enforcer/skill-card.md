## Description: <br>
Agent Workflow Enforcer helps agents follow strict task checklists, output formats, and style-context continuity rules before starting or completing work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jzOcb](https://clawhub.ai/user/jzOcb) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to make AI task workflows more consistent by requiring gate checks, checklist-style responses, and persistent style context for multi-step work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make an agent refuse to proceed until checklist or gate requirements are satisfied. <br>
Mitigation: Install it only in projects where strict workflow enforcement is desired, and keep the requirements project-scoped rather than global when possible. <br>
Risk: User-supplied command arguments for gate checks could be mishandled if copied into shell commands without care. <br>
Mitigation: Quote command arguments and review any project-specific gate configuration before running it. <br>
Risk: Learned corrections or style-context files can steer future outputs in unintended ways. <br>
Mitigation: Review learned rules and persisted style context before saving or reusing them. <br>


## Reference(s): <br>
- [Agent Workflow Enforcer on ClawHub](https://clawhub.ai/jzOcb/jz-workflow-enforcer) <br>
- [Publisher Profile](https://clawhub.ai/user/jzOcb) <br>
- [Project Homepage](https://github.com/example/agent-workflow-enforcer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with checklist blocks and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can prompt agents to run a local gate script and to include required checklist sections before proceeding.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
