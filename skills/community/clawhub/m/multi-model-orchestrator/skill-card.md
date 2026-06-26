## Description: <br>
Multi Model Orchestrator coordinates multi-model agent workflows for requirement clarification, planning, parallel execution, persistent task completion, debugging, frontend work, code review, and autopilot loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lpq6](https://clawhub.ai/user/lpq6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to route coding work across planning, implementation, review, debugging, and frontend workflows. It is most useful when a task benefits from explicit model roles, parallel execution, or persistent completion with review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad orchestration can start parallel or persistent agent workflows with limited user control. <br>
Mitigation: Use explicit commands for $team, $ralph, and $autopilot, and confirm before allowing parallel or persistent execution. <br>
Risk: Model routing and dependency installation behavior may expose sensitive project context or alter a workspace unexpectedly. <br>
Mitigation: Review model routing and approve dependency changes before use on private code or sensitive projects. <br>
Risk: Under-scoped triggers may select a larger orchestration workflow than the user intended. <br>
Mitigation: Prefer narrow prompts and explicit workflow names so the agent chooses the intended level of automation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lpq6/multi-model-orchestrator) <br>
- [oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex) <br>
- [superpowers-systematic-debugging](https://github.com/wcygan/dotfiles/tree/main/config/claude/skills/superpowers-systematic-debugging) <br>
- [frontend-design](https://github.com/iuliandita/skills/tree/main/skills/frontend-design) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with task templates, review reports, implementation plans, code snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May coordinate multiple model-specific agents and parallel sessions when the user invokes team or autopilot workflows.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
