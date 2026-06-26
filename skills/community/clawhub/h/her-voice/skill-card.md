## Description: <br>
Give your agent a voice. Use when the user wants the agent to speak, read aloud, or have voice responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matusvojtek](https://clawhub.ai/user/matusvojtek) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use Her Voice to add local text-to-speech responses, streamed spoken output, optional WAV export, and configurable voice behavior to an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup may download third-party TTS packages and models. <br>
Mitigation: Review the setup steps and install only in an environment where those downloads are acceptable. <br>
Risk: The optional local daemon uses significant RAM and keeps local socket and PID files under ~/.her-voice. <br>
Mitigation: Run the daemon only when low-latency speech is needed, check its status, and stop it when not in use. <br>
Risk: The visualizer and text-to-speech inputs may process user-provided text. <br>
Mitigation: Do not paste passwords, tokens, or other secrets into the visualizer or speech input. <br>
Risk: The uninstall command removes all Her Voice local data. <br>
Mitigation: Review the uninstall command before running it and back up any configuration or generated files that should be kept. <br>


## Reference(s): <br>
- [Her Voice on ClawHub](https://clawhub.ai/matusvojtek/her-voice) <br>
- [Publisher profile](https://clawhub.ai/user/matusvojtek) <br>


## Skill Output: <br>
**Output Type(s):** [Audio, Files, Shell commands, Configuration] <br>
**Output Format:** [Spoken audio, optional WAV files, JSON configuration, and Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally, may download TTS packages and models during setup, and can use an optional local daemon for lower-latency speech.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and CHANGELOG.md, released 2026-02-15) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
