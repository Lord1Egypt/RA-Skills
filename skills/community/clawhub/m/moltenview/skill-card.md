## Description:

Push persistent visual views (charts, metrics, lists, progress bars) to MoltenView Mac app when agent output benefits from visual display that persists outside chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goldcote](https://clawhub.ai/user/goldcote)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to push structured dashboards, charts, metrics, progress indicators, links, and images into the MoltenView Mac app for persistent visual reference outside chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Data sent to MoltenView may remain visible after the chat response is gone.

Mitigation: Use the skill only for information appropriate for persistent local display, and clear or replace views when they should no longer be shown.

Risk: The skill depends on the local MoltenView Mac app and its Unix socket being available.

Mitigation: Confirm MoltenView is running and use the socket path shown in the app settings before sending view payloads.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/goldcote/skills/moltenview)
- [MoltenView Homepage](https://moltenrock.com)
- [MoltenView App Store Listing](https://apps.apple.com/app/molten-view/id6742515562)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to send structured view payloads to a local MoltenView socket; displayed views may persist until cleared or replaced.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
