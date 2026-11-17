## Description:

Switches an OpenClaw agent's active LLM model on the Huddle01 GRU gateway and reports the current model state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omguptaind](https://clawhub.ai/user/omguptaind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to change or inspect the active model for agents configured with the hudl provider backed by gru.huddle01.io.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad or ambiguous chat phrasing can trigger persistent changes to the active and default OpenClaw model and then restart the agent.

Mitigation: Review the requested model before switching, prefer explicit model names, and confirm the active/default values before restart.

Risk: Model switching changes local OpenClaw configuration.

Mitigation: Back up the OpenClaw config before switching and verify both active and default model fields after the script runs.

Risk: Gateway validation accepts HTTP as well as HTTPS for the GRU base URL.

Mitigation: Use only an HTTPS Huddle01 GRU baseUrl for deployment.

Risk: The GitHub fallback install path is unpinned while server-resolved import provenance is unavailable.

Mitigation: Prefer the ClawHub release artifact or independently verify the repository state before using the GitHub fallback.

## Reference(s):

- [Hudl Model Switch Skill Page](https://clawhub.ai/omguptaind/skills/hudl-model-switch)
- [GRU Gateway](https://gru.huddle01.io)
- [GRU Gateway Models API](https://gru.huddle01.io/v1/models)
- [GRU Gateway Model Catalog](references/models.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status messages with shell command execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update OpenClaw configuration and initiate an OpenClaw restart when used for model switching.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
