## Description:

图谱 routes blockchain data questions to suitable Graph Protocol services and provides real-time data, subgraph selection, and query optimization guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and automation teams use this skill to ask blockchain data questions, choose relevant subgraphs, and receive Graph Protocol routing or query optimization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read, execute, and write authority for a task that is documented as Graph Protocol routing.

Mitigation: Install with constrained tool access and review proposed commands or file writes before execution.

Risk: The setup guidance uses a generic API key and includes ambiguous command execution language.

Mitigation: Use scoped credentials, avoid logging secrets, and require an explicit allowlist for commands that may run in the agent environment.

Risk: The documented scope is inconsistent, including non-blockchain analytics claims despite stating that non-blockchain graph database queries are out of scope.

Mitigation: Use the skill only for blockchain Graph Protocol routing and verify material outputs against trusted chain data sources before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/graph-query-2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Graph Protocol routing recommendations, subgraph endpoint suggestions, query optimization guidance, and API key setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.9.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
