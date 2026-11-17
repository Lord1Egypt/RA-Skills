## Description:

Use an OOMOL-connected Kintone account to search and read users, groups, departments, and user services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People with an OOMOL-connected Kintone account can look up users and their assigned departments, groups, and services, or list users, groups, and departments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup runs downloaded code whose contents have not been verified.

Mitigation: Review and approve CLI installation separately before setup; review bundled skill changes and connect only the Kintone account intended for this use.

## Reference(s):

- [Kintone homepage](https://www.kintone.com/)
- [Kintone API documentation](https://kintone.dev/en/docs/kintone/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON responses from Kintone actions with brief usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only lookups and lists; action input fields are determined by the live connector schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
