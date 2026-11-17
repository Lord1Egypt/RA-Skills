## Description:

Model Routing Tool Pro helps teams govern model routing with cost dashboards, batch dispatch, custom routing rules, multi-provider failover, monitoring alerts, and policy controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation teams, and technical leads use this skill to plan and document team-level model routing policies, budget alerts, batch task routing, provider failover, and audit-oriented configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad read, write, and command execution authority can affect workspace files or execute unintended commands.

Mitigation: Use the skill only in workspaces where those actions are acceptable, and require explicit confirmation before exports, configuration changes, provider switching, alerts, or shell commands.

Risk: Provider API keys and webhook credentials may be needed for routing, monitoring, and notification workflows.

Mitigation: Store credentials in environment variables or a secret manager, and avoid placing secrets in configuration files, generated reports, or prompts.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/model-routing-tool-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON, YAML, JavaScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include routing policy examples, cost-report structures, operational checklists, and command suggestions for agent execution.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
