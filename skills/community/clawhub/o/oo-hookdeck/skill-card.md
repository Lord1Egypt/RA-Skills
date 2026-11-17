## Description:

Hookdeck (hookdeck.com). Use this skill for ANY Hookdeck request — reading, creating, updating, and deleting data. Whenever a task involves Hookdeck, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Hookdeck users can use the skill to inspect, create, update, and delete Hookdeck connections, sources, and destinations through an OOMOL-connected account. It provides commands for checking action schemas and sending JSON payloads, with explicit approval steps for writes and deletions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup can install or update additional agent skills, and the remote installer and hosted connector were not verified end to end.

Mitigation: Review the CLI installation and any skill synchronization before proceeding; disable synchronization if it is unwanted.

Risk: Write and delete actions change Hookdeck state.

Mitigation: Review the exact payload and effect and get user approval before writes; confirm the target and get explicit approval before deletions.

## Reference(s):

- [Hookdeck API documentation](https://hookdeck.com/docs/api)
- [Hookdeck](https://hookdeck.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-hookdeck)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands invoke Hookdeck actions; users supply action names and JSON payloads when needed.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
