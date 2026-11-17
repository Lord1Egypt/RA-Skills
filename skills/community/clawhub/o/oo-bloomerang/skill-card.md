## Description:

Search, list, and read Bloomerang constituent and household records through the connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and fundraising teams can retrieve Bloomerang constituent and household information by ID, list, or text search. The skill is intended for read-only lookups through an already connected Bloomerang account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs unverified downloads and may add persistent agent skills; remote installer and service behavior have not been verified.

Mitigation: Review and approve CLI installation separately using an inspected, pinned release. Consider setting OO_SKILLS_SYNC_DISABLED=1 to prevent startup skill synchronization, as documented in the command reference.

Risk: Constituent data is accessed through an OOMOL-connected account.

Mitigation: Confirm that OOMOL's data handling is acceptable and grant only the account access needed for the lookup tasks.

## Reference(s):

- [Bloomerang homepage](https://bloomerang.com/)
- [Bloomerang REST API documentation](https://bloomerang.com/api/rest-api)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-bloomerang)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Structured Bloomerang lookup results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only constituent and household records; results depend on the connected account's access.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
