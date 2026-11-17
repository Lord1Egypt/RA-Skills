## Description:

Multi Model Orchestrator coordinates multi-agent workflows for requirement clarification, planning, parallel execution, persistent implementation, debugging, frontend work, code review, and autopilot loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lpq6](https://clawhub.ai/user/lpq6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to route complex coding, debugging, frontend, planning, and review work across specialized agent workflows. It helps structure tasks into interviews, plans, delegated execution, reviews, and follow-up fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can route broad phrases into autonomous, parallel, or autopilot workflows.

Mitigation: Review selected workflow mode and task scope before execution, especially for broad or ambiguous prompts.

Risk: The skill documentation includes dependency installation as an automatic repair path.

Mitigation: Require explicit approval before any package-manager command, dependency installation, or environment change.

Risk: Parallel and delegated workflows may make changes across a project without enough scoping.

Mitigation: Use the skill only in a sandboxed project environment and verify proposed file changes before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lpq6/skills/multi-model-orchestrator)
- [oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex)
- [superpowers-systematic-debugging](https://github.com/wcygan/dotfiles/tree/main/config/claude/skills/superpowers-systematic-debugging)
- [frontend-design](https://github.com/iuliandita/skills/tree/main/skills/frontend-design)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured task plans, review reports, command snippets, configuration guidance, and code-oriented deliverables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger autonomous, parallel, or autopilot workflows depending on user phrasing and agent environment.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
