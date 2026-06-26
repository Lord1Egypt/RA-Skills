## Description: <br>
Provides MOSI Studio audio workflows for speech recognition, text-to-speech, multi-speaker dialogue synthesis, voice cloning, and Feishu voice-message delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mkkb473](https://clawhub.ai/user/mkkb473) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to transcribe inbound audio, synthesize spoken replies, create multi-speaker dialogue or cloned voices through MOSI, and send Feishu voice bubbles when configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload sensitive audio or text to MOSI cloud services. <br>
Mitigation: Use only with MOSI accounts you trust and avoid sending confidential recordings or text unless MOSI cloud processing is acceptable. <br>
Risk: The voice-cloning workflow can create or use a speaker's voice without authorization. <br>
Mitigation: Use voice cloning only when explicit rights and consent from the speaker are available. <br>
Risk: Feishu voice-message delivery uses app credentials and can send audio to the wrong chat. <br>
Mitigation: Configure least-privilege Feishu credentials and confirm the target chat before sending voice bubbles. <br>
Risk: The server security verdict is suspicious because of voice cloning, cloud audio processing, and Feishu messaging behavior. <br>
Mitigation: Review the skill before installing and validate account, credential, and data-handling controls before deployment. <br>


## Reference(s): <br>
- [MOSI API Reference](references/api.md) <br>
- [MOSI Studio](https://studio.mosi.cn) <br>
- [ClawHub Skill Page](https://clawhub.ai/mkkb473/moss-tts-family-chatbot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Audio files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; scripts produce plain text transcripts, JSON responses, and WAV or OPUS audio files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MOSI_TTS_API_KEY for MOSI calls; Feishu voice messages require FEISHU_APP_ID and FEISHU_APP_SECRET; generated media is expected under ~/.openclaw/workspace/.] <br>

## Skill Version(s): <br>
0.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
