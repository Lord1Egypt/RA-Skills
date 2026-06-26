## Description: <br>
Audio transcription and text-to-speech generation using OpenRouter API for transcribing audio files to text or generating speech/audio from text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odubinkin](https://clawhub.ai/user/odubinkin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to transcribe selected local audio files and generate speech audio through OpenRouter-backed models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files, prompts, and text-to-speech content are sent to OpenRouter and routed providers. <br>
Mitigation: Use the skill only for content acceptable for provider processing, avoid highly sensitive audio unless approved, and use a constrained OpenRouter API key where possible. <br>
Risk: Generated audio files are saved locally and may persist after use. <br>
Mitigation: Review generated file paths before keeping or sharing outputs and remove generated files when they are no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files] <br>
**Output Format:** [Plain text transcripts or JSON containing generated audio paths, transcript, and output format] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated audio is written to the OpenClaw workspace tmp directory when available, or to an explicit output path.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
