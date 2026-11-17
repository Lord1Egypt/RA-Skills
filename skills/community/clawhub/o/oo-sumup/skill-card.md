## Description:

Operate on SumUp customer and checkout data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing a SumUp account can use this skill to retrieve checkout and customer information, create customers or checkouts, update customer details, and deactivate pending checkouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unchecked software and introduce broader, persistent agent changes.

Mitigation: Review and approve CLI installation separately, verify the software source, and disable automatic skill synchronization before use.

Risk: Creating or updating customers and deactivating checkouts can change SumUp account data.

Mitigation: Review the exact action, target, and payload, and retain the skill's confirmation requirements for changes and deactivation.

Risk: Connecting SumUp entrusts OOMOL with account access.

Mitigation: Review the account connection before use and connect only the intended SumUp account.

## Reference(s):

- [SumUp](https://www.sumup.com)
- [SumUp API documentation](https://developer.sumup.com/api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, JSON, Guidance, Shell commands]

**Output Format:** [Guidance with oo CLI commands and JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the connected SumUp account; state-changing actions require confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
