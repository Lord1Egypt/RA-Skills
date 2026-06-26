## Description: <br>
Transcribe audio via OpenAI Audio Transcriptions API (Whisper). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to transcribe local audio files through OpenAI's audio transcription API and save the transcript as text or JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The selected audio file is uploaded to OpenAI for transcription. <br>
Mitigation: Use only audio files approved for processing by OpenAI and avoid files containing sensitive data unless that use is authorized. <br>
Risk: The skill requires OPENAI_API_KEY for API access. <br>
Mitigation: Keep the API key secret, provide it through the environment or approved local configuration, and rotate it if exposure is suspected. <br>
Risk: A writable file selected with --out can be overwritten. <br>
Mitigation: Choose the output path deliberately and check for existing files before running transcription. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/steipete/openai-whisper-api) <br>
- [Publisher profile](https://clawhub.ai/user/steipete) <br>
- [OpenAI speech-to-text documentation](https://platform.openai.com/docs/guides/speech-to-text) <br>
- [OpenAI audio transcriptions endpoint](https://api.openai.com/v1/audio/transcriptions) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration] <br>
**Output Format:** [Plain text transcript or JSON written to a local file, with the output path printed to stdout.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and OPENAI_API_KEY; default model is whisper-1; optional language, prompt, output path, and JSON response flags are supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
