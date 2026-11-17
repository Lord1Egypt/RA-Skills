## Description:

Searches LogEase logs for security alerts, network device events, and system logs, with relative time windows, sample limits, and aggregation templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x1nq](https://clawhub.ai/user/x1nq)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts and operations engineers use this skill to query LogEase data, inspect recent alerts and infrastructure logs, and generate focused summaries or reports from search and aggregation results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Administrator access details are exposed in the release artifact.

Mitigation: Rotate the exposed LogEase administrator password and replace it with a scoped read-only token loaded from a secret store before deployment.

Risk: The skill includes broader privileged API tooling than a read-only log search skill needs.

Mitigation: Remove or isolate generic OpenAPI mutation servers and deploy only the read-only log search functions needed for the agent.

Risk: LogEase access may use insecure transport or weak certificate handling.

Mitigation: Require HTTPS with certificate validation for all LogEase connections.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/x1nq/skills/logeasy-search)
- [Artifact skill instructions](artifact/SKILL.md)
- [Rizhiyi MCP README](artifact/rizhiyi-mcp/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell and Python examples; MCP tools return JSON text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Log search samples are limited to 100 rows; aggregation queries can summarize broader result sets.]

## Skill Version(s):

1.1.0 (source: server release metadata, released 2026-03-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
