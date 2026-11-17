## Description:

Make outbound phone calls via ElevenLabs voice agent and Twilio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[humanjesse](https://clawhub.ai/user/humanjesse)

### License/Terms of Use:


## Use Case:

External users or agents use this skill to place explicitly approved outbound US phone calls through an ElevenLabs voice agent backed by Twilio. It is intended for call, dial, ring, or phone-call requests after confirming the normalized recipient number.

### Deployment Geography for Use:

Global, with current artifact behavior limited to US E.164 phone numbers.

## Known Risks and Mitigations:

Risk: Outbound calls are real third-party actions that can contact recipients and transmit optional message or context data.

Mitigation: Require explicit user confirmation of the normalized phone number before every call and avoid passing secrets or unnecessary personal data in message or context fields.

Risk: The skill depends on ElevenLabs credentials and phone configuration.

Mitigation: Use a limited ElevenLabs key where possible and configure ELEVENLABS_API_KEY, ELEVENLABS_AGENT_ID, and ELEVENLABS_PHONE_NUMBER_ID only in the execution environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/humanjesse/skills/outbound-call)
- [Publisher profile](https://clawhub.ai/user/humanjesse)
- [Source code and setup guide](https://github.com/humanjesse/hostinger-openclaw-guides)
- [ElevenLabs outbound call API endpoint](https://api.elevenlabs.io/v1/convai/twilio/outbound-call)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell command examples; the call script returns JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ELEVENLABS_API_KEY, ELEVENLABS_AGENT_ID, and ELEVENLABS_PHONE_NUMBER_ID; requires explicit user confirmation before calls.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
