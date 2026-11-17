## Description:

Converts novel chapters into MP3 audiobooks by analyzing chapter structure, identifying narration and dialogue roles, assigning voices, optionally generating mood-matched background music, and assembling the final audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lws-lzh](https://clawhub.ai/user/lws-lzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn provided novel chapter text or chapter files into narrated audiobook output with character-specific voices and optional background music.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chapter text and generated audio workflow data are sent to external AI services.

Mitigation: Use the skill only for manuscripts that may be shared with DeepSeek and MiniMax under their applicable terms.

Risk: API keys are expected in local configuration.

Mitigation: Use throwaway or restricted API keys and keep config.json out of source control and backups.

Risk: Intermediate files may remain on disk after audiobook generation.

Mitigation: Manually clean temp_analysis.json, temp_audio, and temp_bgm after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lws-lzh/skills/novel-to-audiobook-hznuyx17)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-producing script steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent through local script execution that produces intermediate JSON, generated audio segments, optional background music, and a final MP3 audiobook file.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
