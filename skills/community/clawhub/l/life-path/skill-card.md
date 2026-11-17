## Description:

A life-reflection assistant that uses Confucius's six-stage life framework to help users interpret life stages, assess their current stage, produce personalized action guidance, compare related life-stage theories, and generate an interactive HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill for guided life-stage reflection, Confucian six-stage interpretation, personal stage assessment, action planning, quotation lookup, cross-cultural theory comparison, and optional HTML report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may collect personal life-stage reflections and self-assessment details for generated guidance or reports.

Mitigation: Tell users before collecting or saving reflective details, minimize sensitive input, and review generated reports before sharing them.

Risk: Generated HTML reports may include user-provided text, which can be unsafe if untrusted markup is inserted without escaping or sanitization.

Mitigation: Escape or sanitize dynamic user text before inserting it into HTML and avoid opening reports built from untrusted pasted markup.

Risk: Life-planning guidance can be mistaken for professional counseling or mental-health advice.

Mitigation: Frame outputs as reflective guidance, encourage independent judgment, and direct users to qualified professionals for clinical, legal, financial, or crisis needs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/life-path)
- [Life Wisdom Reference](references/life_wisdom.md)
- [Six Stages Reference](references/six_stages.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown responses with optional generated HTML report content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May incorporate user-provided life-stage reflections and self-assessment details into generated guidance or a local HTML report.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
