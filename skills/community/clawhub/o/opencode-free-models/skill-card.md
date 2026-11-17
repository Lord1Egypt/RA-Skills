## Description:

Configures free opencode.ai models for OpenClaw or QClaw by fetching available model metadata and adding provider entries to the local model configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinke](https://clawhub.ai/user/pinke)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to add currently available free opencode.ai models to OpenClaw or QClaw without manually editing provider configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically change persistent OpenClaw or QClaw model configuration based on remote data.

Mitigation: Review the proposed configuration changes, back up the existing configuration file, and run the update only after explicit confirmation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/pinke/skills/opencode-free-models)
- [Publisher profile](https://clawhub.ai/user/pinke)
- [opencode.ai models endpoint](https://opencode.ai/zen/v1/models)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update OpenClaw or QClaw model provider configuration on disk when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
