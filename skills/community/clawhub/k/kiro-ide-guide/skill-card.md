## Description: <br>
Guides agents through Kiro IDE workflows for spec-driven development, hooks automation, steering rules, MCP server setup, powers extensions, and end-to-end development planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xwz119](https://clawhub.ai/user/xwz119) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to apply Kiro-style spec-driven development, configure hooks and steering rules, connect MCP servers, and scaffold standard spec documents for implementation planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hook examples may run commands for formatting, tests, deployment, deletion, notifications, or scheduled jobs. <br>
Mitigation: Review each hook before use, keep save-time hooks fast and local, and avoid deploying, deleting, or posting messages unless the project owner explicitly approves the action. <br>
Risk: MCP server examples can expose credentials or filesystem access if configured too broadly. <br>
Mitigation: Store credentials in environment variables, use least-privilege tokens, enable only required servers, and restrict filesystem allowed paths to the intended project. <br>
Risk: Generated spec scaffolds are templates and can contain assumptions that do not match a specific project. <br>
Mitigation: Review and adapt generated requirements, design, and task files before allowing an agent to implement from them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xwz119/kiro-ide-guide) <br>
- [Kiro documentation](https://kiro.dev/docs/) <br>
- [Kiro CLI guide](https://kiro.dev/docs/cli) <br>
- [Kiro first project tutorial](https://kiro.dev/docs/getting-started/first-project/) <br>
- [Kiro GitHub repository](https://github.com/kirodotdev/kiro) <br>
- [Spec template](references/spec-template.md) <br>
- [Hooks reference](references/hooks-reference.md) <br>
- [MCP servers reference](references/mcp-servers.md) <br>
- [Project rules steering template](assets/steering-templates/project-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell command, YAML, JSON, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can also produce scaffolded requirements, design, and task markdown files through the bundled create-spec.py script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
