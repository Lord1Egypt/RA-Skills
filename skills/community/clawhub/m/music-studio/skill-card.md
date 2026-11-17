## Description:

Music Studio is a lightweight MiniMax-based music creation workspace that guides an agent through lyrics generation, text-to-music generation, cover-song preprocessing, local output management, and music library actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrgyan](https://clawhub.ai/user/mrgyan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create lyrics, generate music from text prompts, produce cover-song outputs through MiniMax, and manage generated files through a local music library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain a MiniMax API key in local configuration.

Mitigation: Use a dedicated MiniMax key, store it only on trusted machines, clear or rotate the key after testing, and avoid committing local config files.

Risk: Prompts, lyrics, and cover-audio URLs are sent to MiniMax for generation.

Mitigation: Avoid submitting confidential lyrics, unpublished audio, personal data, or third-party content that the user is not authorized to process.

Risk: Clean, reset, and purge actions can delete local generated outputs in the configured output directory.

Mitigation: Use a dedicated output directory, review the configured path before cleanup, and keep backups of outputs that must be retained.

Risk: Downloaded audio is fetched from service-provided URLs and written locally.

Mitigation: Download only expected generation outputs, keep the output directory isolated, and review files before reusing or distributing them.

## Reference(s):

- [ClawHub Music Studio skill page](https://clawhub.ai/mrgyan/skills/music-studio)
- [MiniMax music API reference](artifact/references/api.md)
- [MiniMax API base URL](https://api.minimaxi.com/v1/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown guidance with CLI commands plus generated text, URLs, metadata, and optional audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a MiniMax API key and may write config, session, lyrics, URL, metadata, hex, and MP3 files under the configured local output directory.]

## Skill Version(s):

1.0.10 (source: frontmatter, artifact/music_studio/version.py, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
