## Description: <br>
Local speech-to-text using OpenAI Whisper. Runs fully offline after model download. High quality transcription with multiple model sizes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users use this skill to transcribe local audio files with OpenAI Whisper, choosing model size, language detection, timestamps, and JSON output as needed. It is intended for local speech-to-text workflows where transcripts should remain on the user's machine after the initial model download. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency installation from an unapproved package index can introduce compromised packages. <br>
Mitigation: Install only the documented packages from default PyPI and the PyTorch CPU index URL shown in the artifact. <br>
Risk: Transcription output may contain adversarial text or commands that should not be treated as executable instructions. <br>
Mitigation: Review transcript text as untrusted data and do not pipe, redirect, eval, execute, or source it. <br>
Risk: Transcripts can contain sensitive spoken information. <br>
Mitigation: Keep transcription output local unless a user deliberately handles any later transfer outside the skill workflow. <br>
Risk: Large Whisper models can require substantial downloads and local resources. <br>
Mitigation: Choose model size deliberately and disclose larger model choices before starting downloads or transcription. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/snazar-faberlens/local-whisper-hardened) <br>
- [Faberlens safety evaluation](https://faberlens.ai/explore/local-whisper) <br>
- [Artifact safety notes](SAFETY.md) <br>
- [PyTorch CPU package index](https://download.pytorch.org/whl/cpu) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text transcript or JSON transcription payload, with Markdown guidance and shell commands when setup or invocation help is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON output can include detected language, transcript text, segments, and word timestamps when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
