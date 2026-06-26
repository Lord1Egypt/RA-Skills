## Description: <br>
Kiro workflow guidance for agentic IDE and CLI development, covering spec-driven development, hooks automation, steering rules, MCP server integration, and powers extensions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pupuking723](https://clawhub.ai/user/pupuking723) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and operate Kiro workflows, including specs, hooks, steering rules, MCP configuration, and reusable project templates. It helps agents produce practical setup guidance, configuration examples, shell commands, and starter files for Kiro-based development. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MCP examples can grant local file or external service access if copied with broad paths or overly privileged tokens. <br>
Mitigation: Restrict MCP allowedPaths, use project-specific least-privilege tokens, and enable only the servers needed for the current task. <br>
Risk: Hook examples can run shell commands, delete files, trigger deploys, or send external webhooks when configured by a user. <br>
Mitigation: Review hook patterns and actions before enabling them, protect production deploy hooks with approvals, and avoid destructive or outbound webhook hooks unless paths, payloads, and secrets are validated. <br>
Risk: Workflow templates and examples may be copied into projects without matching local requirements. <br>
Mitigation: Review generated specs, steering rules, and configuration examples before applying them to production repositories. <br>


## Reference(s): <br>
- [Kiro Documentation](https://kiro.dev/docs/) <br>
- [Kiro CLI Guide](https://kiro.dev/docs/cli) <br>
- [Kiro First Project Tutorial](https://kiro.dev/docs/getting-started/first-project/) <br>
- [Kiro GitHub Repository](https://github.com/kirodotdev/kiro) <br>
- [Kiro Spec Template](references/spec-template.md) <br>
- [Kiro Hooks Configuration Reference](references/hooks-reference.md) <br>
- [Kiro MCP Server Reference](references/mcp-servers.md) <br>
- [Project Rules Steering Template](assets/steering-templates/project-rules.md) <br>
- [ClawHub Kiro Release](https://clawhub.ai/pupuking723/kiro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell command, YAML, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Kiro spec template files when the bundled helper script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
