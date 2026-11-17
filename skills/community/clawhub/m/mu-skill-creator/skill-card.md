## Description:

Skill创建与质量门控，含56项10层审计模型。触发词：创建skill、skill创建、skill审计、质量审计。不适用：skill发布、生态体检（用mu-skill-auditor）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[muippt](https://clawhub.ai/user/muippt)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill authors use this skill to create, refactor, and audit agent skills with staged quality gates, trigger-word checks, security checks, and a 56-item review model. It supports local skill handoff preparation, while publishing remains delegated to a dedicated publishing tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit script may inspect more local skills than intended when run without a target or with an overly broad SKILL_BASE.

Mitigation: Run the audit script with explicit skill targets or a carefully chosen SKILL_BASE before reviewing its results.

Risk: Publishing language in public materials may overstate the skill's role.

Mitigation: Use this skill for creation, audit, and handoff preparation only; delegate publishing to the appropriate publishing tool.

Risk: Generated skill edits and audit recommendations can still miss qualitative design issues.

Mitigation: Review proposed changes and use the full 56-item checklist, including human-judgment items, before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/muippt/skills/mu-skill-creator)
- [Project landing page](https://muippt.github.io/mu-skill-creator/)
- [Quality gates reference](references/quality-gates.md)
- [Collaboration guide](references/collaboration-guide.md)
- [Evaluation examples](evals/evals.json)
- [Release notes](https://github.com/muippt/mu-skill-creator/releases)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated skill files, reference documents, shell commands, and audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local, user-directed workflow; audit script output is evidence for a broader human review and is not a standalone approval.]

## Skill Version(s):

3.7.10 (source: server release metadata; artifact frontmatter reports 4.1.9)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
