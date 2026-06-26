## Description: <br>
Local STT with selectable backends - Parakeet (best accuracy) or Whisper (fastest, multilingual). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[araa47](https://clawhub.ai/user/araa47) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to transcribe local audio files through an OpenClaw-compatible CLI. It supports selectable Parakeet and Whisper backends for English-focused accuracy or multilingual transcription. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches listed Python and model dependencies during local execution. <br>
Mitigation: Install it only in environments where uv dependency and model downloads are permitted and reviewed. <br>
Risk: Recognized speech can be posted to a Matrix room when --room-id is used. <br>
Mitigation: Use --room-id only intentionally, configure a limited Matrix token, and avoid sending sensitive recordings to shared rooms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/araa47/local-stt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls] <br>
**Output Format:** [Plain text transcription on stdout; optional Matrix message when --room-id is provided] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg and Python/model dependencies fetched by uv; uses int8 quantization by default unless --no-int8 is set.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
