## Description:

Browser Use (browser-use.com). Use this skill for ANY Browser Use request — reading, creating, updating, and deleting data. Whenever a task involves Browser Use, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the oo CLI to operate Browser Use through an OOMOL-connected account, including reading information and managing sessions or tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path may execute remote code that has not been verified.

Mitigation: Review and install the oo CLI separately before using the skill; the remote installer contents and resulting release were not verified.

Risk: Startup synchronization can introduce additional agent skills without explaining the changes.

Mitigation: Review any additional skills before allowing them; use OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization.

Risk: Tasks use an OOMOL-connected account and send task payloads to Browser Use.

Mitigation: Use an appropriately scoped account and review each task payload.

## Reference(s):

- [Browser Use](https://browser-use.com)
- [Browser Use Cloud API reference](https://docs.browser-use.com/cloud/api-reference)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes action schemas and task payload guidance; Browser Use actions may read or change account data.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
