## Description: <br>
Local speech-to-text with the Whisper CLI (no API key). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other users use this skill to run local Whisper CLI transcription or translation for audio files without sending audio to an API service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transcripts can contain private, medical, legal, or third-party speech. <br>
Mitigation: Keep transcript output local unless there is consent and a separate approved upload process. <br>
Risk: Audio from sensitive system paths or other users' directories may contain private recordings. <br>
Mitigation: Confirm authorization and consent before transcribing files from sensitive paths such as /etc/, /var/log/, or another user's home directory. <br>
Risk: Using translation mode when a verbatim transcript is required can change the intended output. <br>
Mitigation: Avoid --task translate when the user needs a faithful transcript in the source language. <br>
Risk: Using the Whisper Python API expands the execution surface beyond the skill's stated scope. <br>
Mitigation: Use the whisper CLI commands described by the skill instead of import whisper workflows. <br>


## Reference(s): <br>
- [OpenAI Whisper](https://openai.com/research/whisper) <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/openai-whisper-hardened) <br>
- [Safety evaluation](SAFETY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is scoped to local Whisper CLI usage and local transcript handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
