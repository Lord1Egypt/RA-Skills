## Description:

Businessmap (businessmap.io). Use this skill for ANY Businessmap request — reading, creating, updating, and deleting data. Whenever a task involves Businessmap, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to read and manage Businessmap workspaces, boards, and cards through their connected account. It guides the agent to inspect each action's schema and obtain confirmation before changes or destructive operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback downloads and runs an installer whose code was not available for inspection.

Mitigation: Install a verified CLI release independently and require separate approval before future installation changes.

Risk: The connected Businessmap key can be used for actions that change or delete workspace data.

Mitigation: Use a narrowly scoped Businessmap key, confirm write payloads before running them, and explicitly approve destructive actions.

## Reference(s):

- [Businessmap](https://businessmap.io)
- [Businessmap REST API documentation](https://knowledgebase.businessmap.io/hc/en-us/articles/360012393692-Businessmap-REST-API)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON action payloads and Businessmap data responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action payloads are based on the live connector schema.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
