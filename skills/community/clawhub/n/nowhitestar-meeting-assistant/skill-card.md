## Description:

Native macOS meeting automation for OpenClaw that detects meetings, prompts before recording, captures system and microphone audio, transcribes locally with whisper-cli, and queues agent-generated meeting notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nowhitestar](https://clawhub.ai/user/nowhitestar)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and individual operators use this skill to automate meeting detection, consent prompts, local recording, transcription, and summary generation on macOS. Developers can also use its scripts and configuration guidance to integrate OpenClaw meeting-note workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests sensitive macOS permissions and installs background services for recording and meeting detection.

Mitigation: Review the package before installation, especially on shared or work machines, and grant Microphone, Screen and System Audio Recording, and Accessibility permissions only when the intended workflow requires them.

Risk: The recording daemon and calendar webhook increase local control and network attack surface.

Mitigation: Restrict the audio daemon socket, authenticate webhook requests, and expose webhook or tunnel services only when they are needed.

Risk: Installer behavior and OAuth handling can expose users to unwanted command execution or retained secrets.

Mitigation: Avoid curl-to-bash installation, remove eval-based setup behavior before deployment, and keep OAuth client secrets, refresh tokens, API keys, and personal calendar IDs out of the skill package.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nowhitestar/skills/nowhitestar-meeting-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, transcript text, and summary Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local recordings and generated meeting notes after the user grants the required macOS permissions and configures local services.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
