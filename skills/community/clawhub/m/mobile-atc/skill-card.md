## Description:

Diagnose mobile PDP and cart friction where the add-to-cart control is hard to see or reach by simulating scroll paths and thumb zones, flagging text-stacked dead zones and tap blind spots, and proposing minimal UI refactors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

External commerce teams, developers, and conversion specialists use this skill to diagnose mobile product-detail-page add-to-cart visibility problems, especially when mobile conversion trails desktop or the primary CTA is buried below dense content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Illustrative visibility scores or simulated scroll paths may be mistaken for measurements from real user behavior.

Mitigation: Label simulations clearly and validate recommendations with screenshots, breakpoint testing, analytics, or usability evidence before making production changes.

Risk: The skill could be treated as a substitute for formal accessibility or legal review.

Mitigation: Use it for UX triage only and route accessibility compliance or legal claims through qualified reviewers.

Risk: Mobile conversion data, product performance, or customer behavior details may be commercially sensitive.

Mitigation: Share only the funnel and layout details needed for analysis, and anonymize or aggregate sensitive business data where possible.

## Reference(s):

- [Mobile ATC visibility playbook](references/mobile_atc_playbook.md)
- [ClawHub skill page](https://clawhub.ai/rijoyai/skills/mobile-atc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown analysis with scoring, recommendations, tables, and simulated scroll-path notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include illustrative scores when screenshots or URLs are unavailable; simulations should be labeled as simulated.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
