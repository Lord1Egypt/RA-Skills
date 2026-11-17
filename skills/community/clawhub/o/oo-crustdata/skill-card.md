## Description:

Search Crustdata and retrieve company information through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business researchers use this skill to search Crustdata, resolve company identifiers, and retrieve company enrichment data through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, setup guidance can run a downloaded installer without separate approval or integrity verification.

Mitigation: Review and install the CLI separately before agent use, and require approval for any later installation attempt.

Risk: The OOMOL connection handles Crustdata access and query payloads.

Mitigation: Understand that OOMOL handles the connected account access and payloads before using the skill.

## Reference(s):

- [Crustdata API documentation](https://docs.crustdata.com/openapi-specs/2025-11-01/introduction)
- [Crustdata](https://crustdata.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured company data with concise textual summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Company search, identification, autocomplete, and enrichment results; company search supports cursor pagination.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
