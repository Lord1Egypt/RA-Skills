## Description:

Give your agent a voice. Use when the user wants the agent to speak, read aloud, or have voice responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matusvojtek](https://clawhub.ai/user/matusvojtek)

### License/Terms of Use:


## Use Case:

Developers and agent users use Her Voice to add local text-to-speech responses, save spoken output, configure voices, and optionally run a warm TTS daemon and macOS visualizer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may download mutable third-party packages and model assets.

Mitigation: Review setup actions before installation and install only in environments where these downloads are acceptable.

Risk: The local daemon uses substantial memory and exposes local voice generation through a background service.

Mitigation: Enable the daemon only when low-latency voice output is needed, and stop it when not in use.

Risk: Persist mode can turn clipboard text into speech.

Mitigation: Use persist mode only when clipboard-to-speech behavior is intended.

Risk: A configurable model value may create code execution risk on Apple Silicon until the scanner-identified interpolation issue is fixed.

Mitigation: Do not set a custom model value on Apple Silicon before that issue is remediated.

Risk: Uninstall removes local Her Voice data.

Mitigation: Run uninstall commands only after explicit user confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/matusvojtek/skills/her-voice)
- [Skill documentation](artifact/SKILL.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Audio, Shell commands, Configuration, Guidance]

**Output Format:** [Spoken audio, WAV files, and Markdown/text instructions with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally, can use an optional background TTS daemon, and requires local setup dependencies including python3 and espeak-ng.]

## Skill Version(s):

1.0.2 (source: server release metadata and CHANGELOG, released 2026-02-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
