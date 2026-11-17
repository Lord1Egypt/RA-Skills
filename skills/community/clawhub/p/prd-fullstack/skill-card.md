## Description:

A Chinese-language full-stack PRD workflow that guides users through collaborative product discovery and produces complete product requirements documentation for product, design, development, testing, operations, and project management teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shixiangyu2](https://clawhub.ai/user/shixiangyu2)

### License/Terms of Use:

MIT-0

## Use Case:

External users, product managers, designers, developers, testers, operations teams, and project managers use this skill to turn early product ideas into a structured PRD covering requirements, market analysis, user flows, UI guidance, architecture, testing, operations, and project planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Included local build and versioning scripts may write files unsafely or expose code-injection paths when run with unreviewed inputs.

Mitigation: Review and harden update.sh, generated project scripts, release messages, and version.json filename handling before execution; run scripts only in a trusted project directory.

Risk: The skill generates detailed PRD, architecture, testing, and operations guidance that can become misleading if users accept outputs without domain review.

Mitigation: Have product, engineering, security, testing, and operations stakeholders review generated requirements and plans before using them for implementation or release decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shixiangyu2/skills/prd-fullstack)
- [README](README.md)
- [FullStack PRD workflow design](FULLSTACK_PRD.md)
- [Collaboration workflow reference](COLLABORATION.md)
- [Design system reference](references/design-system.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documentation with tables, Mermaid diagrams, PRD templates, HTML/PDF build outputs, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on user-provided product details and may include long-form PRD sections, local template files, and generated project documentation.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
