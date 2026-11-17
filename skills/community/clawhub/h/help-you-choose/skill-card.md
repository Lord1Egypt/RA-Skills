## Description:

A Chinese-first decision coaching agent that uses Socratic questioning and structured decision frameworks to help users clarify options, values, risks, and next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stella-ji-shuting](https://clawhub.ai/user/stella-ji-shuting)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for structured life decisions such as career, relationship, relocation, and multi-option choices. It guides users through background collection, values clarification, structured analysis, stress testing, and a decision report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive decision history and profile information may be stored locally.

Mitigation: Ask for explicit consent before saving records, and avoid storing sensitive details unless they are needed for the user's decision workflow.

Risk: Generated decision reports may expose personal decision details if published or shared publicly.

Mitigation: Review and redact report content before publishing, and share public links only when the user explicitly wants the report to be public.

Risk: Generated HTML may be unsafe when labels or titles come from untrusted text.

Mitigation: Treat generated HTML as untrusted, inspect or sanitize untrusted inputs, and avoid opening or sharing reports that contain unreviewed user-provided labels.

## Reference(s):

- [Decision frameworks reference](artifact/references/frameworks.md)
- [ClawHub skill page](https://clawhub.ai/stella-ji-shuting/skills/help-you-choose)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Conversational guidance and Markdown decision reports, with optional HTML visualization files and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first interaction; optional local decision history, profile records, and HTML visualizations when the user consents and provides the needed inputs.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
