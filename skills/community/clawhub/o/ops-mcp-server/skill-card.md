## Description:

Query observability data and execute operational procedures via the ops-mcp-server MCP interface, covering Kubernetes events, Prometheus metrics, Elasticsearch logs, Jaeger distributed traces, and SOPS runbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaowenchen](https://clawhub.ai/user/shaowenchen)

### License/Terms of Use:


## Use Case:

Developers and operations engineers use this skill to investigate incidents and service health through MCP-backed observability tools, then run standardized operational procedures when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SOP execution can change infrastructure despite the artifact also describing the skill as read-only.

Mitigation: Require explicit human approval before each SOP execution and treat all SOPS workflows as change operations.

Risk: The skill depends on MCP access to operational telemetry and procedures.

Mitigation: Use least-privilege MCP credentials and restrict access to vetted users and environments.

Risk: Setup examples invoke mcporter through npx.

Mitigation: Use a vetted, pinned mcporter version before installing or operating the skill.

## Reference(s):

- [Ops MCP Server Skill Page](https://clawhub.ai/shaowenchen/skills/ops-mcp-server)
- [Event Format Design](references/design.md)
- [Ops MCP Server Examples](examples/README.md)
- [Prometheus PromQL](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Elasticsearch ES|QL](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql.html)
- [Jaeger Documentation](https://www.jaegertracing.io/docs/)
- [NATS Subjects](https://docs.nats.io/nats-concepts/subjects)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, MCP tool calls, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational query patterns, investigation steps, and SOP execution guidance.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
