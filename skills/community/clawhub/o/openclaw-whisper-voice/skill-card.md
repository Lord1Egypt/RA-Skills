## Description: <br>
Local Whisper speech-to-text for audio files and inbound voice notes on the OpenClaw Gateway host. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sabyaghosh](https://clawhub.ai/user/sabyaghosh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install a local Whisper transcription path on an OpenClaw Gateway host, then transcribe audio files or configure inbound WhatsApp and Telegram voice notes through a CLI media tool fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer adds user-local Python packages and ~/.local/bin launchers and may download Whisper models on first use. <br>
Mitigation: Review the shell scripts before installation, run them in an isolated or virtual environment when supply-chain controls require it, and plan for model cache storage under ~/.cache/whisper. <br>
Risk: The transcription wrapper processes local audio files that may contain sensitive voice content. <br>
Mitigation: Run transcription only on trusted Gateway hosts with appropriate access controls and avoid sending sensitive audio to unapproved environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sabyaghosh/openclaw-whisper-voice) <br>
- [Publisher profile](https://clawhub.ai/user/sabyaghosh) <br>
- [PyTorch CPU wheel index](https://download.pytorch.org/whl/cpu) <br>
- [pip bootstrap script URL used by installer](https://bootstrap.pypa.io/get-pip.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash commands and JSON5 configuration snippets; transcription output can be txt, srt, vtt, or json.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports Whisper model, language, task, format, and stdout-only options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
