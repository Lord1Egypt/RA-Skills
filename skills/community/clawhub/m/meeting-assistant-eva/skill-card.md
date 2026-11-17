## Description:

Meeting Assistant lets an agent join supported online meetings, monitor chat and transcripts, answer participant questions, and produce meeting notes or summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeron-g](https://clawhub.ai/user/zeron-g)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and meeting participants use this skill to run an AI meeting assistant that can join a meeting, monitor conversation, respond through meeting chat, capture transcripts, and generate summaries. It also includes a medical assistant mode for consultation support where appropriate privacy and compliance controls are in place.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled reusable-looking credentials or tokens may expose meeting services or external APIs.

Mitigation: Replace all bundled tokens and secrets before installation, rotate any values that may have been used, and keep credentials in environment-specific secret storage.

Risk: Meeting services exposed broadly can allow unintended access to bot controls, transcripts, chats, or recordings.

Mitigation: Bind services to localhost or an isolated Docker network and restrict access to trusted operators.

Risk: Recordings, screenshots, transcripts, summaries, and Docker volumes can contain sensitive personal or business information.

Mitigation: Obtain participant consent and define retention, encryption, storage, and deletion rules before running the assistant.

Risk: Automatic chat replies can send inappropriate, inaccurate, or sensitive responses into live meetings.

Mitigation: Disable or review automatic replies for sensitive meetings and require human review where mistakes would have material impact.

Risk: Medical assistant mode may process protected health information or be mistaken for clinical advice.

Mitigation: Use medical mode only in environments with appropriate privacy and compliance controls, and keep outputs informational rather than a substitute for professional judgment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zeron-g/skills/meeting-assistant-eva)
- [Publisher Profile](https://clawhub.ai/user/zeron-g)
- [Developer Documentation](docs/README.md)
- [Setup Guide](docs/setup.md)
- [Agent Usage Guide](docs/agent-usage.md)
- [API Reference](docs/api-reference.md)
- [Architecture](docs/architecture.md)
- [Troubleshooting Guide](docs/troubleshooting.md)
- [Integration Guide](references/integration-guide.md)
- [Medical Terms Guide](references/medical-terms-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Meeting chat responses, transcript text, JSON logs, Markdown summaries, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local recordings, screenshots, transcript logs, suggestion logs, and meeting summaries during operation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
