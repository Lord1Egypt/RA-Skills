## Description:

This skill helps users query vehicle ownership transfer history from a VIN, including transfer counts, transfer months, and before/after cities, through a paid Alipay AI payment flow backed by Juhe Data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check a vehicle's historical ownership transfer records before resale, financing, insurance, or other risk-review scenarios. The skill requires a valid VIN and user consent to a paid query before requesting data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow points users to an unpinned npm installer for the Alipay payment dependency.

Mitigation: Review and pin a known version of the payment dependency before use, and run installation in a least-privilege environment.

Risk: The skill sends a VIN to Juhe and initiates a paid query through an external payment skill.

Mitigation: Confirm user consent, payment details, and comfort with sharing the VIN before making the request.

Risk: Vehicle transfer records may be delayed or incomplete and should not be the only basis for a transaction decision.

Mitigation: Present results as reference information and advise users to verify against official vehicle registration records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-vehicle-owner-a2a)
- [Juhe A2A query endpoint](https://apis.juhe.cn/a2a/query)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown tables with structured vehicle transfer summary and record details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs only interface-returned fields, sorts transfer records by changeMonth descending, and appends a reference-only disclaimer.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
