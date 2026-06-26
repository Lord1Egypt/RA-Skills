## Description: <br>
Provides an always-on agency workflow for agents, with startup calibration, self-checks, recovery steps, and persistent learning prompts for complex tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yu-xiao-sheng](https://clawhub.ai/user/yu-xiao-sheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can apply this skill to push an agent toward end-to-end ownership, stronger verification habits, persistent troubleshooting, and cross-session learning during complex work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill broadly changes agent behavior across tasks and may encourage an aggressive always-on workflow. <br>
Mitigation: Install only when that productivity posture is intentional, and keep user approval requirements for broad task expansion or sensitive work. <br>
Risk: The skill uses persistent memory files without enough built-in user control. <br>
Mitigation: Require approval before creating or updating builder-journal.md or HANDOFF.md, especially in private repositories or sensitive workspaces. <br>
Risk: The skill may encourage broad file inspections or commands beyond the immediate task scope. <br>
Mitigation: Limit automatic memory reads and writes, and require approval before broad file inspection or command execution outside the current task scope. <br>


## Reference(s): <br>
- [High Agency on ClawHub](https://clawhub.ai/yu-xiao-sheng/high-agency) <br>
- [OpenPUA](https://openpua.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with checklists, structured prompts, and occasional inline command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide the agent to read or write local memory files such as builder-journal.md or HANDOFF.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
