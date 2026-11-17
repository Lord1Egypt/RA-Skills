## Description:

Add the NVIDIA provider to OpenClaw with SecretRef apiKey (no plaintext in openclaw.json). Documents shell vs systemd gateway env so the key actually resolves. Includes Mixtral, Kimi, Nemotron Super, Nemotron Ultra, and MiniMax M2.5 model entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xli](https://clawhub.ai/user/0xli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add the NVIDIA provider and bundled model entries to OpenClaw configuration while keeping the API key in an environment-backed SecretRef.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can update OpenClaw configuration and optional gateway environment files.

Mitigation: Use --dry-run to inspect changes first and --backup before writing to an existing openclaw.json.

Risk: An NVIDIA API key may be exposed if passed on the command line or written inline to configuration.

Mitigation: Prefer NVIDIA_API_KEY from a protected shell environment or user-owned gateway.env file, and avoid --inline-key except for short-lived local testing.

Risk: The OpenClaw gateway may not resolve the key if it runs under systemd without the expected environment file.

Mitigation: Configure a private gateway.env path and systemd user override when the gateway is managed by systemd.

## Reference(s):

- [NVIDIA API endpoint used by the skill](https://integrate.api.nvidia.com/v1)
- [ClawHub skill page](https://clawhub.ai/0xli/skills/nvidia-model-config)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with bash commands and JSON configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write OpenClaw configuration, a backup file, a gateway environment file, or a systemd user override when the user runs the bundled script with those options.]

## Skill Version(s):

1.0.5 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
