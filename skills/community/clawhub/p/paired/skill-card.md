## Description:

Connects an OpenClaw agent to the user's own phone for messaging, calls, contacts, media and file controls, and optional local voice synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nj070574-gif](https://clawhub.ai/user/nj070574-gif)

### License/Terms of Use:

MIT-0

## Use Case:

People using OpenClaw with a Linux host and their own paired phone can check phone status, manage messages and calls, control media, transfer files, and optionally synthesize speech in their own voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent services can monitor messages and calls or dispatch phone actions.

Mitigation: Keep services disabled until reviewed; use the signed inbox hook rather than the deprecated session-log command hook.

Risk: SMS and call authority can contact unintended recipients.

Mitigation: Keep the trusted-numbers list small and confirm high-impact actions before execution.

Risk: A stored phone PIN and integration credentials can expose device access or private data.

Mitigation: Avoid storing a PIN unless automatic unlock is needed, and restrict access to PIN, Telegram, Gemini, inbox-key, and voice files.

Risk: Automated SMS responses can send message content to an external service.

Mitigation: Enable respond_local_only when SMS content must remain on the local machine.

## Reference(s):

- [Paired: Phone Agent release](https://clawhub.ai/nj070574-gif/skills/paired)
- [Voice setup guide](artifact/docs/VOICE-SETUP.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON results, Guidance]

**Output Format:** [Conversational responses with shell commands and structured phone-status results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands can act on the user's phone, including sending SMS and placing calls.]

## Skill Version(s):

2.4.1 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
