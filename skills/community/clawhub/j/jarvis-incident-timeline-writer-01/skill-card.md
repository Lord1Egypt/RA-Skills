## Description:

Create precise incident timelines from logs and notes. Use when handling development work that needs repeatable steps, quality gates, and practical outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xammarie](https://clawhub.ai/user/xammarie)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to convert logs, notes, constraints, and task artifacts into evidence-backed incident timelines, ranked findings, action plans, risks, mitigations, and checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce broad development plans rather than only incident chronology, which may cause over-activation or outputs that are less specific than an incident timeline workflow requires.

Mitigation: Use it with prompts and review criteria that explicitly request incident chronology, evidence sources, timestamps, assumptions, and acceptance checks.

Risk: Generated findings, commands, or checklists could be incomplete or misleading if the supplied logs and notes are incomplete.

Mitigation: Review the output against the source artifacts before executing commands or assigning owners and deadlines.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with concise summaries, ranked findings, action plans, risk mitigations, and exact checklists or commands where useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Situation summary is capped at 5 lines by the skill artifact.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
