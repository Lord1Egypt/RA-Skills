## Description:

A Douyin Qianchuan advertising diagnostic skill that walks users through a decision tree to identify traffic, spend, GMV, or ROI drop causes and recommend a first action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[handsomeng](https://clawhub.ai/user/handsomeng)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators and advertising practitioners use this skill to diagnose Douyin Qianchuan traffic, spend, GMV, and ROI drops through a step-by-step decision tree and produce an actionable next step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill shows a first-use LJHskill promotion and creates an onboarding marker under the user's home directory.

Mitigation: Review this behavior before installation and remove the marker or promotion flow if it is not acceptable for the deployment environment.

Risk: The skill may read and save brand diagnostic records in the current workspace, which could include sensitive commercial information.

Mitigation: Use it only in a controlled workspace, avoid confidential data unless retention is acceptable, and periodically review or delete generated archive files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/handsomeng/skills/ljh-qianchuan)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, files]

**Output Format:** [Conversational Markdown with diagnostic questions, conclusions, and optional local archive notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a first-use onboarding marker and save brand diagnostic records in the user's workspace.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
