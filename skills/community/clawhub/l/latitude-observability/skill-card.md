## Description: <br>
Export OpenClaw OTLP traces to Latitude for open-source LLM observability and evaluation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[latitude](https://clawhub.ai/user/latitude) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure OpenClaw telemetry so model-call, run, tool, and message spans are delivered to Latitude for observability and evaluation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenClaw telemetry may send trace metadata to Latitude or to a self-hosted Latitude endpoint. <br>
Mitigation: Review organizational telemetry, retention, and privacy policies before enabling the exporter, and keep raw prompt or response capture disabled unless policy allows it. <br>


## Reference(s): <br>
- [Latitude Observability on ClawHub](https://clawhub.ai/latitude/skills/latitude-observability) <br>
- [Latitude](https://latitude.so) <br>
- [Latitude MCP Getting Started](https://docs.latitude.so/getting-started/mcp) <br>
- [Latitude Dashboard](https://console.latitude.so/login) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, Markdown] <br>
**Output Format:** [Markdown with JSON5 configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LATITUDE_API_KEY and LATITUDE_PROJECT environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
