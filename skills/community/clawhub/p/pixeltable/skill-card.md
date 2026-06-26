## Description: <br>
Build multimodal AI applications with Pixeltable using declarative tables, computed columns, embedding indexes, retrieval, tool-calling agents, and AI provider integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pierrebrunelle](https://clawhub.ai/user/pierrebrunelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build RAG pipelines, multimodal data workflows, AI provider integrations, FastAPI serving patterns, and tool-calling agents backed by Pixeltable tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider integrations may require sensitive credentials and may send data to third-party services. <br>
Mitigation: Use approved providers, store API keys in environment variables or a secret manager, and review vendor terms and retention before using private or regulated data. <br>
Risk: Tool-calling, MCP, deletion, and network examples can trigger writes, deletes, external calls, or cost-incurring actions. <br>
Mitigation: Use only trusted MCP servers and require human approval for tools that can write, delete, spend money, or make network calls. <br>
Risk: Serving and persistent-memory examples can expose user data or retain sensitive information if deployed without controls. <br>
Mitigation: Add authentication, audit logs, backups, and retention/deletion policies before deploying serving or memory workflows. <br>


## Reference(s): <br>
- [Pixeltable documentation](https://docs.pixeltable.com/) <br>
- [Pixeltable support discussions](https://github.com/pixeltable/pixeltable/discussions) <br>
- [Pixeltable GitHub repository](https://github.com/pixeltable/pixeltable) <br>
- [Pixeltable Starter Kit](https://github.com/pixeltable/pixeltable-starter-kit) <br>
- [Pixeltable project generator](https://github.com/pixeltable/pixeltable-new) <br>
- [Pixeltable developer MCP server](https://github.com/pixeltable/mcp-server-pixeltable-developer) <br>
- [Pixeltable llms-full.txt](https://docs.pixeltable.com/llms-full.txt) <br>
- [Pixeltable llms.txt](https://www.pixeltable.com/llms.txt) <br>
- [Core API reference](references/core-api.md) <br>
- [Provider reference](references/providers.md) <br>
- [Workflow templates](references/workflows.md) <br>
- [Agent with memory and MCP tools](references/agents-memory-mcp.md) <br>
- [Video RAG agent](references/video-rag-agents.md) <br>
- [ML data wrangling pipeline](references/ml-data-pipeline.md) <br>
- [Agentic patterns](references/agentic-patterns.md) <br>
- [Anti-patterns](references/anti-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include provider setup, API-serving patterns, data-pipeline recipes, and review guidance for credentials, tools, and data handling.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
