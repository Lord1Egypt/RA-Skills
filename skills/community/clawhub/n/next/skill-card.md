## Description: <br>
Suggests next actions after task completion and can auto-trigger through a Stop hook when completion keywords are detected. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use Next to choose follow-up work after an agent finishes a task, including verification, commit, PR, CI, or session wrap-up actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently auto-trigger after ordinary completions and interrupt otherwise quiet sessions. <br>
Mitigation: Review the Stop hook registration before installation and disable it when manual follow-up control is preferred. <br>
Risk: Follow-up options may lead to repository, PR, CI, or reviewer actions with business impact. <br>
Mitigation: Require explicit user selection before executing external actions and review suggested actions before proceeding. <br>
Risk: The workflow may inspect recent conversation and GitHub workflow state to suggest next actions. <br>
Mitigation: Use it only in workspaces where that context access is acceptable and appropriate for the repository. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drumrobot/next) <br>
- [Ask Gates](ask-gates.md) <br>
- [Stall Detection](stall-detect.md) <br>
- [Suggestion Patterns](suggestion-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Shell commands, Configuration] <br>
**Output Format:** [Markdown text with structured next-action options and inline shell commands when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can be invoked manually or by a Stop hook that reacts to task-completion signals.] <br>

## Skill Version(s): <br>
0.4.2 (source: ClawHub release metadata and CHANGELOG, released 2026-06-19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
