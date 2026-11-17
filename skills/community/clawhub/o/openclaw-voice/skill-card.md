## Description:

OpenClaw Voice is a CLI-oriented skill for managing voice conversation sessions, transcripts, ElevenLabs voice profiles, searchable history, backups, and Markdown interchange summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frank-bot07](https://clawhub.ai/user/frank-bot07)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to track voice-oriented conversations, manage transcript history and voice profiles, and publish concise Markdown context for other agents in an OpenClaw workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice conversation transcripts, summaries, and profile descriptions can contain sensitive personal or business information retained in local storage.

Mitigation: Avoid entering secrets or sensitive data, and review or delete the SQLite database, backups, and generated interchange files according to the workspace retention policy.

Risk: User-controlled conversation summaries and profile descriptions may be published as Markdown that other agents can read.

Mitigation: Treat generated Markdown as untrusted context and review it before allowing other agents to rely on it.

Risk: Future phone-calling behavior would add real-time communications, external service credentials, and higher privacy impact.

Mitigation: Require a separate security and privacy review before enabling any phone-calling implementation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frank-bot07/skills/openclaw-voice)
- [README.md](artifact/README.md)
- [VOICE_CALLING_SPEC.md](artifact/VOICE_CALLING_SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Command-line text and generated Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local SQLite data, backups, and agent-readable Markdown interchange files.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
