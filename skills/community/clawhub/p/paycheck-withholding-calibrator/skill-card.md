## Description:

W-4 feedback loop from one paystub — projects the tax-year federal liability (2026-shaped brackets, standard deduction, child credits), compares it to your withholding trajectory, and names the outcome in dollars (a big refund is an interest-free loan to the IRS; a big owe risks Form 2210 penalties). Checks the 90%/100%/110% safe harbors and prints the exact W-4 fix — the per-paycheck number for Step 4(c) extra withholding or the Step 3 credit adjustment — to land on your target refund.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Wage earners use this skill to estimate their year-end federal income tax and withholding from paystub figures, then review possible W-4 adjustments and underpayment safe-harbor status.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: A reported calculation limitation could make a suggested midyear withholding adjustment fall short of its target.

Mitigation: Check the calculation and suggested W-4 change against current IRS tables before relying on it, especially for a midyear adjustment.

## Reference(s):

- [Withholding model reference](references/withholding-model.md)
- [ClawHub release page](https://clawhub.ai/voronindenis5/skills/paycheck-withholding-calibrator)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text]

**Output Format:** [Console text with a tax projection, withholding assessment, and suggested W-4 adjustments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Federal income tax estimates only; excludes state, local, and FICA taxes and includes a reminder to verify current IRS tables.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
