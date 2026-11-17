## Description:

Search and read Firstbase data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations teams use this skill to retrieve catalog, brand, category, and inventory information from their connected Firstbase organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The linked CLI setup or execution may make persistent changes to local agent skill directories.

Mitigation: Review and install a verified CLI release before use; consider setting OO_SKILLS_SYNC_DISABLED=1 before invoking the skill.

Risk: The skill accesses data through the connected Firstbase account, and OOMOL intermediates requests.

Mitigation: Connect only the intended Firstbase account with read access.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Firstbase API documentation](https://apipub.firstbasehq.com/swagger-ui/index.html)
- [Firstbase](https://www.firstbase.com)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Structured data, Text summaries, Guidance]

**Output Format:** [JSON responses with concise text summaries and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Firstbase catalog and inventory information]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
