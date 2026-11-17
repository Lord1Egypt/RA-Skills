## Description:

Search and read DataCite DOI metadata through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers can retrieve a DOI record or search DataCite metadata through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded code without a separate approval step.

Mitigation: Review and verify a pinned CLI installation before enabling the skill, and require approval for setup changes.

Risk: The CLI may automatically synchronize bundled skills.

Mitigation: Review or disable the CLI's automatic bundled-skill synchronization.

Risk: DataCite access is governed by the connected API key's permissions.

Mitigation: Use a DataCite key limited to the records you intend to access through OOMOL.

Risk: Remote installer contents and server-side credential protections were not verified.

Mitigation: Review the installer and credential handling before enabling the skill.

## Reference(s):

- [DataCite API documentation](https://support.datacite.org/docs/api)
- [DataCite](https://datacite.org/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [DataCite skill release](https://clawhub.ai/oomol/skills/oo-datacite)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON request payloads and DataCite metadata responses, with shell commands and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only DOI retrieval and search actions]

## Skill Version(s):

1.0.4 (source: frontmatter; server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
