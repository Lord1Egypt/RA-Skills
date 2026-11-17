## Description:

Configure an OpenClaw instance to use a local OpenAI-compatible TTS backend with cloned voices, verify model and voice mapping, generate test clips, and troubleshoot LAN or Tailscale access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lotfinity](https://clawhub.ai/user/lotfinity)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to connect OpenClaw message TTS to a trusted local OpenAI-compatible speech backend, confirm cloned voice behavior, and expose the TTS service over LAN or Tailscale when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenClaw configuration changes could route speech synthesis to an unintended backend, model, or cloned voice.

Mitigation: Review proposed OpenClaw config changes before applying them and verify the active base URL, provider, model, and voice with `openclaw config get`.

Risk: Exposing the TTS service beyond the local host could make the endpoint reachable by untrusted users.

Mitigation: Avoid exposing the TTS port beyond trusted LAN or Tailscale users, confirm listener bindings, and restrict access with firewall rules or Tailscale ACLs.

Risk: Docker inspection commands may require elevated local privileges.

Mitigation: Run Docker commands with the least privilege available and inspect only the intended TTS backend container.

Risk: Generated test clips written to shared temporary paths may be overwritten or exposed to other local users.

Mitigation: Use a safer temporary output path for generated test clips when handling sensitive or private voice samples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lotfinity/skills/local-openedai-tts)
- [Publisher profile](https://clawhub.ai/user/lotfinity)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration keys]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OpenClaw configuration commands, direct API test requests, Docker inspection commands, reachability checks, and channel delivery troubleshooting steps.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
