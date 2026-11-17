## Description:

Pydantic Logfire observability for OpenClaw with OTEL GenAI traces, tool-call spans, token metrics, and distributed tracing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[namabile](https://clawhub.ai/user/namabile)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this plugin to send OpenClaw agent lifecycle traces, tool spans, token metrics, errors, and optional distributed trace context to Pydantic Logfire.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tool arguments and raw error details may be sent to Logfire by default.

Mitigation: Set captureToolInput and captureStackTraces to false unless they are explicitly required for the workspace.

Risk: Sensitive message or tool-result content could be exposed if optional capture settings are enabled.

Mitigation: Keep captureToolOutput and captureMessageContent disabled for normal use, especially in workspaces with credentials, customer data, private files, or production operations.

Risk: Secret redaction is best-effort and may not cover every credential format.

Mitigation: Treat redaction as an additional control rather than a guarantee, avoid sending secrets through tool inputs, and restrict Logfire project access.

## Reference(s):

- [Pydantic Logfire](https://pydantic.dev/logfire)
- [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [npm Package](https://www.npmjs.com/package/@ultrathink-solutions/openclaw-logfire)
- [OpenClaw Production Deployment Article](https://ultrathinksolutions.com/the-signal/openclaw-to-production/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Logfire write token through LOGFIRE_TOKEN or plugin configuration.]

## Skill Version(s):

0.1.2 (source: SKILL.md frontmatter, package.json, CHANGELOG, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
