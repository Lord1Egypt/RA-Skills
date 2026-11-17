## Description:

Export OpenClaw OTLP traces to Latitude for open-source LLM observability and evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[latitude](https://clawhub.ai/user/latitude)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure OpenClaw telemetry export so model-call, run, tool, and message spans land in Latitude for observability and evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trace telemetry may include operational metadata and can include prompt or response content if raw capture is enabled.

Mitigation: Confirm retention and privacy requirements before enabling content capture, and leave raw prompt and response capture disabled unless policy allows it.

Risk: A misplaced API key or project slug could send traces to the wrong Latitude project or expose credentials.

Mitigation: Protect LATITUDE_API_KEY as a secret, verify LATITUDE_PROJECT belongs to the intended organization, and confirm the ingest endpoint before deployment.

Risk: Strict provenance requirements may not be satisfied because server-resolved GitHub provenance is unavailable for this release.

Mitigation: Pin or verify the diagnostics plugin version and review the release evidence before installation in provenance-sensitive environments.

## Reference(s):

- [Latitude documentation](https://docs.latitude.so/getting-started/mcp)
- [Latitude](https://latitude.so)
- [Latitude dashboard](https://console.latitude.so/login)
- [ClawHub skill page](https://clawhub.ai/latitude/skills/latitude-observability)
- [Latitude publisher profile](https://clawhub.ai/user/latitude)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown with JSON5 configuration and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Configures OTLP trace export with Latitude API key and project slug environment variables.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
