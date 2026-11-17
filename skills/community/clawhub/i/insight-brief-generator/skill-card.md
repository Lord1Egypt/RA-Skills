## Description:

Generates management-level insight briefs from reports and charts, separating findings, explanations, recommended actions, data gaps, and risk alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external analysts, and developers use this skill to turn chart conclusions, data summaries, and business questions into reviewable Markdown briefs for weekly updates, operating reviews, and management summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local Python helper can read user-provided files or directories and write requested report outputs.

Mitigation: Point the skill only at intended input files or constrained directories, prefer stdout or dry-run review for sensitive work, and avoid broad private repositories unless the script and spec have been reviewed.

Risk: Security evidence flags under-disclosed directory, pattern, CSV, and skill-audit modes that exceed the main briefing description.

Mitigation: Review the helper script and resource specification before enabling audit-style modes, and keep usage limited to the structured brief workflow unless those modes are explicitly desired.

Risk: Briefs can mislead decision-makers if correlations are presented as causes or if missing context is filled in as fact.

Mitigation: Require the output to label facts, inferences, data gaps, and review-needed items, and have a domain reviewer confirm conclusions before acting on recommendations.

Risk: Input reports or charts may contain personal, confidential, or regulated information.

Mitigation: Redact or minimize sensitive fields before use and keep generated drafts within the intended review workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/insight-brief-generator)
- [Publisher Profile](https://clawhub.ai/user/52yuanchangxing)
- [README](README.md)
- [Output Template](resources/template.md)
- [Structured Brief Specification](resources/spec.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown brief or JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a requested local report file; uses local input only and does not fetch facts from the network.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
