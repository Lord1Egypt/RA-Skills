## Description: <br>
persona-voice helps ChatGPT or Claw generate short persona-styled replies for Feishu/Lark bots, synthesize them with SenseAudio TTS, and send them as native Feishu voice messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hei-MaoM](https://clawhub.ai/user/Hei-MaoM) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and bot operators use this skill to run persona-based voice replies in Feishu/Lark chat workflows. It supports text input and audio input, using SenseAudio ASR for transcription and SenseAudio TTS plus Feishu APIs for native voice-message delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Feishu bot credentials and a SenseAudio API key. <br>
Mitigation: Use least-privilege Feishu permissions, keep .env files out of source control, and rotate credentials if exposed. <br>
Risk: Chat text, generated replies, and voice recordings may be processed by external providers. <br>
Mitigation: Inform chat users before use and avoid sensitive conversations unless the providers' data-handling terms are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Hei-MaoM/persona-voice) <br>
- [Feishu / Lark integration notes](references/feishu_integration.md) <br>
- [Persona presets](references/personas.md) <br>
- [Provider notes](references/provider_notes.md) <br>
- [Feishu API base URL](https://open.feishu.cn) <br>
- [SenseAudio API base URL](https://api.senseaudio.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Markdown guidance with JSON command output and generated audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persona prompts, transcription JSON, local MP3/OPUS audio files, and Feishu voice-message send results.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
