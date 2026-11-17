## Description:

Control Philips Hue lights/scenes via the OpenHue CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to control Philips Hue lights and scenes through the OpenHue CLI while following guardrails for setup, discovery, and sensitive Hue data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Discovery and setup commands can scan the local network or modify Hue Bridge pairing state.

Mitigation: Run openhue discover or openhue setup only when the user explicitly requests discovery or setup.

Risk: Bridge IP addresses, API keys, device serial numbers, device IDs, room layouts, and related Hue data can expose sensitive home infrastructure details.

Mitigation: Do not include bridge IP addresses, API keys, or device serial numbers in responses, and keep OpenHue output local.

Risk: Piping or sending OpenHue output to network-facing commands can leak sensitive Hue data.

Mitigation: Do not pipe or transmit OpenHue output to network endpoints; provide local-only command alternatives.

Risk: Installing the OpenHue CLI through Homebrew introduces normal third-party tool supply-chain considerations.

Mitigation: Install only if the user is comfortable with an agent operating Hue lights through the OpenHue CLI, and review the Homebrew formula source or publisher when supply-chain assurance is needed.

## Reference(s):

- [OpenHue CLI documentation](https://www.openhue.io/cli)
- [Faberlens OpenHue safety evaluation](https://faberlens.ai/explore/openhue)
- [ClawHub Openhue Hardened skill page](https://clawhub.ai/snazar-faberlens/skills/openhue-hardened)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proposes local OpenHue CLI commands and guardrail-aware guidance; OpenHue output should not be transmitted to network endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
