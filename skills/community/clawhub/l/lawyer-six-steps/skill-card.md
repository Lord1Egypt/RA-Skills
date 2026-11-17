## Description:

中国律师办案六步法，用于按事实梳理、法律分析、法理研究、案例检索、裁判规则和结果预判六个阶段辅助民商事案件分析，并生成案件分析报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[happylawyer](https://clawhub.ai/user/happylawyer)

### License/Terms of Use:

MIT-0

## Use Case:

External legal professionals use this skill to structure Chinese civil and commercial litigation analysis, review elements and evidence, anticipate opposing arguments, and prepare a case analysis report for internal discussion or case-file retention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process confidential Chinese legal matter materials.

Mitigation: Use the explicit /lawyer-six-steps command and avoid providing case materials that are unnecessary for the requested analysis.

Risk: The skill writes a final case analysis report to the workspace, which may persist sensitive matter information.

Mitigation: Confirm the report location before completion and review workspace access and retention expectations before use.

Risk: Legal and case-search outputs may be incomplete or require verification.

Mitigation: Have a qualified lawyer review cited laws, cases, links, and conclusions before relying on the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/happylawyer/skills/lawyer-six-steps)
- [Deep mode operating details](references/deep-mode.md)
- [Output templates](references/output-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Conversational legal analysis with structured Markdown tables and a final Markdown case analysis report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may use web_search for legal and case references, asks for confirmation at key steps, and writes the final report to the workspace.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
