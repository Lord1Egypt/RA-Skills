## Description:

Make AI-powered outbound phone calls using ElevenLabs voice, GPT, and Twilio, with one-way prerecorded messages or live two-way conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omerflo](https://clawhub.ai/user/omerflo)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to place AI-voiced outbound calls, leave voice messages, schedule calls, or conduct short interactive phone conversations for tasks such as reservations and appointments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real phone calls and consume paid Twilio, OpenAI, and ElevenLabs resources.

Mitigation: Require explicit per-call confirmation, verify recipients and consent, and monitor account spend before execution.

Risk: Interactive call webhooks may be exposed through a public tunnel without Twilio signature validation.

Mitigation: Add Twilio request signature validation, restrict accepted call SIDs, and limit tunnel exposure before operational use.

Risk: One-way call audio may be uploaded to public temporary hosting.

Mitigation: Avoid sensitive content in hosted audio, prefer controlled storage, and define retention and deletion procedures.

Risk: Generated audio and call transcripts may be written to temporary local files.

Mitigation: Apply cleanup, access controls, and data retention rules for temporary audio and transcript files.

Risk: Call summaries may be forwarded through iMessage.

Mitigation: Confirm the destination number and avoid sending sensitive summaries unless the communication channel is approved.

## Reference(s):

- [ElevenLabs Voice Reference](references/voices.md)
- [Phone Caller ClawHub Skill Page](https://clawhub.ai/omerflo/skills/phone-caller)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands, environment variable guidance, and concise operational notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate real outbound calls through Twilio and generate call audio or summaries when executed with credentials.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
