## Description:

Manage pet boarding operations including owner and pet profiles, reservations, daily care logs, and billing for dogs, cats, and other pets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[katherine0325](https://clawhub.ai/user/katherine0325)

### License/Terms of Use:

MIT-0

## Use Case:

Pet boarding providers use this skill to maintain owner and pet records, create reservations, log daily care, calculate fees, and manage billing-related records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store customer contact, pet health, and billing records in predictable local JSON files without explicit privacy safeguards.

Mitigation: Require owner-only file permissions, avoid storing full payment details, minimize medical and contact data, and define retention and deletion practices.

Risk: Operational updates could be applied to the wrong owner, pet, or reservation.

Mitigation: Confirm the correct owner, pet, and reservation identifiers before creating or changing records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/katherine0325/skills/pet-boarding-manager)
- [Publisher profile](https://clawhub.ai/user/katherine0325)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown and structured text with JSON-style records and fee calculations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include owner, pet, reservation, care-log, and billing record details supplied by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
