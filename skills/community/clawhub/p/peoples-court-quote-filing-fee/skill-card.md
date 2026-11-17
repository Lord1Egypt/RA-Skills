## Description:

Quotes the People's Court filing fee for a claim amount using its live quote tool when connected or the published fee schedule otherwise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shunhe-wang](https://clawhub.ai/user/shunhe-wang)

### License/Terms of Use:

MIT-0

## Use Case:

External users ask what it costs to file a People's Court arbitration claim. The skill returns a live quote when connected or an estimate based on the published fee schedule.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live quote uses the cases:read permission, which also covers existing case information.

Mitigation: Review the account permissions before connecting; use the fallback estimate if you prefer not to connect an account.

Risk: A fee calculated from the published schedule may differ from the exact fee shown before payment.

Mitigation: Label schedule-based results as estimates and direct users to the current fee schedule or a live quote for the exact amount.

## Reference(s):

- [People's Court connector documentation](https://peoplescourt.ai/docs/api/connectors)
- [People's Court published fee schedule](https://peoplescourt.ai/pricing)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text fee quote or estimate with procedure details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live quotes are reported as returned; schedule-based calculations are identified as estimates.]

## Skill Version(s):

1.0.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
