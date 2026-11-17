## Description:

Use this skill to search and read vulnerability data from OSV (osv.dev).

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to retrieve an OSV record by vulnerability identifier or find known vulnerabilities affecting a package or version.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, setup may run a downloaded installer without clear user approval; the external installers and CLI implementation were not audited.

Mitigation: Install a reviewed, pinned CLI release yourself and require approval before downloaded code runs. Consider whether routing package queries through OOMOL and its billing model suits your needs.

## Reference(s):

- [OSV](https://osv.dev)
- [OSV API documentation](https://google.github.io/osv.dev/api/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [OSV vulnerability data and findings in text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content varies by vulnerability identifier or package query.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
