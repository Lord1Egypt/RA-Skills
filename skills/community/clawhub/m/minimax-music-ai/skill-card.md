## Description:

Generates lyrics, instrumental tracks, vocal songs, and batch music samples through the MiniMax API, with optional FFmpeg audio merging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[838997125](https://clawhub.ai/user/838997125)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, developers, and agents use this skill to generate lyrics and MP3 music assets for short videos, audio content, background music, and song drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact ships a hardcoded MiniMax API credential.

Mitigation: Revoke the exposed credential, replace it with a securely provided user key, and review the skill before installation or execution.

Risk: Prompts and lyrics are sent to a third-party MiniMax API without clear privacy warnings or consent guidance.

Mitigation: Use only non-sensitive prompts and lyrics, and add explicit privacy and permission disclosures before release.

Risk: Batch generation, downloads, and FFmpeg merging can write or overwrite local files.

Mitigation: Review command arguments and target paths before running generation or merge workflows.

## Reference(s):

- [MiniMax Music API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/838997125/skills/minimax-music-ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; generated runtime artifacts may include lyric text files and MP3 audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MiniMax API calls and optional FFmpeg merging; audio download URLs are described as time-limited.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
