## Description:

Interact with IoT devices via the jettyd platform to read sensors, send commands, manage rules, and list devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jettydiot](https://clawhub.ai/user/jettydiot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let agents inspect jettyd-connected IoT devices, read sensor telemetry, send device commands, manage JettyScript rules, and configure webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent API-key-backed authority over real IoT devices.

Mitigation: Use narrowly scoped tokens and require human confirmation before relay, actuator, device configuration, or webhook changes.

Risk: Secrets may be exposed if API keys or fleet tokens are committed to repositories or firmware defaults.

Mitigation: Keep secrets out of repositories and firmware defaults; prefer managed secrets or environment configuration.

Risk: Custom API base URLs and optional integration dependencies can expand trust assumptions.

Mitigation: Use the default jettyd API endpoint unless a custom endpoint is fully trusted, and pin optional MCP or Python dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jettydiot/skills/jettyd)
- [jettyd homepage](https://jettyd.com)
- [jettyd API base](https://api.jettyd.com/v1)
- [jettyd API Reference](references/api-summary.md)
- [jettyd + OpenClaw Blueprint](blueprint.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, and CLI/API response text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a jettyd API key and Node.js; may read JETTYD_API_KEY or ~/.openclaw/openclaw.json.]

## Skill Version(s):

1.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
