## Description:

Use RealPhoneValidation to validate phone numbers and retrieve caller-enrichment data when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support teams use the skill to validate 10-digit phone numbers and retrieve caller-enrichment fields when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute downloaded code that has not been verified.

Mitigation: Review and approve CLI installation separately, using a verified release.

Risk: Automatic startup synchronization can make unexplained changes to other agents’ skills.

Mitigation: Review the synchronization behavior before first use; set OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization.

Risk: Phone numbers are sent to OOMOL and RealPhoneValidation, and usage may incur charges.

Mitigation: Submit only phone numbers you intend to share and check applicable usage costs.

## Reference(s):

- [RealPhoneValidation API documentation](https://realphonevalidation.com/api-documentation/active-api/)
- [RealPhoneValidation](https://realphonevalidation.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON validation results with concise action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Caller-enrichment fields are included when available.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
