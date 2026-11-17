## Description:

Provides OpenClaw configuration guidance and a bundled preset for token-cost optimizations that adjust heartbeat model selection, plugin enablement, sub-agent archiving, and session cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elontools](https://clawhub.ai/user/elontools)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill when setting up or tuning an OpenClaw instance to reduce routine token and storage costs while preserving factory defaults for context management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying the bundled preset can broadly change OpenClaw configuration, including disabling messaging integrations and enforcing session cleanup.

Mitigation: Back up configuration and session state before applying the preset, and remove plugin-disabling or session-pruning sections that do not match the target instance.

Risk: Messaging integrations such as WhatsApp, Discord, Slack, Nostr, Google Chat, iMessage, and Signal can be disabled by the preset.

Mitigation: Review references/preset-safe.json before use and keep required messaging plugins enabled.

Risk: Earlier versions of the skill are described as having caused production tool-call loops after changing context-management settings.

Mitigation: Keep OpenClaw factory defaults for contextPruning, compaction, bootstrapMaxChars, hardClear, softTrim, reserveTokensFloor, and maxHistoryShare unless separately reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/elontools/skills/openclaw-elontools-optimizer-v3)
- [Safe Preset Configuration](references/preset-safe.json)

## Skill Output:

**Output Type(s):** [configuration, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON configuration references and gateway command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes post-application verification checks for OpenClaw configuration and active plugins.]

## Skill Version(s):

3.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
