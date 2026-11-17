## Description:

Create, refactor, and improve Codex-compatible skills with gated requirement discovery, reusable resource planning, executable scaffolding scripts, and validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nimachu](https://clawhub.ai/user/nimachu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to design, scaffold, validate, package, refactor, and improve Codex-compatible skills with structured discovery and review gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent skill folders and modify files when its scaffolding scripts are used.

Mitigation: Review target paths before running generated commands, especially paths under CODEX_HOME or other shared skill locations.

Risk: Packaging output inside the source skill directory can pollute the source artifact or future package contents.

Mitigation: Write package archives outside the source skill directory and validate the skill before packaging.

Risk: Generated or refactored skill guidance can be misleading if requirements are underspecified.

Mitigation: Use the discovery gate to confirm inputs, outputs, triggers, constraints, and target directory before creating or rewriting skill files.

## Reference(s):

- [Best Practices](references/best-practices.md)
- [Skill Design Patterns](references/design-patterns.md)
- [Chinese Discovery Prompts](references/interaction-guide.md)
- [Output Patterns](references/output-patterns.md)
- [Workflow Patterns](references/workflows.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated or modified skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create skill folders, reference files, scripts, OpenAI interface configuration, and zip archives when the user chooses those workflows.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
