## Description:

Operation Tracer records tool calls, LLM calls, errors, and context compression events in a local SQLite database for after-the-fact analysis and performance optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent engineers use Operation Tracer to instrument agent workflows, persist operation traces, analyze slow or failed operations, and export trace data for debugging or optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trace records and JSON/CSV exports may contain sensitive tool parameters, file paths, prompts, results, and errors.

Mitigation: Avoid tracing secrets, protect or delete traces/agent_traces.db when needed, and review exported data before sharing.

## Reference(s):

- [Trace Schema](references/trace_schema.md)

## Skill Output:

**Output Type(s):** [code, configuration, guidance]

**Output Format:** [Markdown with Python code examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local SQLite trace records and supports JSON/CSV export through the included analyzer.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
