## Description:

Query available models from your configured providers and add them to OpenClaw config.

This skill is ready for commercial/non-commercial use.

## Publisher:

[da-kaine](https://clawhub.ai/user/da-kaine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to query configured OpenClaw API providers for available models, then add selected model definitions and aliases to the local OpenClaw configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send local or environment-backed API credentials to arbitrary configured provider URLs.

Mitigation: Review each provider baseUrl before use and avoid untrusted, plaintext HTTP, private-network, or recently changed provider URLs unless credential exposure is acceptable.

Risk: The skill modifies OpenClaw model defaults after model selection.

Mitigation: Confirm selected models before saving and rely on the backup created by the skill to recover the prior configuration if needed.

## Reference(s):

- [ClawHub metadata homepage](https://github.com/openclaw/skills/model-catalog)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Interactive terminal text and JSON configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a backup file before modifying the OpenClaw configuration.]

## Skill Version(s):

0.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
