## Description: <br>
Connect live streaming data (MQTT, Kafka, Webhook) to your AI agent via MCP with automated alerts and anomaly detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsafaya-edrv](https://clawhub.ai/user/rsafaya-edrv) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to connect MQTT, Kafka, and webhook streams to an AI agent through JustinX MCP, then inspect live messages, create alerts, and expose WebSocket streams for live applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stream data and credentials are sent to JustinX as a third-party service. <br>
Mitigation: Use scoped API keys and least-privilege broker credentials, avoid sending secrets or regulated data unless approved, and confirm retention and compliance requirements before use. <br>
Risk: API keys or broker credentials may be exposed if pasted into configuration files, shell history, or generated examples. <br>
Mitigation: Store credentials in approved secret stores or environment variables, avoid committing local MCP configuration, and rotate keys if they are exposed. <br>


## Reference(s): <br>
- [JustinX homepage](https://justinx.ai) <br>
- [JustinX documentation](https://justinx.ai/docs) <br>
- [JustinX full tool reference](https://justinx.ai/llms-full.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, API calls, Code] <br>
**Output Format:** [Markdown with JSON and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference JustinX MCP tool calls, WebSocket URLs, watcher configuration, and stream message formats.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
