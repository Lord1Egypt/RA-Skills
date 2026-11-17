## Description:

Transcribes Telegram voice messages with Groq Whisper and sends the recognized text to a Groq chat model for a concise Russian-language response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iosif2321](https://clawhub.ai/user/iosif2321)

### License/Terms of Use:


## Use Case:

Developers and Telegram bot operators use this skill to turn incoming Telegram voice messages into text and generate a short Russian-language assistant reply.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram voice audio and transcripts are processed through Groq services.

Mitigation: Document third-party data handling and obtain appropriate user consent before deployment.

Risk: The security evidence reports a hard-coded Groq credential fallback.

Mitigation: Remove the embedded credential, rotate it, and require GROQ_API_KEY to be supplied from a secure environment variable.

Risk: The dependency declaration does not pin an exact Groq SDK version.

Mitigation: Pin and review dependencies before installing the skill in a production environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iosif2321/skills/groq-voice-transcriber)
- [Publisher profile](https://clawhub.ai/user/iosif2321)

## Skill Output:

**Output Type(s):** [text, API Calls, guidance]

**Output Format:** [String]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns either the generated assistant response or a Russian-language error string.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and artifact config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
