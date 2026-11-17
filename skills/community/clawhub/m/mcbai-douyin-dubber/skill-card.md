## Description:

Auto-dubs Douyin/TikTok videos into a target language by downloading with Playwright, transcribing with Whisper, translating subtitles through the agent, generating TTS, and mixing audio and subtitles with FFmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcbaivn](https://clawhub.ai/user/mcbaivn)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and automation developers use this skill to translate and dub Douyin or TikTok videos into another language while producing synchronized subtitles and a mixed output video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin session cookies grant account access if exposed.

Mitigation: Use a throwaway Douyin account, store the cookie file outside shared locations, restrict file permissions, and rotate the cookie after use.

Risk: Subtitle text and generated prompts may include sensitive transcript content.

Mitigation: Avoid confidential videos, review generated prompt/result files, and delete temporary translation artifacts after the run.

Risk: Selected TTS providers and the AI translation step may receive subtitle text despite local-only wording in the skill documentation.

Mitigation: Choose providers according to the data sensitivity of the source video and disclose remote processing before using third-party TTS or agent translation.

Risk: The skill has a suspicious scanner verdict due to data exposure tradeoffs and temporary-file practices.

Mitigation: Run it in a dedicated virtual environment, review dependencies and commands before execution, and scan outputs before sharing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mcbaivn/skills/mcbai-douyin-dubber)
- [Publisher Profile](https://clawhub.ai/user/mcbaivn)
- [MCB AI](https://www.mcbai.vn)
- [OpenClaw 101](https://openclaw.mcbai.vn/openclaw101)
- [Python Downloads](https://www.python.org/downloads/)
- [FFmpeg Downloads](https://ffmpeg.org/download.html)
- [ElevenLabs](https://elevenlabs.io)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated media/subtitle files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a dubbed MP4 plus intermediate MP4, SRT, ASS, MP3, and temporary translation JSON/prompt files during execution.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
