## Description: <br>
Provides integration patterns for using Mapbox MCP Server in AI applications and agent frameworks, including pydantic-ai, Mastra, LangChain, CrewAI, smolagents, and custom agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mapbox](https://clawhub.ai/user/mapbox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate Mapbox MCP Server into AI agents that need routing, geocoding, point-of-interest search, geometry operations, and production geospatial patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Precise coordinates, addresses, home or work locations, commute searches, and route queries may be sent to Mapbox services and possibly an LLM provider. <br>
Mitigation: Treat location data as sensitive, disclose third-party processing to users, avoid unnecessary retention, and avoid logging prompts or responses that contain exact locations. <br>
Risk: Mapbox access tokens and authorization headers can grant unintended service access if exposed or over-scoped. <br>
Mitigation: Use scoped Mapbox tokens, store tokens in environment variables or secret managers, avoid hardcoded credentials, and prevent Authorization headers from appearing in logs. <br>
Risk: Hosted Mapbox API tools can incur costs or be mistaken for offline no-cost tools. <br>
Mitigation: Prefer offline tools when real-time data or routing is not needed, and clearly distinguish API-backed tools that require a token and count against usage. <br>
Risk: Broad agent base tools can expand the runtime surface beyond the geospatial tasks the skill is meant to support. <br>
Mitigation: Disable broad agent base tools unless they are required, and expose only the Mapbox tools needed for the application workflow. <br>


## Reference(s): <br>
- [Mapbox MCP Server](https://github.com/mapbox/mcp-server) <br>
- [Model Context Protocol](https://modelcontextprotocol.io) <br>
- [Mapbox API Documentation](https://docs.mapbox.com/api/) <br>
- [Pydantic AI Integration](references/pydantic-ai.md) <br>
- [CrewAI Integration](references/crewai.md) <br>
- [Smolagents Integration](references/smolagents.md) <br>
- [Mastra Integration](references/mastra.md) <br>
- [LangChain Integration](references/langchain.md) <br>
- [Custom Agent Integration](references/custom-agent.md) <br>
- [Use Cases](references/use-cases.md) <br>
- [Production Patterns](references/production.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code examples, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Python and TypeScript examples for multiple agent frameworks.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
