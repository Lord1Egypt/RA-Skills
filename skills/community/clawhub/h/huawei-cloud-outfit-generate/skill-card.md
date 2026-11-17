## Description:

Generates one outfit suggestion across four clothing categories, with optional style and season filters and Markdown, plain-text, or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents can use this skill to get a complete daily outfit suggestion from the bundled sample wardrobe. Style and season can be selected, and a seed can make the generated suggestion reproducible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The requested style or season may be relaxed if the wardrobe has no strict match.

Mitigation: Check the output for a fallback notice.

Risk: Writing with --output can replace an existing file.

Mitigation: Choose the destination path carefully before writing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wlc-dev/skills/huawei-cloud-outfit-generate)
- [Usage Guide](artifact/references/usage-guide.md)
- [Acceptance Criteria](artifact/references/acceptance-criteria.md)
- [IAM Policies](artifact/references/iam-policies.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown, plain text, or JSON outfit suggestion]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One outfit per invocation; a seed enables reproducible results.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
