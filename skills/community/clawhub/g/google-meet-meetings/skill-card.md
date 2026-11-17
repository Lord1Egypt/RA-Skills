## Description:

Google Meet API integration with managed OAuth for creating meeting spaces, inspecting conference records, retrieving recordings and transcripts, and managing meeting participants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to connect a Google account through ClawLink, manage Google Meet spaces and conference records, and retrieve meeting artifacts such as recordings, transcripts, and participant sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the skill requires trusting a third-party ClawLink plugin with access to Google Meet data available to the connected Google account.

Mitigation: Install only from a trusted ClawHub source, review the Google OAuth consent screen during setup, and revoke the Google connection or remove the plugin if access is no longer needed.

Risk: Create, update, and end-meeting operations can change or terminate active Google Meet resources.

Mitigation: Confirm the target resource and intended effect before any write action, and preview tool calls when available before execution.

Risk: Recordings and transcripts can contain sensitive meeting content and may be unavailable due to organizer or domain policy.

Mitigation: Retrieve meeting artifacts only for authorized users and communicate when empty results may reflect policy restrictions or delayed processing.

## Reference(s):

- [Google Meet API Overview](https://developers.google.com/meet/rest/reference)
- [Google Meet Conference Records](https://developers.google.com/meet/rest/reference/v1/conferenceRecords)
- [Google Meet Spaces](https://developers.google.com/meet/rest/reference/v1/spaces)
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/google-meet-meetings)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, text]

**Output Format:** [Markdown with inline shell commands and JSON tool-call parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Google Meet resource identifiers, meeting URIs, transcript text, recording metadata, participant data, and setup or troubleshooting steps.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
