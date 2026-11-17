## Description:

Query and manage Langfuse traces, prompts, datasets, sessions, observations, scores, and metrics via Langfuse SDKs and the public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[south-american-cowboy](https://clawhub.ai/user/south-american-cowboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add or audit Langfuse tracing, prompt management, evaluation scoring, data querying, and self-hosted deployment guidance in Python or JS/TS projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, traces, scores, and related project data may be sent to Langfuse or a self-hosted Langfuse endpoint.

Mitigation: Use scoped project keys, prefer environment variables over pasted secrets, and confirm the intended Langfuse base URL before running generated examples.

Risk: Trace metadata can include personal identifiers or sensitive infrastructure context.

Mitigation: Avoid direct personal identifiers in trace metadata where possible and limit use of internal/self-hosted URLs to the task at hand.

Risk: Generated prompt creation, score writes, or dataset changes can mutate production Langfuse projects.

Mitigation: Review generated mutations before execution and use non-production projects or scoped credentials when validating changes.

## Reference(s):

- [Prompt Migration](references/prompt-migration.md)
- [Tracing and Querying](references/tracing-and-querying.md)
- [Evaluations and Scores](references/evals-and-scores.md)
- [Self-Hosted Langfuse](references/self-hosted.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python, TypeScript, JSON, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SDK/API examples and runbooks; live access requires Langfuse environment variables.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
