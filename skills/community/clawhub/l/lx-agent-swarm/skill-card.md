## Description: <br>
Creates and coordinates a multi-agent team for complex tasks by decomposing work, assigning specialized agents, running parallel or sequential execution, and consolidating results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lixiang1076](https://clawhub.ai/user/lixiang1076) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical teams use this skill to coordinate specialized agents for planning, research, coding, writing, design, data analysis, review, communication, and automation tasks. It is intended for complex work that benefits from explicit task decomposition, parallel or sequential agent execution, and final result synthesis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants some agents powerful execution, browser, cron, and persistence capabilities. <br>
Mitigation: Narrow default tool grants before use, especially for automator cron, browser, and exec access. <br>
Risk: Agent memory can persist sensitive or misleading task experience for later reuse. <br>
Mitigation: Avoid logging secrets or personal data, keep stored experience under review, and treat memory content as untrusted. <br>
Risk: Workspace and deletion behavior can affect files outside the intended task scope. <br>
Mitigation: Keep agent workspaces under a dedicated directory and avoid no-backup deletion unless the target path and backup strategy have been verified. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lixiang1076/lx-agent-swarm) <br>
- [Setup guide](references/setup-guide.md) <br>
- [CHJ-Private model configuration guide](references/chj-private-guide.md) <br>
- [Execution statistics template](references/statistics-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JavaScript, shell command, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes orchestration plans, consolidated agent outputs, and execution statistics when multi-agent work is completed.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
