## Description:

学习娃 LearnWa turns a parent or educator's request into a parent-controlled, single-file Chinese HTML math teaching aid for make-ten, break-ten, and level-ten methods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lwter](https://clawhub.ai/user/lwter)

### License/Terms of Use:

MIT-0

## Use Case:

Parents, educators, and external users use this skill to generate localized Chinese interactive math lessons for early primary learners. The skill focuses on parent-operated lessons where children observe, reason aloud, and answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated files can overwrite existing documents if the user chooses an important output path.

Mitigation: Review the output path before running generation and write lessons to a normal workspace or dedicated output folder.

Risk: Custom SVG themes could introduce unsafe or non-static markup if an agent ignores the skill constraints.

Mitigation: Keep custom SVGs static and inline, avoid scripts, event handlers, JavaScript URLs, and external links, and review generated HTML before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lwter/skills/neway-learnwa)
- [Examples](references/examples.md)
- [FAQ](references/faq.md)
- [Lesson block format](references/lesson-block-format.md)
- [Math rules](references/math-rules.md)
- [Themes](references/themes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Lesson block JSON and shell commands that generate a single-file HTML teaching page]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for local generation and review before delivery.]

## Skill Version(s):

1.0.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
