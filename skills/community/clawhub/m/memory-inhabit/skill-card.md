## Description:

Loads SoulPod persona packages so an agent can converse in character, with replica and companion modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evangeliona](https://clawhub.ai/user/evangeliona)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Memory Inhabit to load SoulPod persona packages and run character-based chat in replica or companion mode, including optional diary, image generation, and text-to-speech workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores private conversation-derived history and diary data locally.

Mitigation: Avoid sensitive conversations when using the skill, and periodically review or delete local history and diary files.

Risk: Image and text-to-speech workflows may send prompts, chat text, or voice text to external media APIs.

Mitigation: Use only configured providers you trust, keep API keys protected, and avoid sending sensitive text to image or TTS generation.

Risk: Image reference paths can expose local files when passed to external image generation.

Mitigation: Do not pass arbitrary local paths as image references; use only trusted persona assets intended for upload.

Risk: Persona packages can strongly steer agent behavior and identity.

Mitigation: Install and use only trusted SoulPod persona packages, and review persona prompts, memories, and configuration before use.

## Reference(s):

- [Memory Inhabit product homepage](https://memory-series.github.io/#/product/inhabit)
- [ClawHub skill page](https://clawhub.ai/evangeliona/skills/memory-inhabit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown and text responses with JSON status from helper scripts and generated local media or memory files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce persona chat content, diary traces, image URLs or files, audio files, and local conversation history.]

## Skill Version(s):

1.1.7 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
