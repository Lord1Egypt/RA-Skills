## Description:

Guide for creating OpenClaw plugins using hooks like llm_input and llm_output, with logging, request tracking, and configuration management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cicadafang](https://clawhub.ai/user/cicadafang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create OpenClaw plugins, register lifecycle and LLM hooks, manage plugin configuration, and build logging or request-response correlation patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Logger examples can capture raw prompts, system prompts, conversation history, tool data, or complete responses.

Mitigation: Prefer metadata-only logs with redaction, restrictive file permissions, encryption where needed, and retention limits unless full-content logging is explicitly required and approved.

Risk: Generated plugin code or configuration may be used without enough review despite the suspicious security verdict.

Mitigation: Review the generated plugin behavior before installation, especially hook registration, file writes, and any data captured by logging paths.

## Reference(s):

- [Openclaw Plugin Dev on ClawHub](https://clawhub.ai/cicadafang/skills/openclaw-plugin-dev)
- [OpenClaw LLM API Logger example](https://github.com/cicadaFang/openclaw-llm-api-logger)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with TypeScript, JSON, and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce plugin templates, configuration examples, debugging commands, and logging patterns for review before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
