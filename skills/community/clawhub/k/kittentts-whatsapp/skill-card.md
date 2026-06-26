## Description: <br>
Converts KittenTTS speech output into WhatsApp-compatible OGG Opus voice notes and optionally transcribes incoming WhatsApp audio with Whisper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lakshibro](https://clawhub.ai/user/lakshibro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to generate WhatsApp-ready voice note files from text with KittenTTS and to optionally transcribe incoming WhatsApp audio during voice-to-voice workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted TTS input, voice names, or speed values may lead to local Python code execution. <br>
Mitigation: Run the skill only in an isolated environment and pass untrusted values through safe argument, environment, or JSON handling before using external WhatsApp content. <br>
Risk: Setup commands install system packages and use --break-system-packages. <br>
Mitigation: Review install commands before running them, prefer a container or virtual environment, and avoid these commands on managed systems unless approved. <br>
Risk: Fixed temporary audio paths can expose or overwrite local audio data. <br>
Mitigation: Use private mktemp directories for all intermediate audio files and clean up temporary WAV files after conversion or transcription. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lakshibro/kittentts-whatsapp) <br>
- [KittenML Hugging Face Models](https://huggingface.co/KittenML) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime scripts produce OGG Opus audio files and transcription text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The TTS script writes audio under /tmp/kittentts-walkie and may download a KittenTTS model from Hugging Face on first run.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
