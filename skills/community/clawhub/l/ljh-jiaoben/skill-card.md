## Description:

Reviews e-commerce selling scripts against a seven-step persuasion chain and flags missing steps, weak conversion logic, and sales claims without matching visuals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[handsomeng](https://clawhub.ai/user/handsomeng)

### License/Terms of Use:

MIT-0

## Use Case:

Content-commerce operators, marketers, and script reviewers use this skill to diagnose full selling scripts before filming or publishing. It focuses on structure, visual-message pairing, and revision priorities rather than writing the script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may show promotional onboarding and point users toward external contact channels.

Mitigation: Review the onboarding text before deployment and disclose or remove promotional contact routing in managed environments.

Risk: The skill may create a hidden onboarding file in the user's home directory.

Mitigation: Run it only where persistent local state is permitted, or disable onboarding writes before installation.

Risk: The skill may store review conclusions and full deliverables in a local ljh-档案 folder.

Mitigation: Avoid confidential sales scripts or brand strategy unless local retention is approved; clear generated archives after review when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/handsomeng/skills/ljh-jiaoben)
- [ClawHub publisher profile](https://clawhub.ai/user/handsomeng)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review report with tables and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
