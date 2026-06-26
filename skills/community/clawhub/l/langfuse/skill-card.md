## Description: <br>
Query and manage Langfuse traces, prompts, datasets, sessions, observations, scores, and metrics via Langfuse SDKs and the public API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[south-american-cowboy](https://clawhub.ai/user/south-american-cowboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add or audit Langfuse tracing, prompt management, evaluations, data querying, and self-hosted deployment guidance in Python or JS/TS projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live Langfuse credentials may allow an agent to query or change prompts, traces, scores, datasets, and related project data. <br>
Mitigation: Provide credentials through environment variables when possible, prefer scoped or read-only keys for read-only work, and only grant live access when the task requires it. <br>
Risk: Self-hosted Langfuse base URLs can reveal private infrastructure context. <br>
Mitigation: Use internal deployment URLs only for the Langfuse task at hand and avoid replacing self-hosted values with cloud defaults. <br>


## Reference(s): <br>
- [Langfuse skill release](https://clawhub.ai/south-american-cowboy/langfuse) <br>
- [Prompt Migration](references/prompt-migration.md) <br>
- [Tracing and Querying](references/tracing-and-querying.md) <br>
- [Evaluations and Scores](references/evals-and-scores.md) <br>
- [Self-Hosted Langfuse](references/self-hosted.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code blocks, shell commands, API examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
