## Description: <br>
Transcribe audio files via OpenRouter using audio-capable models (Gemini, GPT-4o-audio, etc). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obviyus](https://clawhub.ai/user/obviyus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to convert a chosen local audio file into a readable transcript through OpenRouter audio-capable chat models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files, transcription prompts, and request metadata are sent to OpenRouter and may be processed by the chosen model provider. <br>
Mitigation: Use only recordings approved for third-party processing, choose an API key dedicated to this workflow, and monitor OpenRouter usage and billing. <br>
Risk: Transcription quality depends on the chosen audio-capable model and the input audio condition. <br>
Mitigation: Review transcripts before relying on them, and retry with a suitable model or clearer source audio when accuracy matters. <br>


## Reference(s): <br>
- [OpenRouter Documentation](https://openrouter.ai/docs) <br>
- [OpenRouter Chat Completions API](https://openrouter.ai/api/v1/chat/completions) <br>
- [ClawHub Skill Page](https://clawhub.ai/obviyus/openrouter-transcribe) <br>
- [Publisher Profile](https://clawhub.ai/user/obviyus) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text transcript to stdout or a text file when --out is provided.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY and local curl, ffmpeg, base64, and jq binaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
