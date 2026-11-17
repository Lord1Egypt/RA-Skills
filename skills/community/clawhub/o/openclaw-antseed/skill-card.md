## Description:

Connects OpenClaw to the AntSeed P2P AI network as a buyer by installing a local buyer proxy and configuring OpenClaw to route LLM requests through available providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kotevcode](https://clawhub.ai/user/kotevcode)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to set up AntSeed as an OpenClaw model provider, start or install the buyer proxy, and configure a selected network model as the OpenClaw default.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path can install a reboot-persistent systemd service.

Mitigation: Use a temporary foreground proxy first and avoid the --service option unless a persistent background process is explicitly intended.

Risk: Future model traffic can be routed through the AntSeed P2P provider network.

Mitigation: Do not route secrets or regulated data through the network unless the providers are trusted, and review OpenClaw configuration changes before use.

Risk: Unsafe setup-script argument handling can enable code or service-file injection.

Mitigation: Treat the setup script as unsafe with untrusted arguments; review inputs and prefer pinned package versions before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kotevcode/skills/openclaw-antseed)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash, JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce OpenClaw configuration changes and optional systemd service setup steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
