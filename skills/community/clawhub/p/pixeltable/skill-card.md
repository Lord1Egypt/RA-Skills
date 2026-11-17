## Description:

Build multimodal AI applications with Pixeltable using declarative tables for chunking, embeddings, retrieval, tool-calling agents, provider integrations, computed columns, version control, similarity search, FastAPI serving, and production patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pierrebrunelle](https://clawhub.ai/user/pierrebrunelle)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and engineers use this skill to build Pixeltable-based multimodal RAG, media processing, AI provider integration, and tool-calling agent workflows. It guides agents toward declarative Pixeltable tables, computed columns, embedding indexes, persistent memory patterns, and serving or batch pipeline designs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated examples can expose unauthenticated data endpoints.

Mitigation: Add authentication and authorization before exposing generated APIs, and review route behavior before deployment.

Risk: Persistent memory examples can allow LLM-written data to affect later interactions.

Mitigation: Bind memory writes to server-side identity, scope memory by user or tenant, and review stored facts before relying on them.

Risk: Destructive cleanup examples can remove local Pixeltable state.

Mitigation: Run cleanup only in restricted development environments and back up Pixeltable state before destructive operations.

Risk: Generated code or scaffolding may include dependencies or behavior unsuitable for the target environment.

Mitigation: Review generated code before execution, pin package versions where possible, and test scaffolds in a restricted environment.

## Reference(s):

- [Pixeltable documentation](https://docs.pixeltable.com/)
- [Pixeltable support discussions](https://github.com/pixeltable/pixeltable/discussions)
- [Pixeltable GitHub repository](https://github.com/pixeltable/pixeltable)
- [Pixeltable starter kit](https://github.com/pixeltable/pixeltable-starter-kit)
- [pixeltable-new scaffolding tool](https://github.com/pixeltable/pixeltable-new)
- [Pixeltable developer MCP server](https://github.com/pixeltable/mcp-server-pixeltable-developer)
- [Pixeltable LLM documentation](https://docs.pixeltable.com/llms-full.txt)
- [Pixeltable Core API Reference](references/core-api.md)
- [Pixeltable End-to-End Workflow Templates](references/workflows.md)
- [Pixeltable AI Provider Reference](references/providers.md)
- [Anti-Patterns: Training-Distribution Biases LLMs Bring to Pixeltable](references/anti-patterns.md)
- [Agent with Memory and MCP Tools](references/agents-memory-mcp.md)
- [Agentic Patterns](references/agentic-patterns.md)
- [ML Data Wrangling Pipeline](references/ml-data-pipeline.md)
- [Video RAG Agent](references/video-rag-agents.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with code snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Pixeltable project scaffolds, table schemas, computed columns, provider calls, API route patterns, and data pipeline guidance.]

## Skill Version(s):

2.3.0 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
