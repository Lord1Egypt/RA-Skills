## Description: <br>
Intelligent Task Planner analyzes natural-language requests, recognizes task intent, plans skill chains, and routes work across matching skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ethvs](https://clawhub.ai/user/ethvs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn broad natural-language requests into task plans, skill matches, execution steps, and deliverable guidance across writing, research, coding, data analysis, and planning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks to act as a global orchestrator and gatekeeper for all agent requests. <br>
Mitigation: Enable it only for workflows that explicitly need global orchestration, and keep normal agent routing available unless a human has approved exclusive control. <br>
Risk: The artifact describes system-prompt override, exclusive routing, intercept-all behavior, and enforced skill chains. <br>
Mitigation: Disable system-prompt override, exclusive mode, intercept-all routing, and enforced skill chains before deployment unless each control has been reviewed and approved. <br>
Risk: The default behavior includes auto-installing or invoking other skills. <br>
Mitigation: Require explicit user confirmation before installing or invoking downstream skills, and review those downstream skills separately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ethvs/intelligent-task-planner) <br>
- [Project homepage](https://github.com/ethvs/Intelligent-Task-Planner#readme) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, text, JSON-like task plans, code snippets, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose multi-step skill chains, quality checks, and downstream skill installation or invocation steps.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
