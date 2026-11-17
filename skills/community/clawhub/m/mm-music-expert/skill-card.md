## Description:

Create music with MiniMax music models (music-2.5+, music-2.5) for songs, instrumental tracks, or chanting from lyrics and style prompts via MiniMax Music Generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blue-coconut](https://clawhub.ai/user/blue-coconut)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to clarify music requirements, draft a structured song blueprint, create prompts and lyrics, and generate audio through the MiniMax Music Generation API after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, lyrics, and the MiniMax API credential are sent to the MiniMax service for generation.

Mitigation: Use an authorized MiniMax API key and avoid submitting confidential or sensitive material unless approved for that service.

Risk: Generated audio is written to local files.

Mitigation: Choose an intended output path and handle generated audio according to applicable data retention and sharing requirements.

## Reference(s):

- [MiniMax Music API Reference](references/minimax_music_api.md)
- [MiniMax Music Generation API Documentation](https://platform.minimaxi.com/docs/api-reference/music-generation)
- [ClawHub Skill Page](https://clawhub.ai/blue-coconut/skills/mm-music-expert)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with prompts, lyrics, command examples, and generated audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use the MINIMAX_MUSIC_API_KEY environment variable, call the MiniMax API, and save generated audio locally.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
