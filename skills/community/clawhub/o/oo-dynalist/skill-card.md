## Description:

Dynalist (dynalist.io). Use this skill for ANY Dynalist request — reading, creating, updating, and deleting data. Whenever a task involves Dynalist, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected Dynalist account can list and read documents, check for updates, manage inbox preferences, and create, edit, move, or delete Dynalist content through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup directs the user to execute a remote CLI installer whose contents are unverified.

Mitigation: Review and approve CLI installation separately; prefer a pinned, verified release.

Risk: Write and destructive actions can change or remove Dynalist content.

Mitigation: Keep the documented confirmation step for the exact write payload or destructive target and effect.

## Reference(s):

- [Dynalist](https://dynalist.io/)
- [Dynalist API Documentation](https://apidocs.dynalist.io/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Dynalist data and JSON responses, with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
