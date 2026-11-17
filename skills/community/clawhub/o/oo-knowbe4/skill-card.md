## Description:

Use the OOMOL-connected KnowBe4 service to search and read KnowBe4 account, group, and user data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

KnowBe4 administrators use this skill to retrieve account and subscription details and to look up or list users and groups through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback executes downloaded code without verification or a clear approval step.

Mitigation: Review and approve CLI installation separately, including any automatic agent-skill changes, and use a verified CLI version.

Risk: The connected service can access requested KnowBe4 data through OOMOL.

Mitigation: Use a least-privilege KnowBe4 connection and account for OOMOL brokering access to requested data.

## Reference(s):

- [KnowBe4](https://www.knowbe4.com)
- [KnowBe4 Reporting API documentation](https://developer.knowbe4.com/rest/reporting/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API data, JSON, Guidance]

**Output Format:** [JSON connector responses with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only account, group, and user information]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
