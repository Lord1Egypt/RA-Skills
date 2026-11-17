## Description:

Guides Chinese-market sales account research by mapping a target company's business lines, likely buying committee, decision influencers, reachable entry points, and evidence-backed first-step sales strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[summerzb](https://clawhub.ai/user/summerzb)

### License/Terms of Use:

MIT-0

## Use Case:

External sales teams and account researchers use this skill when starting work on a named company or project and needing to identify relevant business lines, buying-committee roles, decision influencers, contact paths, and a practical first outreach angle. It is not intended for building net-new prospect lists, standalone business-record lookups, individual profiles, or lead-list scoring.

### Deployment Geography for Use:

China market

## Known Risks and Mitigations:

Risk: The workflow may surface personal contact details or contact paths during sales research.

Mitigation: Use only appropriate public sources or user-authorized accounts, retain source URLs, and review jurisdiction-specific privacy and outreach rules before acting on contact details.

Risk: Auto-detection could route broad sales or account-research prompts into this specialized workflow.

Mitigation: Review trigger behavior before broad enablement and keep use scoped to named-company or named-project account-entry research.

Risk: Outdated or weakly sourced people, role, or phone-number claims can misdirect outreach.

Mitigation: Require source-backed role and contact evidence, use the skill's confidence labels for phone numbers and employment status, and preserve named evidence gaps instead of filling them by inference.

## Reference(s):

- [Decision-chain research method](references/decision-chain.md)
- [Data sources and source substitution](references/data-sources.md)
- [Engineering project branch](references/branch-engineering.md)
- [Delivery report template](references/output-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown research report with tables, source links, contact-path notes, evidence gaps, and recommended next sales action.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public contact paths and source URLs; contact details should be source-verified and labeled with confidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
