## Description: <br>
Manage plashboard templates and autonomously convert natural-language dashboard requests into plashboard tool actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhytabest](https://clawhub.ai/user/jhytabest) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to administer Plashboard runtime templates, convert natural-language dashboard requests into tool actions, activate dashboards, trigger runs, and inspect runtime status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically create, activate, and run live dashboards from broad natural-language requests without a confirmation step. <br>
Mitigation: For production use, require explicit operator confirmation before activation, deletion, or run-now actions, and review the target dashboard or template before execution. <br>
Risk: The skill is intended to make live Plashboard changes through trusted tools. <br>
Mitigation: Install only where the Plashboard tools are trusted and available, and keep direct edits to dashboard, template, state, and run JSON files prohibited. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jhytabest/plashboard-admin) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, tool actions, shell commands, configuration] <br>
**Output Format:** [Markdown and agent tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May present exact operator commands when readiness or exposure issues are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
