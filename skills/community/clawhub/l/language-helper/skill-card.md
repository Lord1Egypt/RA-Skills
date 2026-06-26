## Description: <br>
Helps users learn how to say a phrase in another language by producing a natural translation, pronunciation audio, grammar notes, vocabulary, and optional alternative expressions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igloomatics](https://clawhub.ai/user/igloomatics) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Language learners and multilingual users use this skill to convert Chinese or English prompts into natural target-language expressions, hear pronunciation audio, and review concise grammar and vocabulary notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input phrases are sent to SenseAudio for text-to-speech generation. <br>
Mitigation: Avoid using the skill with confidential or sensitive text unless sending that content to SenseAudio is acceptable. <br>
Risk: Optional Feishu delivery can upload generated audio and post it to a configured chat. <br>
Mitigation: Use a least-privilege Feishu bot, verify FEISHU_CHAT_ID before sending, and keep Feishu credentials private. <br>
Risk: Debug logs can expose request content when explicitly enabled. <br>
Mitigation: Do not use --debug-log for confidential content and keep the .env file private. <br>


## Reference(s): <br>
- [ClawHub language-helper release page](https://clawhub.ai/igloomatics/language-helper) <br>
- [SenseAudio API endpoint](https://api.senseaudio.cn/v1/t2a_v2) <br>
- [SenseAudio service](https://senseaudio.cn) <br>
- [Feishu developer console](https://open.feishu.cn/app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown response with translated text, pronunciation notes, vocabulary tables, optional alternative phrasing, and TTS command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local audio files or optionally send Feishu voice messages when user credentials are configured.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
