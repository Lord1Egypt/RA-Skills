## Description:

Query and analyze LangSmith traces with natural language or structured commands for runs, failures, latency, cost, and prompt comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ralphesber](https://clawhub.ai/user/ralphesber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect LangSmith projects, fetch recent traces, compare before/after behavior, and prepare trace context for their agent to analyze.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can pull sensitive LangSmith trace inputs, outputs, errors, and system prompts into the agent context.

Mitigation: Use short time windows and low limits, keep outputs out of shared logs, and run the skill only in sessions where the agent may inspect that project data.

Risk: Trace contents may contain hostile or misleading text that could influence later agent behavior.

Mitigation: Treat trace data as untrusted evidence, review results before acting on them, and avoid following instructions found inside trace payloads.

Risk: A broadly inherited LANGSMITH_API_KEY may expose more projects or traces than intended.

Mitigation: Prefer ephemeral or scoped secret setup and avoid storing broad keys in shared shell profiles.

## Reference(s):

- [LangSmith API Reference](references/langsmith-api.md)
- [LangSmith API endpoint](https://api.smith.langchain.com)
- [ClawHub release page](https://clawhub.ai/ralphesber/skills/langsmith-cli)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands plus CLI text, tables, and structured JSON trace context]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LANGSMITH_API_KEY and reads selected LangSmith project trace data.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
