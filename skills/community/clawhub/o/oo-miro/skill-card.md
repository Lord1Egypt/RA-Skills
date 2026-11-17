## Description:

Use this skill to read, create, update, and delete data in Miro.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use it to inspect Miro boards and items, create or update board content, and remove connectors or items through the connected Miro account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup uses remote installers, and the hosted implementation was not verified.

Mitigation: Review the setup, use a separately reviewed version-pinned CLI, and check automatic skill synchronization; use OO_SKILLS_SYNC_DISABLED as an available control.

Risk: Write and destructive actions can change or remove Miro board content.

Mitigation: Connect only the intended Miro account, confirm the exact payload and effect before writes, and require explicit approval for deletion targets.

## Reference(s):

- [Miro API documentation](https://developers.miro.com/reference/api-reference)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Miro](https://miro.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and JSON action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and deletions require user approval; action schemas should be checked before constructing payloads.]

## Skill Version(s):

1.0.6 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
