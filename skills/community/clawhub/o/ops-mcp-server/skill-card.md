## Description: <br>
Query observability data and execute operational procedures via the ops-mcp-server MCP interface, covering Kubernetes events, Prometheus metrics, Elasticsearch logs, Jaeger distributed traces, and SOPS runbooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaowenchen](https://clawhub.ai/user/shaowenchen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations engineers use this skill to investigate infrastructure incidents, query observability systems, and run standard operating procedures through an MCP-connected operations server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute operational procedures through SOPS even though parts of the artifact describe operational-data access as read-only. <br>
Mitigation: Treat the skill as capable of production operations, separate read-only observability credentials from SOP execution privileges where possible, and require explicit human approval before procedure execution. <br>
Risk: Configured MCP server credentials may grant access to infrastructure observability data or operational actions. <br>
Mitigation: Use least-privilege tokens, trust only the configured local ops MCP server, and review the mcporter package and credential configuration before installation. <br>
Risk: Restart, scaling, migration, database, node, or namespace-changing procedures may affect production availability or data state. <br>
Mitigation: Require human confirmation, change-management review, and environment scoping before executing any infrastructure-changing SOP. <br>


## Reference(s): <br>
- [Ops MCP Server Skill Page](https://clawhub.ai/shaowenchen/ops-mcp-server) <br>
- [Event Format Design](references/design.md) <br>
- [Prometheus PromQL Documentation](https://prometheus.io/docs/prometheus/latest/querying/basics/) <br>
- [Elasticsearch ES|QL Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql.html) <br>
- [Jaeger Documentation](https://www.jaegertracing.io/docs/) <br>
- [NATS Subjects Documentation](https://docs.nats.io/nats-concepts/subjects) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell commands, query examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP tool names, PromQL, ES|QL, NATS subject patterns, trace query parameters, and SOP execution parameters.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
