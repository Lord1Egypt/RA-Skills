## Description:

MindsDB MCP Skill helps agents use natural language to query databases, connect data sources, run SQL, create AI models, build RAG knowledge bases, and analyze data through a MindsDB MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yejinlei](https://clawhub.ai/user/yejinlei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and operations teams use this skill to let an agent interact with approved MindsDB-backed data sources, generate SQL, analyze data, create predictive models, and build knowledge-base workflows from natural-language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad database and model-operation authority across connected data sources.

Mitigation: Use only approved data sources, default to read-only or least-privilege credentials, and add confirmation and audit controls before use with production systems.

Risk: Generated SQL or workflow guidance can perform state-changing operations such as CREATE, INSERT, UPDATE, DELETE, DROP, imports, exports, SaaS connections, RAG ingestion, scheduled jobs, or production model deployment.

Mitigation: Require explicit user approval before executing mutating operations, data movement, external service connections, ingestion, scheduling, or deployment actions.

Risk: API keys or database credentials may be exposed if placed directly in URLs, prompts, or shared configuration snippets.

Mitigation: Store secrets in approved credential stores or environment variables and avoid putting real keys in prompts, URLs, examples, logs, or generated output.

Risk: Unpinned dependencies can change behavior or security posture after installation.

Mitigation: Pin dependency versions and review updates before deploying the skill in controlled environments.

## Reference(s):

- [MindsDB documentation](https://docs.mindsdb.com)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MindsDB MCP server issues](https://github.com/mindsdb/mcp-server/issues)
- [MindsDB MCP tools reference](references/mindsdb-tools.md)
- [MindsDB data source configuration reference](references/data-sources.md)
- [MindsDB SQL query examples](references/sql-examples.md)
- [MindsDB SDK and API reference](references/sdk-api.md)
- [MindsDB knowledge base and RAG guide](references/knowledge-base.md)
- [MindsDB MLOps and advanced features guide](references/mlops-advanced.md)
- [MindsDB streaming and pipeline guide](references/streaming-pipelines.md)
- [MindsDB intelligent analysis guide](references/intelligent-analysis.md)
- [Industrial monitoring case study](references/industrial-monitoring-case.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with SQL, JSON, Python, JavaScript, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include database queries, configuration snippets, analysis summaries, and operational recommendations.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
