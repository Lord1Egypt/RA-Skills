## Description:

Helps agents read ListingGood data, check listing readiness and compliance, prepare listing details, generate marketplace copy, and retrieve task results through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to review listing readiness and compliance, expand product descriptions into listing fields, generate marketplace listing copy, and retrieve task results through a connected ListingGood account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required oo CLI may change skills installed for other agents through startup synchronization.

Mitigation: Review and install the CLI separately. Set OO_SKILLS_SYNC_DISABLED=1 before invoking oo when you do not want cross-agent skill synchronization.

Risk: Listing requests pass through OOMOL, and generating listing copy spends account credits.

Mitigation: Review the submitted listing details and confirm the credit-bearing generation action before running it.

## Reference(s):

- [ListingGood developer documentation](https://listinggood.com/developers)
- [ListingGood](https://listinggood.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-listinggood)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Listing checks and task results as text or JSON, including generated listing copy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Listing generation uses account credits and saves copy in ListingGood; it does not publish to Amazon.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
