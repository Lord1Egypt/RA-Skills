## Description:

Helps users read, create, and update Ortto contact records through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers can retrieve Ortto contacts by ID, list and filter people, and create or update people through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute downloaded code without separate approval or clear limits on local changes; exact installer effects remain unverified.

Mitigation: Review and approve CLI installation separately, preferably using a verified release. Check or disable bundled-skill synchronization before use, confirm acceptance of OOMOL handling Ortto requests and credentials, and retain confirmation for contact changes.

## Reference(s):

- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI source and documentation](https://github.com/oomol-lab/oo-cli)
- [Ortto developer documentation](https://help.ortto.com/developer/latest/)
- [Ortto](https://ortto.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON connector requests and responses with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports contact lookup, listing, and merge operations; merge can create or update contacts.]

## Skill Version(s):

1.0.4 (source: frontmatter; server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
