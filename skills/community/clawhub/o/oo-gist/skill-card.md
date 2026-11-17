## Description:

Gist (gist.github.com). Use this skill for ANY Gist request — reading, creating, updating, and deleting data. Whenever a task involves Gist, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to read and manage GitHub Gists through an OOMOL-connected account. It guides them to inspect each action's schema and obtain approval before making or deleting changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup fallback can execute downloaded CLI installer code without a separate installation approval step; startup synchronization may also install additional skills.

Mitigation: Review the CLI installer before running setup, prefer a reviewed fixed release, confirm OOMOL account permissions, and use OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization if it is not wanted.

## Reference(s):

- [Gist](https://gist.github.com)
- [Gist API documentation](https://developers.getgist.com/api/)
- [oo CLI source](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, API Calls, Shell commands, Guidance]

**Output Format:** [Gist results and action guidance, with shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive actions require user approval; deletion and overwrite actions are destructive.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
