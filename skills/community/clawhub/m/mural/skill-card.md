## Description:

Mural API integration with managed OAuth for collaborative whiteboard automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect Mural through ClawLink OAuth, browse workspaces, rooms, murals, widgets, templates, and tags, and create sticky notes when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and enables an external ClawLink plugin.

Mitigation: Install only when the ClawLink plugin source is trusted, and pin or verify the plugin release where OpenClaw deployment supports it.

Risk: Mural OAuth grants access according to the authenticated user's account permissions.

Mitigation: Review the Mural permissions during OAuth connection and reconnect only from the documented ClawLink dashboard.

Risk: The sticky-note creation tool can modify mural content.

Mitigation: Confirm sticky-note creation requests before execution and check target mural IDs and note contents.

## Reference(s):

- [Mural API Docs](https://developers.mural.co/public/docs)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=mural)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/mural)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with shell commands and JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OAuth setup, Mural discovery workflows, read operations, and confirmed sticky-note write operations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
