## Description:

Control a GeekMagic holocube display as an AI emote system. Generate holographic sprite kits with Gemini, upload to device, and swap expressions based on agent state (idle, working, error, etc.). Use when the user has a GeekMagic holocube (HelloCubic-Lite or similar) and wants their AI assistant to have a physical face that reacts to conversation context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thrive-spencerj](https://clawhub.ai/user/thrive-spencerj)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to generate, upload, and switch Holocube emote sprites so an assistant can show physical expressions tied to session state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup tooling can delete existing Holocube images during device setup.

Mitigation: Use the skill only with a Holocube you control and make an independent backup before clearing or onboarding the device.

Risk: A malicious or compromised device could cause unsafe local backup writes.

Mitigation: Avoid pointing --ip at untrusted hosts and review backup output paths before relying on generated backups.

Risk: Gemini credentials may be exposed if passed as command-line arguments.

Mitigation: Provide Gemini credentials through the environment or local configuration instead of the --api-key argument.

## Reference(s):

- [TOOLS.md Example - Holocube Section](references/tools-example.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, Python helper scripts, and generated JPG/GIF sprite files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a compatible GeekMagic Holocube on the local network; sprite generation uses Gemini credentials when enabled.]

## Skill Version(s):

1.0.0 (source: server evidence release version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
