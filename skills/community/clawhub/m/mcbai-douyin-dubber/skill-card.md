## Description: <br>
Auto-dubs Douyin and TikTok videos into a target language by downloading video with Playwright and a Douyin cookie, transcribing with Whisper, translating subtitles with the agent, generating TTS, stretching timing with FFmpeg, mixing audio, and burning subtitles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcbaivn](https://clawhub.ai/user/mcbaivn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content workflow users use this skill to produce dubbed versions of Douyin or TikTok videos, including translated subtitles, generated speech, mixed audio, and a final MP4 output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a full Douyin session cookie, which can grant access to the user's Douyin account. <br>
Mitigation: Use a throwaway or test Douyin account, store the cookie only in the configured local file, never share it, and rotate it after use. <br>
Risk: Transcript and translated text may be sent to the agent and to the selected TTS provider. <br>
Mitigation: Avoid private or sensitive videos and choose the TTS provider deliberately before running the pipeline. <br>
Risk: The security evidence flags external-provider data sharing and dependency review concerns. <br>
Mitigation: Run the skill in a dedicated environment and review dependencies and provider behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mcbaivn/mcbai-douyin-dubber) <br>
- [Publisher Profile](https://clawhub.ai/user/mcbaivn) <br>
- [MCB AI](https://www.mcbai.vn) <br>
- [OpenClaw 101](https://openclaw.mcbai.vn/openclaw101) <br>
- [FFmpeg Downloads](https://ffmpeg.org/download.html) <br>
- [ElevenLabs](https://elevenlabs.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a final dubbed MP4 plus working files such as SRT subtitles, ASS subtitles, TTS audio, and intermediate video/audio assets.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
