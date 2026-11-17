## Description:

Omnicast is a local Node.js media pipeline that turns text, URLs, audio, and video into podcast scripts, synthesized audio, cover art, social media copy, and video assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaudata](https://clawhub.ai/user/kaudata)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, developers, and media teams use Omnicast locally to ingest source media, draft a two-host podcast script, synthesize audio, generate cover art, package LinkedIn assets, and optionally upload a private draft to YouTube.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded files, URLs, transcripts, scripts, and generated media can be sent to external AI providers or YouTube.

Mitigation: Avoid sensitive or regulated content unless those provider transfers are approved, and use limited or disposable API keys where practical.

Risk: The local web service has security concerns when handling untrusted URLs or files.

Mitigation: Keep the service bound to localhost, do not expose its port beyond the local machine, and update vulnerable dependencies before relying on it with untrusted inputs.

Risk: The YouTube integration can upload generated video as a private draft after Google sign-in.

Mitigation: Review the title, description, account, and privacy settings before upload, and use the narrowest practical Google access token.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaudata/skills/omnicast)
- [Publisher Profile](https://clawhub.ai/user/kaudata)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Local web application outputs including plain text, audio files, image files, captions, MP4 video, ZIP archives, and status JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 20 or newer, FFmpeg, GEMINI_API_KEY, OPENAI_API_KEY, and optional provider credentials for ElevenLabs or YouTube upload.]

## Skill Version(s):

1.0.14 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
