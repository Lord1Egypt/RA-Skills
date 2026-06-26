## Description: <br>
Node.js project architecture standards for AI-assisted development that enforce file splitting, config externalization, route modularization, and admin dashboard patterns for games, data tools, content platforms, dashboards, API services, and SDK libraries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abczsl520](https://clawhub.ai/user/abczsl520) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to structure or refactor Node.js projects so agents can work with smaller modules, externalized configuration, and project-type-specific layouts. It is intended for H5 games, data tools, dashboards, API services, content utilities, and SDK libraries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill promotes admin config editors and hot-reloadable config patterns that could expose or modify sensitive settings if applied broadly. <br>
Mitigation: Keep secrets out of config.json, expose only an explicit public allowlist through /api/config, and restrict any config-changing admin routes with strong authentication, authorization, validation, audit logging, CSRF protection where relevant, and restricted deployment. <br>
Risk: Generated project changes may include weakly scoped admin dashboard behavior or other incorrect architecture choices. <br>
Mitigation: Review generated code carefully before deployment and do not apply the admin dashboard pattern by default. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/abczsl520/nodejs-project-arch) <br>
- [H5 Game Architecture](references/game.md) <br>
- [Tool Architecture](references/tool.md) <br>
- [SDK Architecture](references/sdk.md) <br>
- [Admin Dashboard](docs/Admin-Dashboard.md) <br>
- [Config Pattern](docs/Config-Pattern.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript, JSON, project tree, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces architecture recommendations and implementation patterns for agent-assisted Node.js development.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
