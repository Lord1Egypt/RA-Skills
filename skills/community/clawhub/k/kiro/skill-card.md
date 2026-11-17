## Description:

Kiro guides developers through agentic IDE and CLI workflows for spec-driven development, hooks automation, steering rules, MCP integrations, powers, and end-to-end project delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pupuking723](https://clawhub.ai/user/pupuking723)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and manage Kiro-based workflows, including specs, hooks, steering rules, MCP server configuration, and project-rule templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hooks examples can run shell commands or modify files when development events occur.

Mitigation: Review each hook before enabling it, keep save-time hooks fast, add error handling, and limit file changes to the intended project paths.

Risk: MCP examples may launch packages with credentials and filesystem access.

Mitigation: Pin package versions, avoid npx -y for credentialed servers, use least-privilege tokens, store secrets in environment variables, and restrict allowed filesystem paths.

Risk: The spec helper script creates files based on the provided spec name.

Mitigation: Use trusted spec names only and review generated requirements, design, and task files before using them in an automated workflow.

## Reference(s):

- [Kiro documentation](https://kiro.dev/docs/)
- [Kiro CLI guide](https://kiro.dev/docs/cli)
- [Kiro first project tutorial](https://kiro.dev/docs/getting-started/first-project/)
- [Kiro GitHub repository](https://github.com/kirodotdev/kiro)
- [Spec template reference](references/spec-template.md)
- [Hooks reference](references/hooks-reference.md)
- [MCP servers reference](references/mcp-servers.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell, JSON, YAML, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes templates for Kiro specs, steering rules, hooks, MCP configuration, and a helper script that creates spec files.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
