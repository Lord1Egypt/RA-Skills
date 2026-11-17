## Description:

Install and configure the LLM-WikiMind MCP server, a local knowledge base built on Karpathy's LLM Wiki pattern.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hal-9909](https://clawhub.ai/user/hal-9909)

### License/Terms of Use:

MIT

## Use Case:

Developers and MCP users use this skill to install a local Markdown-backed knowledge base, register its MCP server with compatible AI clients, and keep the wiki search index synchronized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable remote code from a Git repository.

Mitigation: Review the WikiMind repository and package sources first, and prefer pinned versions or a reviewed commit before installation.

Risk: The setup can add a background watcher that starts quietly on login.

Mitigation: Run setup in a restricted environment, choose a narrow knowledge-base directory, and avoid adding the auto-start line unless you understand how to remove and monitor it.

## Reference(s):

- [LLM-WikiMind GitHub repository](https://github.com/HAL-9909/llm-wikimind)
- [Karpathy LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [ClawHub skill page](https://clawhub.ai/hal-9909/skills/llm-wikimind-mcp)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides setup steps, MCP client registration snippets, verification commands, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
