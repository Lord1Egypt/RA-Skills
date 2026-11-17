## Description:

Search and read Moxie data using an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can search and read client, contact, and project records, and list configured pipeline or task stages in their connected Moxie workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may run an unverified remote installer without a separate approval step and can install additional agent skills.

Mitigation: Require approval before setup, review a pinned CLI release before installing, and check whether installing additional skills is acceptable.

## Reference(s):

- [Moxie](https://www.withmoxie.com/)
- [Moxie public API fundamentals](https://help.withmoxie.com/en/articles/8154735-public-api-fundamentals)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Moxie skill release](https://clawhub.ai/oomol/skills/oo-moxie)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON results with concise text summaries]

**Output Parameters:** [Varies by selected search or list action.]

**Other Properties Related to Output:** [Read-only workspace data; available fields depend on the records returned.]

## Skill Version(s):

1.0.4 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
