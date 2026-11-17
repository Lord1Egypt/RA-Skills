## Description:

Manage, orchestrate, inspect, and automate the Orca IDE and Multi-Agent Runtime Server for projects, worktrees, supervised workers, terminals, decision gates, accounts, and automations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafacpti23](https://clawhub.ai/user/rafacpti23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to manage Orca IDE runtime environments, inspect workspaces and services, coordinate multi-agent work, and configure Habilis MCP Gateway access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential exposure or mishandling during Habilis, GitHub, Stripe, OpenAI, Meta, or Orca setup.

Mitigation: Keep live tokens out of chat, store them in local environment or vault configuration, rotate any published admin password before use, and avoid copying root GitHub credentials into the Orca account.

Risk: High-impact operational commands can restart services, control terminals, or interrupt active agent work.

Mitigation: Run commands only in environments where service interruption and terminal command execution are acceptable, and review proposed actions before applying them.

Risk: Remote MCP or npx-based client connectors can expand execution and network exposure.

Mitigation: Pin and review connector packages and endpoint configuration before installation, and restrict Bearer tokens to the intended workspace or service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rafacpti23/skills/orca-control)
- [Publisher profile](https://clawhub.ai/user/rafacpti23)
- [Clawdis homepage](https://github.com/rafacpti23/orca-control-skill)
- [Orca Command Reference Cheatsheet](references/commands_cheatsheet.md)
- [Orca GitHub Integration & Preflight Diagnostics](references/github_integration_and_preflight.md)
- [Habilis SaaS & MCP Gateway Architecture Pattern](references/habilis_saas_mcp_gateway.md)
- [Thin-Skill Architecture & Multi-Client Distribution Pattern](references/thin_skill_distribution_pattern.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON/YAML configuration snippets, and operational checklists.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose service restarts, terminal control commands, environment checks, and MCP client configuration changes for user review.]

## Skill Version(s):

1.1.2 (source: ClawHub release metadata; artifact SKILL.md frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
