## Description:

Execute coding work as a cached dependency graph with local quality gates, parallel agents, localized retries, resume support, token telemetry, and an interactive report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwaghmar](https://clawhub.ai/user/gwaghmar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to structure coding work as a dependency graph, coordinate bounded parallel implementation, run local quality gates, manage retries, and summarize execution results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill bootstraps an unpinned external npm package that can execute changing code before the reviewed runtime exists.

Mitigation: Review the `graph-skill` npm package, pin a trusted exact version, run the bootstrap in a sandboxed workspace without unnecessary secrets, and inspect the generated `.graph/graph.py` before use.

## Reference(s):

- [Graph protocol schema](references/protocol.md)
- [Graph homepage](https://github.com/gwaghmar/graph)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and execution summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local graph reports, cache records, quality-check results, retry plans, and optional commit commands only when explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
