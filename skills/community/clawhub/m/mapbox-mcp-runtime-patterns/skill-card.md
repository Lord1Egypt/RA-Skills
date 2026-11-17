## Description:

Integration patterns for Mapbox MCP Server in AI applications and agent frameworks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mapbox](https://clawhub.ai/user/mapbox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate Mapbox MCP Server into AI applications that need geospatial capabilities, including pydantic-ai, Mastra, LangChain, CrewAI, smolagents, and custom agent runtimes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples and hosted MCP use can send coordinates, route requests, and search queries to Mapbox.

Mitigation: Disclose external Mapbox processing to users, avoid sending sensitive location data unless required, and use narrowly scoped Mapbox tokens.

Risk: Example setup uses unpinned package execution or broad dependency ranges.

Mitigation: Pin @mapbox/mcp-server and Python dependencies before production use, and run examples in an isolated environment.

Risk: Offline wording may obscure that hosted MCP examples still contact Mapbox infrastructure.

Mitigation: Review tool selection and deployment mode so offline-only requirements use local deterministic tools without unnecessary hosted calls.

## Reference(s):

- [Mapbox MCP Server](https://github.com/mapbox/mcp-server)
- [Mapbox API Documentation](https://docs.mapbox.com/api/)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [Pydantic AI](https://ai.pydantic.dev/)
- [Mastra](https://mastra.ai/)
- [LangChain](https://docs.langchain.com/oss/javascript/langchain/overview/)
- [CrewAI](https://docs.crewai.com/)
- [Smolagents](https://huggingface.co/docs/smolagents)
- [Pydantic AI Integration](references/pydantic-ai.md)
- [CrewAI Integration](references/crewai.md)
- [Smolagents Integration](references/smolagents.md)
- [Mastra Integration](references/mastra.md)
- [LangChain Integration](references/langchain.md)
- [Custom Agent Integration](references/custom-agent.md)
- [Use Cases](references/use-cases.md)
- [Production Patterns](references/production.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes framework-specific integration patterns and production guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
