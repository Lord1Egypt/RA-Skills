## Description: <br>
Characteristic Voice helps an agent write and generate emotionally expressive companion-style speech with presets, fillers, emotion tuning, and optional TTS backends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ksuriuri](https://clawhub.ai/user/Ksuriuri) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to make generated speech feel warmer and more companion-like, with presets for good night, morning, comfort, celebration, and chat plus script-based TTS output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text and reference audio may be sent to Noiz when the Noiz backend or --ref-audio option is used. <br>
Mitigation: Use the Kokoro backend for private or offline speech, and avoid uploading private or unlicensed voice recordings. <br>
Risk: The script can store a Noiz API key locally at ~/.noiz_api_key. <br>
Mitigation: Remove ~/.noiz_api_key when Noiz access is no longer needed and manage the key with normal local credential hygiene. <br>
Risk: Voice cloning or character-style reference audio can raise consent, copyright, or personality-rights concerns. <br>
Mitigation: Use user-provided or properly licensed reference audio and review rights before uploading or reusing voice samples. <br>


## Reference(s): <br>
- [Characteristic Voice on ClawHub](https://clawhub.ai/Ksuriuri/noizai-characteristic-voice) <br>
- [Noiz API Keys](https://developers.noiz.ai/api-keys) <br>
- [Noiz API endpoint](https://noiz.ai/v1) <br>
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) <br>
- [FFmpeg](https://ffmpeg.org) <br>
- [ripgrep](https://github.com/BurntSushi/ripgrep) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and generated audio file paths from the shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create WAV or MP3 audio files through Kokoro locally or the Noiz API, depending on backend configuration.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
