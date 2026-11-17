## Description:

Logs subagent task completions as Langfuse traces for replay, evaluation, cost analysis, backfill, tag-based filtering, and replay-judge workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to log completed subagent work into Langfuse so sessions can be replayed, evaluated, filtered by tags, and reviewed for cost and routing analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trace logging can capture prompts, outputs, session metadata, and memory-derived task records that may contain secrets, personal data, or sensitive project context.

Mitigation: Redact secrets and personal data before logging, and install only when storing this data in the configured Langfuse project is acceptable.

Risk: Cloud Langfuse endpoints may move trace data outside the user's local infrastructure.

Mitigation: Prefer a local self-hosted Langfuse instance, and use cloud endpoints only when approved for the data being logged.

Risk: Interpolating raw prompt text into shell commands can expose unsafe argument handling paths.

Mitigation: Invoke logging scripts with safe argument handling instead of constructing shell commands from raw prompt text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/langfuse-trace-logger)
- [Publisher profile](https://clawhub.ai/user/nissan)
- [Local Langfuse UI](http://localhost:3100)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown guidance with command examples and trace schema tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.11, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, and a Langfuse endpoint.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
