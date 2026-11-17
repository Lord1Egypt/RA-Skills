## Description:

Connect live streaming data from MQTT, Kafka, and webhooks to an AI agent through MCP with automated alerts and anomaly detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsafaya-edrv](https://clawhub.ai/user/rsafaya-edrv)

### License/Terms of Use:


## Use Case:

Developers building AI agents use justinX to connect MQTT brokers, Kafka topics, and webhook streams through MCP, inspect live messages, create stream watchers, and expose WebSocket feeds for live dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected stream data and broker credentials may be sensitive.

Mitigation: Use secret storage or environment variables for JustinX, broker, and API credentials, and avoid exposing credentials in generated configuration examples.

Risk: Regulated, confidential, or production stream data may be sent to a third-party streaming-data service.

Mitigation: Confirm JustinX is approved for the intended data and review the provider's security, logging, and retention practices before connecting sensitive streams.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/rsafaya-edrv/skills/justinx)
- [JustinX homepage](https://justinx.ai)
- [JustinX documentation](https://justinx.ai/docs)
- [JustinX full tool reference](https://justinx.ai/llms-full.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON configuration snippets and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JUSTINX_API_KEY for MCP access and may require broker or stream credentials for private data sources.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
