## Description: <br>
Offline-first voice assistant stack for macOS with wake word detection, VAD recording, local Whisper ASR, OpenClaw agent response, offline macOS text-to-speech, and an HTTPS WebSocket web UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugurozer84](https://clawhub.ai/user/ugurozer84) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to install, run, and troubleshoot a local macOS voice assistant that can listen for a wake word, transcribe speech locally, route requests to an OpenClaw agent, speak replies, and expose a web microphone interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The web UI can accept or trigger audio processing without built-in authentication when exposed on a network. <br>
Mitigation: Bind the UI to localhost or a trusted interface, add authentication before using 0.0.0.0, and expose it only on trusted networks. <br>
Risk: The assistant listens through the Mac microphone and can save audio and log artifacts locally. <br>
Mitigation: Install only on a trusted machine, review stored recordings and logs, and avoid placing secrets or private keys in the skill directory. <br>
Risk: Spoken or streamed audio becomes input to the configured local OpenClaw agent. <br>
Mitigation: Review the OpenClaw agent's permissions and behavior before enabling the assistant, especially in shared or sensitive environments. <br>
Risk: Web-started wake listening can begin background microphone processing unexpectedly. <br>
Mitigation: Disable MAYLO_WEB_WAKE unless web-started wake listening is explicitly required. <br>


## Reference(s): <br>
- [Maylo Voice Assistant on ClawHub](https://clawhub.ai/ugurozer84/maylo-voice-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup, run, and troubleshooting guidance for a local macOS voice assistant and its bundled app files.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
