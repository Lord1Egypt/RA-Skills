## Description: <br>
MindsDB MCP Skill helps an agent use natural language to query, analyze, and operate MindsDB-connected data sources, including SQL databases, files, SaaS systems, AI models, and RAG knowledge bases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yejinlei](https://clawhub.ai/user/yejinlei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to work with MindsDB through an agent: connecting data sources, generating and executing SQL, creating prediction models, building knowledge bases, and producing data analysis reports from natural language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through broad database and enterprise-data operations. <br>
Mitigation: Use dedicated least-privilege or read-only accounts where possible, and scope access to only the data sources needed for the task. <br>
Risk: Generated SQL or workflow steps could perform writes, deletes, schema changes, imports, exports, model training, or knowledge-base ingestion. <br>
Mitigation: Review generated SQL and require explicit confirmation before any mutating, training, ingestion, scheduled reporting, or regulated-data workflow. <br>
Risk: Credentials or API keys may be exposed if they are placed in prompts, URLs, or shared configuration. <br>
Mitigation: Keep credentials out of prompts and URLs, prefer environment variables or secret stores, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [MindsDB Official Documentation](https://docs.mindsdb.com) <br>
- [Model Context Protocol](https://modelcontextprotocol.io) <br>
- [MindsDB MCP Tools Reference](references/mindsdb-tools.md) <br>
- [MindsDB Data Source Configuration Reference](references/data-sources.md) <br>
- [MindsDB SQL Query Examples](references/sql-examples.md) <br>
- [MindsDB Knowledge Base (KD/RAG) Guide](references/knowledge-base.md) <br>
- [MindsDB SDK and API Reference](references/sdk-api.md) <br>
- [MindsDB MLOps and Advanced Features Guide](references/mlops-advanced.md) <br>
- [MindsDB Streaming and Data Pipelines Guide](references/streaming-pipelines.md) <br>
- [MindsDB Intelligent Analysis Guide](references/intelligent-analysis.md) <br>
- [Industrial Monitoring Case Study](references/industrial-monitoring-case.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with SQL, JSON, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated SQL, data analysis summaries, model setup steps, database connection guidance, and troubleshooting recommendations.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
