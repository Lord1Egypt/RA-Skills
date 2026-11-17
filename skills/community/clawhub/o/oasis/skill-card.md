## Description:

Enables an agent to work inside Oasis 3D worlds by placing catalog objects, crafting procedural scenes, painting ground tiles, moving avatars, taking screenshots, and using Forge text-to-3D conjuration through the Oasis MCP tool surface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parzival-moksha](https://clawhub.ai/user/parzival-moksha)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent that is already connected to Oasis so it can inspect, modify, navigate, and visually verify local 3D worlds through the Oasis MCP tool surface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent can edit local Oasis worlds, including removing objects, clearing worlds, loading other worlds, or deleting conjured assets.

Mitigation: Ask for explicit confirmation and use backups or snapshots before destructive world-management or asset-deletion actions when the world contains work the user cares about.

Risk: The agent may misdescribe the current 3D world if browser screenshot capture is unavailable or stale.

Mitigation: Use Oasis screenshot tools for visual verification when visibility matters, and tell the user when the live browser client or screenshot bridge is unavailable.

## Reference(s):

- [Oasis setup and onboarding docs](https://parzival-moksha.github.io/oasis/)
- [Oasis quickstart](https://parzival-moksha.github.io/oasis/docs/getting-started/quickstart/)
- [Oasis repository](https://github.com/Parzival-Moksha/oasis)
- [ClawHub skill page](https://clawhub.ai/parzival-moksha/skills/oasis)

## Skill Output:

**Output Type(s):** [guidance, text, code, API calls]

**Output Format:** [Markdown guidance with JSON-style Oasis MCP tool call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Oasis MCP tool calls that inspect or mutate a user's local Oasis world; screenshot outputs depend on a live Oasis browser client.]

## Skill Version(s):

0.4.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
