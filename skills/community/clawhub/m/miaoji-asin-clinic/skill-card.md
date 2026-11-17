## Description:

Miaoji Asin Clinic helps Amazon sellers diagnose listing health across compliance, advertising, reviews, visuals, and content, then prioritize repair actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and ecommerce operators use this skill to generate a five-dimension ASIN health report, identify the highest-priority listing issues, and receive guided repair templates for related specialist skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review-analysis inputs can include customer names, order information, private seller notes, support records, or other sensitive customer data.

Mitigation: Paste only the minimum public review text needed and remove sensitive customer or seller data before using review-analysis templates.

Risk: The skill can estimate listing health when complete marketplace data is unavailable, so recommendations may be incomplete or imprecise.

Mitigation: Cross-check scores and repair priorities against Amazon account data, current listing performance, and applicable marketplace policy before acting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangm-a3/skills/miaoji-asin-clinic)
- [README](artifact/README.md)
- [ASIN Diagnosis Matrix](artifact/references/diagnosis-matrix.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown diagnostic reports and repair guidance; JSON health analysis from the local scoring script when used directly.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include estimated scores when seller data is incomplete; users should verify recommendations against current marketplace and account data.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
