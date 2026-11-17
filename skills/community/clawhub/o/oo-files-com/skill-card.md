## Description:

Files.com (files.com). Use this skill for ANY Files.com request — reading, creating, updating, and deleting data. Whenever a task involves Files.com, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Files.com users can use this skill to list, inspect, download, create, and update Files.com resources through their connected account. It also explains setup and authentication recovery when an action reports a connection problem.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup executes remote installer code that was not verified.

Mitigation: Review and pin a specific oo CLI version before installing it.

Risk: The CLI can synchronize changes to skills installed for other agents.

Mitigation: Review that behavior and use OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization when needed.

Risk: Files.com write and delete actions can change or remove user data.

Mitigation: Use a restricted API key and confirm the exact target and effect before running each write or delete action.

## Reference(s):

- [Files.com REST API documentation](https://developers.files.com/rest/)
- [Files.com](https://www.files.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action schemas should be checked before calls; writes and deletes require confirmation of their exact effects.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
