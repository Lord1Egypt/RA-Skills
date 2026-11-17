## Description:

Guides agents through Kiro workflows for spec-driven development, hooks automation, steering rules, MCP integration, powers extensions, and end-to-end development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xwz119](https://clawhub.ai/user/xwz119)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide Kiro project work with specs, hooks, steering rules, MCP servers, and optional automation scripts from prototype through production workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent Kiro hook examples can run shell commands that delete files, deploy, make network requests, or execute on a schedule.

Mitigation: Review every hook before use, keep automatic actions narrow, and avoid enabling destructive, deployment, network, or scheduled hooks without explicit project approval.

Risk: MCP examples involve credentials, filesystem access, and third-party tools with weak default safety boundaries.

Mitigation: Pin packages, use least-privilege tokens, narrow filesystem paths, store secrets in environment variables, and enable only required MCP servers.

Risk: Shell-expanded file placeholders in hook examples can behave unexpectedly when paths contain unsafe characters.

Mitigation: Quote placeholders carefully or avoid shell-expanded placeholders in real project hooks.

## Reference(s):

- [Kiro documentation](https://kiro.dev/docs/)
- [Kiro CLI guide](https://kiro.dev/docs/cli)
- [Kiro first project tutorial](https://kiro.dev/docs/getting-started/first-project/)
- [Kiro GitHub repository](https://github.com/kirodotdev/kiro)
- [Kiro spec template](references/spec-template.md)
- [Kiro hooks reference](references/hooks-reference.md)
- [Kiro MCP servers reference](references/mcp-servers.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell, YAML, JSON, Python, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reusable Kiro steering, hook, MCP, and spec templates plus a Python spec scaffold script.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
