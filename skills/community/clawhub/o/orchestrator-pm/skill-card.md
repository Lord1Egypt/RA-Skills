## Description: <br>
Strategic project manager that reads between the lines, expands scope intelligently, creates job postings, and routes to spawner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dodge1218](https://clawhub.ai/user/dodge1218) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to classify incoming work, infer bounded follow-up tasks, build a dependency-aware job board, route work to specialist agents, and reconcile completion status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, archive, or delete workflow files as part of orchestration. <br>
Mitigation: Review the skill before installation and require explicit approval before file creation, archival, or deletion in sensitive workspaces. <br>
Risk: The skill can delegate work to sub-agents and interrupt agents that exceed timeouts. <br>
Mitigation: Use it only where delegated sub-agent work is acceptable, and require approval before spawning or killing active agents. <br>
Risk: The skill writes risk notes and insight logs that may influence later planning. <br>
Mitigation: Periodically review generated planning, risk, and insight files before relying on them for future routing decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dodge1218/orchestrator-pm) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Orchestrator Instructions](artifact/instructions.md) <br>
- [orchestrator.md](artifact/orchestrator.md) <br>
- [examples.template.json](artifact/examples.template.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown files and structured routing instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update workspace planning files, routing files, risk notes, and insight logs.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
