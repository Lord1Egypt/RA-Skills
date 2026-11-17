## Description:

AI agent orchestrator with Neo4j knowledge graph, Meilisearch search, and Tree-sitter parsing. Use for coordinating multiple coding agents on complex projects with shared context and plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reversteam](https://clawhub.ai/user/reversteam)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use Project Orchestrator to coordinate multiple AI coding agents on complex codebases by sharing project plans, task context, decisions, and searchable code knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Powerful agent execution, code indexing, chat history, and database controls are exposed without adequate access controls.

Mitigation: Use only in an isolated, trusted local environment unless authentication and per-user authorization are added.

Risk: Default Neo4j and Meilisearch credentials can expose project data or administrative controls.

Mitigation: Replace default credentials and bind services to loopback or a restricted private network before use.

Risk: Sync/watch and chat working-directory behavior can expose more workspace content than intended.

Mitigation: Restrict sync/watch and chat cwd to explicit workspaces and disable symlink escapes.

Risk: Permission-bypass agent execution can allow unintended tool actions.

Mitigation: Remove permission-bypass execution or require explicit review before enabling the chat execution path.

Risk: A git dependency is not pinned to a reviewed revision.

Mitigation: Pin the git dependency to a specific reviewed commit and review dependency updates before release.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/reversteam/skills/project-orchestrator)
- [README](README.md)
- [Installation Guide](docs/setup/installation.md)
- [Getting Started Tutorial](docs/guides/getting-started.md)
- [API Reference](docs/api/reference.md)
- [MCP Tools Reference](docs/api/mcp-tools.md)
- [Multi-Agent Workflow Guide](docs/guides/multi-agent-workflow.md)
- [Workspaces Guide](docs/guides/workspaces.md)
- [OpenAI Integration Guide](docs/integrations/openai.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, shell commands, configuration snippets, and code-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing project context, plans, prompts, decisions, code search results, and setup instructions.]

## Skill Version(s):

0.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
