## Description:

Generate music using the MiniMax music-2.6 model, including text-to-music, instrumental tracks, cover generation, and automatic lyrics generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[4833675](https://clawhub.ai/user/4833675)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate vocal or instrumental music, create cover versions from reference audio, and produce lyrics-backed music through MiniMax APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send music prompts, lyrics, API keys, and selected reference audio to MiniMax or to a configured endpoint.

Mitigation: Use only the documented MiniMax domains and avoid submitting sensitive prompts, lyrics, or reference audio unless the user has approved that data sharing.

Risk: The artifact asks users to store API keys in skill files.

Mitigation: Prefer MINIMAX_API_KEY from an environment variable or secret store, and do not paste credentials into SKILL.md or scripts/generate.py.

## Reference(s):

- [MiniMax Music Generation Documentation](https://platform.minimaxi.com/docs/guides/music-generation)
- [ClawHub Skill Page](https://clawhub.ai/4833675/skills/minimax-tokenplan-music)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [CLI guidance with stdout returning either a local audio file path or a temporary audio URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated audio may be written as WAV, MP3, or PCM; URL output is documented as valid for 24 hours.]

## Skill Version(s):

0.9.0 (source: server release metadata, frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
