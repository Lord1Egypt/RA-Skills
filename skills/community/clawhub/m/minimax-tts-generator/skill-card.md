## Description: <br>
MiniMax TTS Generator converts text into natural-sounding speech using MiniMax APIs, with selectable voices, speed and pitch controls, and MP3, WAV, or PCM output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanhaixuan](https://clawhub.ai/user/lanhaixuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content creators, and agents use this skill to turn scripts, articles, narration, or multi-segment dialogue into audio through the MiniMax TTS API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys and submitted text could be exposed if MINIMAX_API_HOST points to an untrusted endpoint. <br>
Mitigation: Use a dedicated MiniMax TTS key, keep MINIMAX_API_HOST unset unless the endpoint is explicitly trusted, and avoid sending sensitive text. <br>
Risk: User-selected output paths can overwrite existing files. <br>
Mitigation: Choose output paths inside a safe workspace and review the target path before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lanhaixuan/minimax-tts-generator) <br>
- [MiniMax Open Platform](https://platform.minimaxi.com) <br>
- [MiniMax Speech Models](https://www.minimaxi.com/models/speech) <br>


## Skill Output: <br>
**Output Type(s):** [Audio files, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON status responses with generated MP3, WAV, or PCM audio file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and MINIMAX_API_KEY; multi-segment merging may require ffmpeg.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
