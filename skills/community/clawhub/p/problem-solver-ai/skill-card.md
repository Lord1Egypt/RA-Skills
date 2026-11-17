## Description:

A structured problem-solving assistant that helps users break down technical, personal, business, and creative problems with frameworks such as 5 Whys, decision matrix, SWOT, Eisenhower prioritization, brainstorming, and step-by-step action plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkpareek0315](https://clawhub.ai/user/mkpareek0315)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to structure open-ended problems, compare options, identify root causes, prioritize tasks, and turn decisions into action plans. It also supports local problem history and saved solutions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation phrases can cause the skill to engage during many everyday problem-solving conversations.

Mitigation: Review when the skill activates and disable it for conversations where structured problem-solving is not desired.

Risk: Problem history and saved solutions may contain sensitive personal, business, or customer information stored locally in plaintext.

Mitigation: Avoid entering secrets or highly sensitive data, and regularly review, clear, or disable the local history files under ~/.openclaw/problem-solver.

## Reference(s):

- [Problem Solver Skill Page](https://clawhub.ai/mkpareek0315/skills/problem-solver-ai)
- [Publisher Profile](https://clawhub.ai/user/mkpareek0315)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown with structured prompts, tables, checklists, JSON examples, and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update local JSON files under ~/.openclaw/problem-solver for settings, history, and saved solutions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
