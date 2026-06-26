## Description: <br>
Converts text, documents, and subtitle timelines into speech audio with local Kokoro or Noiz cloud backends, including voice cloning, emotion control, and per-segment voice mapping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ksuriuri](https://clawhub.ai/user/Ksuriuri) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate narration, voiceovers, dubbing audio, and time-aligned speech from text files, SRT subtitles, PDFs, EPUBs, or direct prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text or reference voice samples may be sent to the Noiz cloud backend when cloud synthesis, emotion control, voice cloning, or duration forcing is used. <br>
Mitigation: Use the local Kokoro backend for private or sensitive text and voice samples, and use Noiz only for content authorized for upload. <br>
Risk: Reference-audio URLs can cause the agent to fetch media from arbitrary remote locations. <br>
Mitigation: Use local reference files or trusted public media URLs, and review requests carefully when the agent has access to internal networks. <br>
Risk: Voice cloning can reproduce recordings without appropriate permission. <br>
Mitigation: Use reference audio only when the user has rights and consent to synthesize speech from the recording. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ksuriuri/noizai-tts) <br>
- [Third-party voice delivery reference](ref_3rd_party.md) <br>
- [Noiz Developer API keys](https://developers.noiz.ai/api-keys) <br>
- [Feishu file upload API](https://open.feishu.cn/document/server-docs/im-v1/file/create) <br>
- [Feishu send message API](https://open.feishu.cn/document/server-docs/im-v1/message/create) <br>
- [Telegram sendVoice API](https://core.telegram.org/bots/api#sendvoice) <br>
- [Discord uploading files](https://discord.com/developers/docs/reference#uploading-files) <br>
- [Discord create message API](https://discord.com/developers/docs/resources/channel#create-message) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated audio, subtitle, configuration, or duration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate WAV, MP3, Opus, Ogg, SRT, JSON voice-map, and duration sidecar files depending on the selected mode and backend.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
