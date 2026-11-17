## Description:

Payroll Data Audit audits payroll spreadsheets with deterministic Python rules aligned to an SOP, producing data scans, rule results, reports, issue views, sampling checks, and delivery summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

Payroll, HR operations, and finance reviewers use this skill to check payroll exports for field completeness, formula consistency, business-rule failures, red/yellow/blue risk signals, month-over-month changes, and policy exceptions before payroll approval or follow-up review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive payroll data and includes cloud delivery behavior plus generated sample outputs and Feishu links.

Mitigation: Review before installation; remove generated sample outputs and cloud links, and require explicit opt-in confirmation of destination and recipients before any Feishu delivery.

Risk: The delivery script executes lark-cli through shell-form subprocess commands.

Mitigation: Change delivery execution to argument-based subprocess calls before using the skill with real payroll data.

Risk: HTML and report outputs may include payroll-derived fields.

Mitigation: Escape payroll-derived values in generated HTML and reports before sharing or deploying the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tuobadaidai/skills/payroll-data-audit)
- [Publisher Profile](https://clawhub.ai/user/tuobadaidai)
- [Rules Reference](artifact/references/rules.json)
- [Skill Source](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, HTML, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local audit artifacts such as data-scan JSON, audit-result JSON, Markdown and HTML reports, issue lists, sampling verification output, and delivery summaries.]

## Skill Version(s):

7.4.1 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
