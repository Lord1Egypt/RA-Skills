## Description:

TheSportsDB (thesportsdb.com). Use this skill for ANY TheSportsDB request — searching and reading data. Whenever a task involves TheSportsDB, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search and read sports data from TheSportsDB, including schedules, live scores, catalogs, and entity details, through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, setup instructions invoke an external installer whose behavior has not been verified and do not clearly require approval.

Mitigation: Review and verify the CLI separately, and require approval before installation.

Risk: The hosted connector implementation is unverified, and OOMOL handles connected-service credentials and may charge for requests.

Mitigation: Review the OOMOL connection and billing arrangements before use, and disable any unwanted agent-skill synchronization.

## Reference(s):

- [TheSportsDB](https://www.thesportsdb.com/)
- [TheSportsDB API documentation](https://www.thesportsdb.com/documentation)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON connector results summarized as natural-language answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on TheSportsDB coverage; entity search requires a Premium API key.]

## Skill Version(s):

1.0.2 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
