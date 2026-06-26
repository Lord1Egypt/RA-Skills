## Description: <br>
Set up mlx-whisper as the local audio transcription engine for OpenClaw on Apple Silicon Macs (M1/M2/M3/M4), automatically transcribing Telegram or WhatsApp voice notes before the agent processes them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YinghaoJia](https://clawhub.ai/user/YinghaoJia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure local speech-to-text for voice notes on Apple Silicon Macs without an API key. It is intended for Telegram or WhatsApp audio workflows where transcripts are passed into the agent conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram or WhatsApp voice notes may contain sensitive personal or business information that becomes visible as transcript text in the agent conversation. <br>
Mitigation: Use the skill only where users accept local download, local transcription, and transcript injection into the conversation; review transcript handling policies before deployment. <br>
Risk: The first setup requires internet access to download the speech model. <br>
Mitigation: Perform the initial model download on a trusted network, then rely on cached local model files for offline operation where appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YinghaoJia/jimmy-claw-mlx-whisper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance for a local transcription command; transcribed voice note content becomes text in the agent conversation.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
