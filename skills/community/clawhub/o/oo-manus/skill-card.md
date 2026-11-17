## Description:

Operate Manus through an OOMOL-connected account to read, create, update, and delete Manus data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage Manus tasks, projects, agents, connectors, and skills through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback may execute a changing remote installer and modify the local environment.

Mitigation: Prefer a separately reviewed, version-pinned CLI installation and require approval before local setup changes.

Risk: Connecting Manus gives OOMOL access to the connected account.

Mitigation: Connect only an account whose access you are willing to entrust to OOMOL.

## Reference(s):

- [Manus](https://manus.im)
- [Manus API documentation](https://open.manus.ai/docs)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Guidance]

**Output Format:** [Markdown guidance with oo CLI commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
