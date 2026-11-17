## Description:

G.workspace registers OpenClaw slash commands and agent tools that proxy Discord server file-space actions to a local G.workspace REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luojingwei123](https://clawhub.ai/user/luojingwei123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to add shared file management, search, version history, upload links, trash management, member listing, and annotation task workflows to Discord servers through OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace and annotation task mutations could be invoked by users or tools without clear authorization boundaries.

Mitigation: Deploy only where the G.workspace service enforces guild, user, and role authorization, and restrict access to the slash commands and AI tools.

Risk: Permanent trash emptying can delete workspace files without an explicit confirmation and admin-only guard.

Mitigation: Keep permanent trash emptying disabled or tightly restricted until confirmation and admin-only controls are reviewed.

Risk: The plugin depends on a local G.workspace service that performs the underlying file-space operations.

Mitigation: Pin that service to a reviewed commit and operate it in a controlled OpenClaw/Discord environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luojingwei123/skills/gworkspace)
- [ClawHub Publisher Profile](https://clawhub.ai/user/luojingwei123)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Configuration]

**Output Format:** [Discord/OpenClaw command responses and JSON tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the configured local G.workspace service and the active Discord guild or workspace state.]

## Skill Version(s):

3.2.1 (source: evidence.json release.version and artifact/plugin/package.json; artifact/_meta.json lists 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
