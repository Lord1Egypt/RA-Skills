## Description:

Configure OpenClaw to use Google Vertex AI Gemini models so normal OpenClaw startup, Gateway service startup, and TUI usage all work without manual shell setup, and keep the Gateway service aligned with the globally installed npm OpenClaw binary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bhrum](https://clawhub.ai/user/bhrum)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure or repair OpenClaw so Google Vertex AI Gemini models work through normal CLI, Gateway, and TUI startup paths. It is intended for setups that need repeatable Vertex ADC authentication, shared environment wiring, Gateway service alignment, and end-to-end verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared environment files and broad shell environment import can increase credential exposure.

Mitigation: Keep OpenClaw environment files and Google ADC credentials readable only by the user, and avoid broad shell environment import unless exported secrets are understood.

Risk: Refreshing a persistent Gateway service can leave OpenClaw using a stale or mismatched binary if the active CLI path is not verified.

Mitigation: Verify the active openclaw binary before reinstalling the Gateway and prefer a pinned OpenClaw npm version for repeatable service behavior.

Risk: Repair steps can disrupt existing OpenClaw service or configuration files.

Mitigation: Back up existing service and configuration files before applying changes, then verify model status, Gateway health, and TUI behavior after the update.

## Reference(s):

- [OpenClaw Vertex Setup on ClawHub](https://clawhub.ai/bhrum/skills/openclaw-vertex-setup)
- [Vertex AI generateContent endpoint pattern](https://aiplatform.googleapis.com/v1/projects/{project}/locations/global/publishers/google/models/{model}:generateContent)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline JSON, dotenv, and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits to local OpenClaw configuration, environment files, auth profile files, and Gateway service setup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
