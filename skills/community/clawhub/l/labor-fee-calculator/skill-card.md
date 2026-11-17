## Description:

劳动法费用计算路由技能，根据用户问题自动分发到补偿金/赔偿金计算、加班工资计算、未休年休假补偿计算、工伤赔偿计算等子技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolalam](https://clawhub.ai/user/coolalam)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and practitioners use this skill to estimate Chinese labor-law related payments for termination compensation, damages, overtime pay, unused annual leave, and work-injury compensation. The skill routes each scenario to a focused calculator and produces structured calculation details, legal basis notes, and practical caveats.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Caller-controlled output_path values can cause generated Excel files to be written outside the intended working area.

Mitigation: Run the skill with a low-privilege account and restrict export paths to a dedicated output directory.

Risk: Caller-controlled @file payload paths can cause the calculators to read unintended local payload files.

Mitigation: Only allow trusted payload files and review any file path arguments before execution.

Risk: Configured policy API calls may transmit API credentials and a persistent session ID to policy endpoints.

Mitigation: Keep config.json API keys narrowly scoped and use only trusted policy API URLs.

Risk: Untrusted environment variables can redirect policy API requests to unintended endpoints.

Mitigation: Do not allow untrusted users to set policy API URL environment variables in the runtime environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coolalam/skills/labor-fee-calculator)
- [Compensation and damages formulas](artifact/compensation-damages-calculator/references/formulas.md)
- [Overtime pay formulas](artifact/overtime-pay-calculator/references/formulas.md)
- [Unused annual leave formulas](artifact/unused-annual-leave-calculator/references/formulas.md)
- [Unused annual leave law articles](artifact/unused-annual-leave-calculator/references/law_articles.md)
- [Work-injury compensation formulas](artifact/work-injury-compensation-calculator/references/formulas.md)
- [Work-injury retirement age reference](artifact/work-injury-compensation-calculator/references/retirement_age.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown with calculation tables, legal basis notes, optional shell commands, and optional generated Excel files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call bundled Python calculators and configured policy APIs; Excel output is only produced when the user explicitly requests export.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
