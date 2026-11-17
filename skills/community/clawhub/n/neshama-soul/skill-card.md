## Description:

Neshama Soul Openclaw gives an AI agent a persistent personality, emotion-aware response style, and user preference memory based on OCEAN and Valence-Arousal models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neshama-ai](https://clawhub.ai/user/neshama-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can install this skill to add persistent persona, user preference memory, and emotion-aware response guidance to an OpenClaw agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent profile files can influence future sessions in ways the user may not expect.

Mitigation: Review the generated profile files before use, keep reset and delete controls available, and do not allow profile updates without clear user consent.

Risk: Some messages may be sent to api.neshama.pw when the external API path is used.

Mitigation: Use local-only behavior for confidential work, avoid sending secrets or sensitive project data, and require explicit consent before external API use.

Risk: The artifact claims not to upload certain data while also describing external API use.

Mitigation: Treat the privacy behavior as unresolved until the publisher provides clear data minimization, consent, and retention terms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neshama-ai/skills/neshama-soul)
- [Neshama website](https://neshama.pw)
- [SoulCraft](https://neshama.pw/soulcraft)
- [Neshama Soul API docs](https://api.neshama.pw/docs)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, shell commands]

**Output Format:** [Markdown text with optional shell commands and configuration file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local soul configuration files and may use an external API when enabled by the skill behavior.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
