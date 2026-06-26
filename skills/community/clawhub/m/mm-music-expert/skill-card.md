## Description: <br>
Create music with MiniMax music models for songs, instrumental tracks, and chanting from lyrics and style prompts via the MiniMax Music Generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BLUE-coconut](https://clawhub.ai/user/BLUE-coconut) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to guide music novices through planning, drafting, generating, and revising songs or instrumental tracks with MiniMax music models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, lyrics, style references, and auto-lyrics requests are sent to MiniMax for processing. <br>
Mitigation: Avoid submitting secrets, sensitive personal text, or confidential unreleased material. <br>
Risk: The skill saves generated audio to a local output path that may already exist. <br>
Mitigation: Choose an output path where overwriting a file would not matter. <br>
Risk: The workflow depends on a MiniMax API key. <br>
Mitigation: Install and run only if you are comfortable using a MiniMax API key with this skill. <br>


## Reference(s): <br>
- [MiniMax Music API Reference](references/minimax_music_api.md) <br>
- [MiniMax Music Generation API Documentation](https://platform.minimaxi.com/docs/api-reference/music-generation) <br>
- [MiniMax Music Generation API Endpoint](https://api.minimaxi.com/v1/music_generation) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with command examples and generated audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MINIMAX_MUSIC_API_KEY and may save audio to a user-selected local output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
