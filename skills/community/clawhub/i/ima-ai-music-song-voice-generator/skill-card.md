## Description:

Enables an agent to create AI-generated music, songs, background tracks, jingles, beats, and voice-oriented audio content using IMA-supported music models including Suno sonic v5, DouBao BGM, and DouBao Song.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dai-shuo](https://clawhub.ai/user/dai-shuo)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, marketers, and developers use this skill to direct an agent to generate music or audio assets from text prompts, including songs with lyrics, background music, soundtracks, jingles, beats, and narration-oriented audio. It requires an IMA API key and returns generation status plus an audio result URL for playback or sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials could be exposed to an arbitrary server if the base URL is changed to an untrusted endpoint.

Mitigation: Use the default IMA endpoint for normal operation, and pass --base-url only with trusted development credentials.

Risk: User prompts are sent to IMA's service, and local model preferences or generation logs may be written under ~/.openclaw.

Mitigation: Avoid sensitive prompt content, use limited-scope IMA keys, and delete or disable local preferences and logs when retention is not desired.

Risk: Unsafe shell-style invocation guidance could create command injection risk if user text is concatenated into a shell command.

Mitigation: Invoke the Python script with an argument array and pass the prompt as a single argument rather than constructing a shell command string.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dai-shuo/skills/ima-ai-music-song-voice-generator)
- [IMA Studio homepage](https://imastudio.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON result handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime flow produces status messages and an audio URL from the IMA service; local preferences and logs may be written under ~/.openclaw.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
