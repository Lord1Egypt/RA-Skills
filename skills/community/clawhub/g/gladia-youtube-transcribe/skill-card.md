## Description:

Transcribe speech from YouTube videos or audio URLs into text using Gladia API with up to 10 free hours of monthly transcription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kanfred](https://clawhub.ai/user/kanfred)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to submit public YouTube, audio, or video URLs to Gladia and receive transcript text for downstream review or summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media URLs and resulting transcription data are sent to Gladia under the user's account.

Mitigation: Use the skill only for public or approved media, avoid private or sensitive content, and confirm Gladia handling requirements before use.

Risk: GLADIA_API_KEY could be exposed if stored in shell startup files or committed configuration.

Mitigation: Keep the API key session-only or in a secrets manager, and do not include it in documentation, repositories, or shared logs.

Risk: Untrusted URLs may be submitted before stronger URL validation and safe JSON encoding are added.

Mitigation: Review URLs before execution and prefer trusted, publicly accessible media sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kanfred/skills/gladia-youtube-transcribe)
- [Gladia](https://gladia.io)
- [Gladia Dashboard](https://app.gladia.io)
- [Gladia usage API](https://api.gladia.io/v2/usage)
- [Gladia pre-recorded transcription API](https://api.gladia.io/v2/pre-recorded)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text transcript output with Markdown usage guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GLADIA_API_KEY, curl, and python3; transcript output can be printed to stdout or written to a caller-provided file.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
