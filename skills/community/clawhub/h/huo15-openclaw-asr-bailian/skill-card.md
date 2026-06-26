## Description: <br>
Uses Alibaba Bailian Paraformer or Fun-ASR to transcribe user-approved audio or video from a public URL, then produce a transcript, meeting-style summary, and OpenClaw ASR delivery block. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agents use this skill when they need cloud ASR for recordings or videos through Alibaba Bailian rather than local Whisper. It is intended for workflows where the user has approved public URL sharing and cloud transcription. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media is exposed through a public share URL and processed by Alibaba Bailian cloud transcription. <br>
Mitigation: Confirm user approval before each run, use local Whisper for confidential or offline transcription, and avoid fabricating or manually composing share URLs. <br>
Risk: The skill requires the sensitive DASHSCOPE_API_KEY credential. <br>
Mitigation: Keep the key in the runtime environment only and do not write it into chat, skill files, command history examples, or generated artifacts. <br>
Risk: Cloud transcription may fail or return empty or low-quality text for unsupported formats, inaccessible URLs, or unsuitable model settings. <br>
Mitigation: Check that the task succeeded and the transcript is non-empty before summarizing; retry with a supported format, a valid URL, or an alternate Bailian model when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-openclaw-asr-bailian) <br>
- [Project homepage](https://cnb.cool/huo15/ai/huo15-skills) <br>
- [Alibaba Bailian recording file recognition](https://help.aliyun.com/zh/model-studio/recording-file-recognition) <br>
- [Alibaba Bailian Paraformer Python SDK](https://help.aliyun.com/zh/model-studio/paraformer-recorded-speech-recognition-python-sdk) <br>
- [Standard operating procedure](docs/SOP.md) <br>
- [Bailian transcription script notes](scripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, transcript text, summary markdown, and an OpenClaw delivery block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY and either a user-provided public media URL or an OpenClaw enhance_share_file public share URL.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter, _meta.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
