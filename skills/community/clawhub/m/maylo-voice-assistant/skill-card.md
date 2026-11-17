## Description:

Maylo Voice Assistant installs and runs an offline-first macOS voice assistant with wake-word listening, VAD recording, local Whisper transcription, OpenClaw responses, offline macOS text-to-speech, and an HTTPS WebSocket web UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugurozer84](https://clawhub.ai/user/ugurozer84)

### License/Terms of Use:


## Use Case:

Developers and Mac users use this skill to install, run, and troubleshoot a local voice assistant that can listen for a wake word, transcribe Turkish speech locally, send the transcript to a local OpenClaw agent, and speak the reply through macOS audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default web UI can expose microphone, transcript, and local-agent controls without authentication when bound to 0.0.0.0.

Mitigation: Bind the web UI to 127.0.0.1 or a trusted private tunnel by default, and add authentication before allowing LAN access.

Risk: The assistant records audio and stores WAV files, transcripts, and logs locally.

Mitigation: Review retained recordings and logs, define a local retention policy, and avoid using the assistant where sensitive audio should not be stored.

Risk: Voice transcripts are passed to a local OpenClaw agent that may perform local-agent actions.

Mitigation: Restrict the OpenClaw agent permissions available to the assistant and review agent behavior before deployment.

## Reference(s):

- [Maylo Voice Assistant ClawHub listing](https://clawhub.ai/ugurozer84/skills/maylo-voice-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and bundled Python, shell, and HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local setup and operating guidance for a macOS voice assistant; the bundled app writes local recordings, transcripts, logs, bridge request files, and bridge response files during use.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
