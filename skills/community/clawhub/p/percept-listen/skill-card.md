## Description:

Captures ambient audio from wearable devices, transcribes it locally, and streams searchable, speaker-tagged conversation data to an OpenClaw agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarvis563](https://clawhub.ai/user/jarvis563)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to connect an Omi pendant or Apple Watch audio source to an agent for local transcription, searchable conversation context, and live transcript access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambient recording can capture sensitive conversations or people who have not consented.

Mitigation: Use only where all recorded participants have been informed as required by law and where ambient capture is appropriate.

Risk: Transcript webhooks and tunnel endpoints can expose sensitive conversation data if reachable without access controls.

Mitigation: Protect the webhook with authentication, private tunnel access controls, or equivalent network restrictions before use.

Risk: Local transcripts and searchable conversation records can retain sensitive data longer than intended.

Mitigation: Define retention and deletion practices for transcript files, SQLite data, and conversation exports before deployment.

Risk: Installing the Percept dependency without version control can increase supply-chain and behavior-change risk.

Mitigation: Install Percept in an isolated environment with a pinned trusted version.

## Reference(s):

- [Percept Listen on ClawHub](https://clawhub.ai/jarvis563/skills/percept-listen)
- [Percept GitHub Repository](https://github.com/GetPercept/percept)
- [Percept Docs](https://github.com/GetPercept/percept/docs)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or reference local transcript text, searchable conversation records, and local data paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
