## Description: <br>
MiniMax Text-to-Speech synthesis via the HTTP REST API generates speech audio from text in 40+ languages with selectable voices, models, streaming, and mp3, wav, or pcm outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agents use this skill to convert text into narrated audio or voiceover files through MiniMax TTS, with controls for model, voice, speed, pitch, volume, format, and streaming. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for synthesis and the API key are sent to MiniMax for processing, and a custom API URL can redirect that data to another endpoint. <br>
Mitigation: Use this skill only with text appropriate for MiniMax processing, prefer MINIMAX_API_KEY over command-line secrets, and set --api_url only to endpoints you fully trust. <br>
Risk: Confidential or regulated text may be included in generated speech requests. <br>
Mitigation: Review the text before synthesis and confirm MiniMax terms and organizational policy fit the intended use case. <br>


## Reference(s): <br>
- [MiniMax TTS Voice Reference](references/voices.md) <br>
- [MiniMax TTS API endpoint](https://api.minimax.io/v1/t2a_v2) <br>
- [ClawHub skill page](https://clawhub.ai/fuzzyb33s/minimax-tts-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Audio files in mp3, wav, or pcm format plus console status text and markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MiniMax API key; supports streaming and non-streaming synthesis.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
