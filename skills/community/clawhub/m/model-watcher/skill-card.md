## Description:

Discover, store, and inspect AI model catalog entries from one or more sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hoopan007](https://clawhub.ai/user/hoopan007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to sync an AI model catalog into SQLite, identify newly discovered models, query recent or monthly additions, inspect individual model records, and view catalog statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan command contacts the OpenRouter model catalog API.

Mitigation: Run scan only in environments where outbound access to OpenRouter is acceptable.

Risk: The scan command creates or updates a local SQLite catalog.

Mitigation: Use --db to place the database in an approved location and review the stored catalog data as needed.

## Reference(s):

- [Model Watcher schema](references/schema.md)
- [OpenRouter model catalog API](https://openrouter.ai/api/v1/models)
- [AI Model Watcher on ClawHub](https://clawhub.ai/hoopan007/skills/model-watcher)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scan command creates or updates a local SQLite database and reporting commands print compact catalog summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
