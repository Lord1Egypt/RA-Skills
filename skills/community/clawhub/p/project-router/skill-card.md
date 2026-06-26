## Description: <br>
Terminal-first project bootstrapper and workspace context manager for detecting current projects, reading project context, running standardized targets, initializing .project bundles, managing artifacts, and exposing those actions through a CLI or MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SafaTinaztepe](https://clawhub.ai/user/SafaTinaztepe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use Project Router to bootstrap and manage local project context, standardized targets, artifacts, and task-focused workspace state. It is suited for agent-assisted project switching where the agent needs project briefs, target commands, and task context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run repository-defined shell commands from .project/targets.json. <br>
Mitigation: Install only for trusted workspaces and inspect .project/targets.json before running any target. <br>
Risk: The skill can apply file-writing plans. <br>
Mitigation: Inspect generated plan JSON before applying it. <br>
Risk: The MCP server may expose project actions for unfamiliar repositories. <br>
Mitigation: Avoid enabling the MCP server for unfamiliar repositories and verify that it invokes the reviewed project CLI. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/SafaTinaztepe/project-router) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with JSON configuration and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local .project bundle files when the plan/apply workflow is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
