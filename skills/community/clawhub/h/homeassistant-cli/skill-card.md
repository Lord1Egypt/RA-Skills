## Description:

Advanced Home Assistant control using the official hass-cli tool, including auto-completion, event monitoring, history queries, and table, YAML, or JSON output formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joneschi](https://clawhub.ai/user/joneschi)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to guide agent-assisted Home Assistant control through hass-cli. It supports interactive entity discovery, service calls, event monitoring, history queries, shell completion, and formatted output for smart-home operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide commands that use broad Home Assistant access tokens.

Mitigation: Use HTTPS with certificate verification, avoid printing or pasting tokens, and store credentials in a secret manager or restricted Home Assistant CLI configuration.

Risk: Generated service-call commands can change the state of live smart-home devices.

Mitigation: Confirm the exact entity and service with the user before execution and test state-changing commands only on verified non-critical entities.

Risk: Troubleshooting guidance may involve bypassing certificate checks for self-signed deployments.

Mitigation: Prefer trusted certificates or explicit certificate files; use insecure mode only when the user understands the local trust boundary.

## Reference(s):

- [Home Assistant CLI project](https://github.com/home-assistant-ecosystem/home-assistant-cli)
- [ClawHub skill page](https://clawhub.ai/joneschi/skills/homeassistant-cli)
- [Autocomplete setup](references/autocomplete.md)
- [Examples](references/examples.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Home Assistant entity IDs, service-call arguments, environment variables, and selectable table, YAML, or JSON CLI output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
