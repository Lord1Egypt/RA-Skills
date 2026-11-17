## Description:

Uses the MiniMax API to convert Chinese text-to-speech requests into MP3 audio files through a guided token, text, and voice-selection flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ggttol](https://clawhub.ai/user/ggttol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill in messaging workflows to collect Chinese text and a voice choice, call MiniMax text-to-speech, and return an MP3 audio file instead of playing local audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided text to MiniMax for text-to-speech generation.

Mitigation: Use it only for content approved for MiniMax processing, and avoid submitting sensitive or regulated text unless that use is permitted.

Risk: The skill stores one shared MiniMax token locally in the skill directory.

Mitigation: Use a scoped token where possible, limit local filesystem access, and rotate the token if the workspace may have been exposed.

Risk: The README recommends broad persistent workspace instruction changes to force TTS behavior.

Mitigation: Avoid applying the global TOOLS.md override across workspaces; review any persistent instruction changes per workspace before deployment.

Risk: The output path can be supplied by the caller and may overwrite existing files.

Mitigation: Prefer the default temporary output location or a dedicated scratch directory, and do not pass paths for important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ggttol/skills/minimax-tts-zh)
- [MiniMax platform](https://minimaxi.com)
- [MiniMax text-to-audio API endpoint](https://api.minimaxi.com/v1/t2a_v2)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Text]

**Output Format:** [MP3 audio files with command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MiniMax API token; generated speech is written to a local MP3 output path.]

## Skill Version(s):

1.2.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
