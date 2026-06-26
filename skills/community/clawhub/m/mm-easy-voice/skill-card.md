## Description: <br>
Simple text-to-speech skill using MiniMax Voice API. Converts text to audio with customizable voice selection. Use for generating speech audio from text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BLUE-coconut](https://clawhub.ai/user/BLUE-coconut) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content creators use this skill to generate speech audio from text with selectable MiniMax voices and to manage voice cloning, designed voices, and local audio conversion workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text, text files, and voice samples may be sent to MiniMax's third-party API. <br>
Mitigation: Use only content allowed by MiniMax terms and local policy; avoid confidential material unless that use is approved. <br>
Risk: Voice cloning can misuse voices without permission. <br>
Mitigation: Clone only voices the user owns or has explicit permission to use. <br>
Risk: Audio generation, conversion, and merge commands write to user-supplied output paths. <br>
Mitigation: Verify output paths before running commands and keep backups of source media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BLUE-coconut/mm-easy-voice) <br>
- [Getting Started](reference/getting-started.md) <br>
- [MiniMax Voice Catalog](reference/voice_catalog.md) <br>
- [Voice Management Guide](reference/voice-guide.md) <br>
- [Audio Processing Guide](reference/audio-guide.md) <br>
- [Troubleshooting](reference/troubleshooting.md) <br>
- [MiniMax Speech T2A HTTP API](https://platform.minimaxi.com/docs/api-reference/speech-t2a-http) <br>
- [MiniMax Voice Cloning API](https://platform.minimaxi.com/docs/api-reference/voice-cloning-clone) <br>
- [MiniMax Voice Design API](https://platform.minimaxi.com/docs/api-reference/voice-design-design) <br>
- [FFmpeg download](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration instructions, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash commands and file paths; CLI commands can produce audio files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_VOICE_API_KEY; FFmpeg is optional for merging and conversion.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
