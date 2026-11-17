## Description:

Poper (poper.ai). Use this skill for ANY Poper request — searching and reading data. Whenever a task involves Poper, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents use this skill to list popups and read the responses collected by Poper through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions can execute downloaded CLI code and may introduce broader persistent agent changes; the installer and hosted connector implementation are unverified.

Mitigation: Review and approve CLI installation separately, check its bundled-skill installation and synchronization behavior, and limit Poper access to the account data needed for the task.

## Reference(s):

- [Poper](https://www.poper.ai)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Poper popup and response data returned as JSON, with text summaries or guidance when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only listing of popup and response data]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
