## Description: <br>
Text-to-Speech (TTS) and voice-feature skill for Gitee AI that lets the user choose audiofly, chattts, cosyvoice2, cosyvoice3, cosyvoice-300m, fish-speech-1.2-sft, index-tts-1.5, index-tts-2, glm-tts, megatts3, moss-ttsd-v0.5, qwen-tts, spark-tts-0.5b, step-audio-tts-3b, or vibevoice-large, then fills in only model-specific parameters for speech or voice feature extraction, including multi-item Qwen3-TTS inputs with built-in or custom voices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fchange](https://clawhub.ai/user/fchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to route Gitee AI speech synthesis and CosyVoice voice-feature extraction requests across supported TTS models while collecting only model-relevant parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gitee AI API keys can authorize speech generation requests and should be treated as sensitive credentials. <br>
Mitigation: Use a scoped GITEEAI_API_KEY where possible, pass it through the environment or a deliberate --api-key value, and avoid logging or sharing command transcripts that contain the key. <br>
Risk: Voice samples, prompt audio URLs, and generated speech can contain sensitive or unauthorized voice data. <br>
Mitigation: Use only audio the user is permitted to submit, avoid private or internal audio URLs, and obtain clear permission before using another person's voice for cloning or feature extraction. <br>
Risk: Generated binary outputs may be written to local paths selected by the caller. <br>
Mitigation: Choose output paths deliberately and review generated files before sharing or using them downstream. <br>


## Reference(s): <br>
- [TTS Model Routing](references/models.md) <br>
- [Moark Tts on ClawHub](https://clawhub.ai/fchange/moark-tts) <br>
- [Gitee AI API endpoint](https://ai.gitee.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with runnable Python command examples and parsed script result labels such as AUDIO_URL, AUDIO_FILE, TTS_RESULT, VOICE_URL, and VOICE_FEATURE_FILE.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce remote audio URLs, local audio or voice-feature files, or JSON API result summaries depending on the selected model and response mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
