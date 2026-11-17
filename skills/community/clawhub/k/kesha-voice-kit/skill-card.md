## Description:

Kesha Voice Kit lets agents transcribe audio, synthesize speech, perform speaker diarization, and detect language locally through a CLI or MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drakulavich](https://clawhub.ai/user/drakulavich)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add local voice-message transcription, text-to-speech voice-note generation, language detection, and MCP or OpenClaw audio workflows without cloud speech APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path uses mutable remote and global installers with broad local code execution authority.

Mitigation: Review install commands before execution, prefer package-manager or pinned installation methods, avoid piping remote installers directly into a shell, and run the tool as a normal non-admin user.

Risk: Installation persists a global CLI plus model assets and can change OpenClaw audio or TTS behavior.

Mitigation: Preview planned downloads with installation plan commands, verify OpenClaw audio and TTS configuration after install, and keep the CLI route explicit in user configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drakulavich/skills/kesha-voice-kit)
- [npm package](https://www.npmjs.com/package/@drakulavich/kesha-voice-kit)
- [Bun runtime](https://bun.sh)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing guidance may direct local CLI calls that produce transcripts, timestamped JSON, language metadata, or generated audio files.]

## Skill Version(s):

1.6.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
