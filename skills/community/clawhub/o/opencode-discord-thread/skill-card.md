## Description:

Use this skill when OpenClaw should hand a coding task to OpenCode, keep the OpenCode run model-compatible with Z.AI Coding Plan / GLM plans, and mirror execution progress into a Discord thread for live review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[r0s-org](https://clawhub.ai/user/r0s-org)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to delegate local coding tasks to OpenCode while mirroring progress, summaries, and transcript chunks into a Discord thread for live review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coding-session content can be sent to Discord without redaction.

Mitigation: Use the skill only with repositories and prompts suitable for the target Discord audience, and prefer restricted or private threads.

Risk: The Discord bot token can be exposed to the OpenCode subprocess environment.

Mitigation: Use a minimally privileged Discord bot token and avoid sensitive repositories until token isolation is added.

Risk: Transcript sharing may be broader than intended for sensitive work.

Mitigation: Review before installing and avoid sensitive repositories until redaction and transcript opt-in or opt-out controls are available.

## Reference(s):

- [OpenCode Discord Bridge Reference](artifact/references/opencode_discord_bridge.md)
- [ClawHub Skill Page](https://clawhub.ai/r0s-org/skills/opencode-discord-thread)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash examples; runtime output is posted as Discord status messages, summaries, and transcript chunks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bridge uses a rolling Discord status message and chunks large transcript output to stay within message limits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
