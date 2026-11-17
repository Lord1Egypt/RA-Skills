## Description:

Meta Academic Translation guides agents through academic translation workflows with added self-verification, reflection, and learning loops for bilingual academic outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate academic papers while preserving citations, formulas, tables, terminology, and bilingual review artifacts. It also asks the agent to perform self-checks and record lessons from translation runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to retain user-derived preferences and notes across sessions.

Mitigation: Permit persistent learning only when users explicitly opt in and can inspect or delete learned_patterns.json.

Risk: The skill describes rewriting its own instructions after repeated errors or usage.

Mitigation: Require human review before any change to SKILL.md or other instruction files is applied.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qq435912743/skills/meta-academic-translation)
- [Distillation Report](artifact/distillation_report.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with optional generated files and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce bilingual translation artifacts, self-check notes, HTML guidance, and learned-pattern records when permitted.]

## Skill Version(s):

1.0.0 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
