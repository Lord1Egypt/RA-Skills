## Description:

Popeye Analysis helps agents analyze user-provided data, compare decisions, and diagnose problems using Chinese-language structured prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangtaoid](https://clawhub.ai/user/jiangtaoid)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to guide Chinese-language analysis of pasted business data, compare options for decisions, and diagnose root causes for described problems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Chinese trigger phrases can activate in ambiguous conversation and produce decision or diagnostic guidance without enough context.

Mitigation: Ask for confirmation and missing context before applying the analysis, decision, or diagnosis templates.

Risk: Outputs may contain incorrect or misleading analysis if user-provided data or problem descriptions are incomplete.

Mitigation: Review conclusions against the provided data and treat recommendations as decision support rather than authoritative advice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiangtaoid/skills/popeye-analysis)
- [Data Analysis Module](artifact/modules/data.md)
- [Decision Support Module](artifact/modules/decision.md)
- [Problem Diagnosis Module](artifact/modules/diagnosis.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with structured headings and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language responses tailored to user-provided data, decisions, or problem descriptions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
