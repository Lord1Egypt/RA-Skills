## Description:

Listmonk (listmonk.app). Use this skill for ANY Listmonk request — reading, creating, updating, and deleting data. Whenever a task involves Listmonk, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect and manage Listmonk subscribers, lists, templates, campaigns, and campaign analytics through an OOMOL-connected account. It guides safe use of the available read, write, and destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can automatically execute an unverified remote installer on the user's machine.

Mitigation: Review and explicitly approve the CLI installation; prefer a pinned, integrity-verified release.

Risk: The connected Listmonk account can expose subscriber data and perform changes, deletion, or campaign sending.

Mitigation: Review the exact target and payload before writes or destructive actions, and confirm campaign scheduling or sending before it executes.

## Reference(s):

- [Listmonk homepage](https://listmonk.app)
- [Listmonk API documentation](https://listmonk.app/docs/apis/apis/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-listmonk)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payloads; connector responses are JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector responses depend on the selected action and the connected Listmonk account.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
