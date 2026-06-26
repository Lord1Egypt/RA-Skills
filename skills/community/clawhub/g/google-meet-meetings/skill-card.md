## Description: <br>
Google Meet API integration with managed OAuth for creating meeting spaces, inspecting conference records, retrieving recordings and transcripts, and managing meeting participants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an OpenClaw agent to Google Meet through ClawLink, then create meeting spaces, inspect conference records, retrieve recordings and transcripts, and manage participants with confirmation before write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide write operations that create or update Google Meet spaces or end an active conference. <br>
Mitigation: Preview and confirm the target resource and intended effect before any write action, and require explicit confirmation before ending an active conference. <br>
Risk: The skill depends on OAuth-connected Google account access and may surface meeting recordings, transcripts, or participant data. <br>
Mitigation: Use normal ClawLink credential controls, verify the connected account, and limit requests to meeting resources the user is authorized to access. <br>
Risk: Recordings and transcripts may be unavailable because of organizer or domain policies, processing delay, or missing meeting configuration. <br>
Mitigation: Report unavailable artifacts as such, retry after a short delay when processing may still be pending, and avoid inventing missing meeting outputs. <br>


## Reference(s): <br>
- [Google Meet API Overview](https://developers.google.com/meet/rest/reference) <br>
- [Google Meet Conference Records](https://developers.google.com/meet/rest/reference/v1/conferenceRecords) <br>
- [Google Meet Spaces](https://developers.google.com/meet/rest/reference/v1/spaces) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/google-meet-meetings) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent through ClawLink discovery, preview, confirmation, and execution workflows for Google Meet tools.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
