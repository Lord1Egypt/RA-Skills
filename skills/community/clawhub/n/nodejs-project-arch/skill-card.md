## Description:

Node.js project architecture standards for AI-assisted development. Enforces file splitting (<400 lines), config externalization, route modularization, and admin dashboards. Use when creating new Node.js projects, refactoring large single-file codebases, or when AI context window is being consumed by oversized files. Covers H5 games (Canvas/Phaser/Matter.js), data tools (crawlers/scrapers), content platforms, monitoring dashboards, API services, and SDK libraries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abczsl520](https://clawhub.ai/user/abczsl520)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to structure or refactor Node.js projects into small modules, externalized runtime configuration, route/service layers, and admin dashboards. It applies to H5 games, data tools, content utilities, monitoring dashboards, API services, and SDK libraries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated admin/config patterns can expose secrets or allow unsafe changes to live application settings.

Mitigation: Keep secrets out of config.json, expose only allowlisted public configuration, and require proper authentication and authorization for admin routes.

Risk: Hot-reload config updates and restore actions can cause unintended production behavior.

Mitigation: Validate all config updates, audit admin changes, and make write or restore operations explicit and reversible.

Risk: Example admin dashboards and config handlers may be copied into production without hardening.

Mitigation: Review generated admin/config code before use and adapt it to the application's production security model.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abczsl520/skills/nodejs-project-arch)
- [H5 Game Architecture](references/game.md)
- [Non-Game Project Architecture](references/tool.md)
- [SDK/Library Architecture](references/sdk.md)
- [Config Pattern](docs/Config-Pattern.md)
- [Admin Dashboard](docs/Admin-Dashboard.md)
- [Token Savings Analysis](docs/Token-Savings.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline code blocks and project structure examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are architecture recommendations and implementation patterns for an agent to apply to Node.js projects.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
