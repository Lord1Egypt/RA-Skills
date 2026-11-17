## Description:

Search and read Interzoid data through the OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Interzoid for company and name matching, email enrichment, IP profiles, remaining credits, and organization name standardization through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote CLI installer has not been inspected, and the security review does not establish its safety.

Mitigation: Review and install a verified CLI release before enabling the skill, and inspect any changes it makes to other agent skills.

Risk: Interzoid requests may involve personal or confidential information.

Mitigation: Connect only the intended account and submit such values only when authorized to share them with OOMOL and Interzoid.

## Reference(s):

- [Interzoid](https://www.interzoid.com/)
- [Interzoid API documentation](https://docs.interzoid.com/)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Interzoid on ClawHub](https://clawhub.ai/oomol/skills/oo-interzoid)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action results with concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Interzoid action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
