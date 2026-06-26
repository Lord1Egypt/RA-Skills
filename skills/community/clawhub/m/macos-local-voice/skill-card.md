## Description: <br>
Local STT and TTS on macOS using native Apple capabilities. Speech-to-text via yap (Apple Speech.framework), text-to-speech via say + ffmpeg. Fully offline, no API keys required. Includes voice quality detection and smart voice selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[STRRL](https://clawhub.ai/user/STRRL) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users on macOS use this skill to transcribe local audio, generate speech audio from text, and inspect available macOS voices without API keys or cloud services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio transcripts may appear in stdout and generated speech audio remains on disk. <br>
Mitigation: Avoid highly sensitive content unless that local exposure is acceptable, choose custom output paths deliberately, and remove generated files when they are no longer needed. <br>
Risk: The skill depends on macOS-only commands and Homebrew-installed tools. <br>
Mitigation: Install only on macOS and verify the yap, say, osascript, and optional ffmpeg dependencies before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/STRRL/macos-local-voice) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [yap speech-to-text dependency](https://github.com/finnvoor/yap) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Plain text stdout, file paths, and generated audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [TTS writes audio files locally, using OGG/Opus when ffmpeg is available and AIFF otherwise.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
