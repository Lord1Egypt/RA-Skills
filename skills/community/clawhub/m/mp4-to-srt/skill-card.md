## Description: <br>
Converts local MP4, MKV, or AVI video files into SRT subtitles and automatically converts the subtitle text to Traditional Chinese. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dolphins1123](https://clawhub.ai/user/dolphins1123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and media operators use this skill to generate SRT subtitle files from local video media for YouTube uploads or standard media players. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local media-processing dependencies may introduce supply-chain or execution risk if installed from untrusted sources. <br>
Mitigation: Install ffmpeg, openai-whisper, and opencc only from trusted package sources before using the skill. <br>
Risk: The generated subtitle path may replace or move an existing subtitle file. <br>
Mitigation: Choose and review the output path before running the conversion script. <br>
Risk: Transcription and Chinese conversion quality may vary with audio quality, source language, and Whisper model size. <br>
Mitigation: Review generated subtitles before publication or downstream use, especially for customer-facing media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dolphins1123/mp4-to-srt) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance with shell command examples and generated SRT subtitle files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local ffmpeg, openai-whisper, and opencc installations; default Whisper model is small.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
