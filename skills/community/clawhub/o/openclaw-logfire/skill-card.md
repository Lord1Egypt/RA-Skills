## Description: <br>
Pydantic Logfire observability for OpenClaw with OTEL GenAI traces, tool call spans, token metrics, and optional distributed tracing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[namabile](https://clawhub.ai/user/namabile) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and platform engineers use this plugin to observe OpenClaw agent runs in Pydantic Logfire, including tool spans, token metrics, errors, and optional cross-service trace propagation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telemetry can include sensitive agent data such as tool arguments when captureToolInput is enabled. <br>
Mitigation: Set captureToolInput to false for sensitive environments, keep captureToolOutput and captureMessageContent disabled unless required, leave redactSecrets enabled, and review truncation limits. <br>
Risk: Distributed tracing can propagate trace context into outbound HTTP commands when enabled. <br>
Mitigation: Leave distributedTracing disabled unless needed, or restrict urlPatterns to trusted service URLs. <br>
Risk: The Logfire write token is required for export and could expose telemetry ingestion if mishandled. <br>
Mitigation: Store LOGFIRE_TOKEN in a secret store or environment configuration and do not commit it to source-controlled files. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/namabile/openclaw-logfire) <br>
- [npm package](https://www.npmjs.com/package/@ultrathink-solutions/openclaw-logfire) <br>
- [Pydantic Logfire](https://pydantic.dev/logfire) <br>
- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) <br>
- [OpenClaw production deployment article](https://ultrathinksolutions.com/the-signal/openclaw-to-production/) <br>


## Skill Output: <br>
**Output Type(s):** [telemetry traces, metrics, trace links, configuration] <br>
**Output Format:** [OTLP HTTP/protobuf telemetry exported to Logfire, plus OpenClaw configuration and shell commands in documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LOGFIRE_TOKEN. Tool input capture is enabled by default; tool output, message content, tool definitions, inference events, and distributed tracing are disabled by default.] <br>

## Skill Version(s): <br>
0.1.2 (source: frontmatter, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
