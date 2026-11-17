## Description:

Operate NeverBounce to verify individual email addresses and manage bulk verification jobs through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to verify individual email addresses, create and manage bulk verification jobs, and retrieve account and job results through their connected NeverBounce account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified downloads, and the documented safety rules classify job-changing actions as reads.

Mitigation: Review setup before installing; use a reviewed CLI installation with automatic skill synchronization disabled, inspect the action schema, and explicitly approve job-changing actions including parsing.

Risk: Email data is processed by OOMOL and NeverBounce, and bulk processing may incur costs.

Mitigation: Submit only email data intended for processing and confirm processing costs before running jobs.

## Reference(s):

- [NeverBounce skill release](https://clawhub.ai/oomol/skills/oo-neverbounce)
- [NeverBounce API documentation](https://developers.neverbounce.com/docs/api-getting-started)
- [NeverBounce](https://neverbounce.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, CSV, Verification and job status information]

**Output Format:** [JSON action responses and CSV bulk job results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-address verification results, account summaries, and paginated or filtered bulk job results.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
