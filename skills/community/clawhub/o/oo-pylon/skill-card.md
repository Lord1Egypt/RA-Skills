## Description:

Access Pylon through an OOMOL-connected account to read, search, create, and update support data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support teams use this skill to retrieve and manage Pylon accounts, contacts, issues, and issue messages through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI dependency may add persistent instructions to other agents without clearly disclosing that effect.

Mitigation: Review the CLI's broader effects, use a verified release, and set OO_SKILLS_SYNC_DISABLED=1 before first use if Pylon access is all you need. Review OOMOL's access to Pylon data and retain confirmation for write actions.

## Reference(s):

- [Pylon API documentation](https://docs.usepylon.com/pylon-docs/developer/api)
- [Pylon](https://www.usepylon.com)
- [oo CLI documentation and source](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Text responses and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
