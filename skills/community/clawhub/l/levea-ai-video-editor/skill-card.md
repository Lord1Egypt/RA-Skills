## Description:

Plan, execute, and verify timeline video edits through the autonomous_edit MCP tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brajendrak00068](https://clawhub.ai/user/brajendrak00068)

### License/Terms of Use:

MIT-0

## Use Case:

Video editors and creators use this skill to describe timeline edits in plain language, then review and export edited video projects with captions, titles, reframing, color, and audio changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media is processed by Levea's cloud editing service.

Mitigation: Use media you are comfortable sharing with Levea.

Risk: An exposed API key could grant access to the editing service account.

Mitigation: Protect the API key in the plugin or MCP server configuration.

Risk: An edit plan may not match the user's intent.

Mitigation: Enable requirePlanApproval to review plans before execution.

## Reference(s):

- [Levea account and API key setup](https://livecore.ai/?openclaw=1&utm_source=clawhub&utm_medium=skill&utm_campaign=levea-ai-video-editor)

## Skill Output:

**Output Type(s):** [Video, Text, Guidance]

**Output Format:** [Rendered MP4 video, project status, and verification report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return an MP4 URL and asynchronous render job status.]

## Skill Version(s):

1.0.32 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
