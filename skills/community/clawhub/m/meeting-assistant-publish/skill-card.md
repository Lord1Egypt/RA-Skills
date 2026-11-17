## Description:

AI Meeting Assistant for Jitsi Meet and Google Meet. Joins calls, transcribes with diarization, interacts via duplex voice, and generates structured minutes through your own self-hosted MCP gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafacpti23](https://clawhub.ai/user/rafacpti23)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and meeting operators use this skill to have an agent join approved Jitsi Meet or Google Meet calls, capture live discussion with speaker attribution, participate by voice when configured, and generate structured meeting minutes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can join live meetings and capture audio, chat, and transcripts without evidence of built-in consent safeguards.

Mitigation: Use it only for meetings where bot participation is permitted, notify participants before capture begins, and prefer explicit prompts that name the specific meeting URL and desired mode.

Risk: Meeting audio, chat, and transcripts may be sent to the configured gateway and AI providers.

Mitigation: Confirm organizational data-handling approval for the gateway and providers before use, and avoid sending sensitive meetings unless those services are approved for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rafacpti23/skills/meeting-assistant-publish)
- [Jitsi Meet](https://meet.jit.si)
- [Google Meet](https://meet.google.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and YAML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces meeting setup guidance, gateway tool usage instructions, live transcript retrieval guidance, and structured meeting-minute content.]

## Skill Version(s):

1.0.1 (source: server release evidence and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
