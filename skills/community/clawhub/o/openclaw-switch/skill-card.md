## Description:

Openclaw Switch helps agents manage OpenClaw model routing by listing configured providers, switching the primary model, visualizing fallback chains, and showing heartbeat and subagent routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2233admin](https://clawhub.ai/user/2233admin)

### License/Terms of Use:

MIT License

## Use Case:

Developers and OpenClaw users use this skill to inspect and adjust local model provider routing, primary model selection, and fallback chains for reliability and cost control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted OpenClaw config or config path could trigger local code execution through the bundled switch script.

Mitigation: Run the switch command only against trusted OpenClaw configuration files and prefer a reviewed patched release that passes values to Python through argv or environment variables.

Risk: Installation guidance may add persistent shell-profile PATH changes.

Mitigation: Review shell-profile edits before applying them, scope PATH changes to the intended OpenClaw bin directory, and remove the entry when it is no longer needed.

Risk: The skill changes the primary model setting in the local OpenClaw configuration.

Mitigation: Back up or review openclaw.json before switching models, and verify the selected model and fallback chain after the command runs.

## Reference(s):

- [Openclaw Switch on ClawHub](https://clawhub.ai/2233admin/skills/openclaw-switch)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Terminal text and local JSON configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads and may update the local OpenClaw configuration file selected by OPENCLAW_CONFIG or the default user OpenClaw config path.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
