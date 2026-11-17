## Description:

Use the OOMOL-connected Tencent Meeting MCP to manage meetings and access recordings, minutes, and transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Tencent Meeting through an OOMOL-connected account can retrieve and search meetings, recordings, minutes, and transcripts, and schedule, update, or cancel meetings and manage recording access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run an unverified remote CLI installer, and synchronization may change other agent skills.

Mitigation: Review and approve CLI installation separately, verify the selected release and synchronization behavior, and disable synchronization if you do not want other skills changed.

Risk: Meeting data passes through OOMOL, while the external installers and service implementation were not verified.

Mitigation: Review OOMOL's data handling and the CLI and service behavior before using sensitive meeting content.

## Reference(s):

- [Tencent Meeting](https://meeting.tencent.com/)
- [Tencent Meeting API documentation](https://meeting.tencent.com/support/topic/2233/index.html)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-tencent-meeting-mcp)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Guidance]

**Output Format:** [Tencent Meeting response data in JSON or text, with Markdown usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may contain meeting details, attendee data, recording URLs, minutes, or transcript text; state-changing actions follow the skill's confirmation safeguards.]

## Skill Version(s):

1.0.2 (source: skill frontmatter; server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
