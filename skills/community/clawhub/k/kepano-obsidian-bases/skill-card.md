## Description:

Create and edit Obsidian Bases (.base files) with views, filters, formulas, and summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hoyaryyj](https://clawhub.ai/user/hoyaryyj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Obsidian users use this skill to create, edit, and validate Obsidian `.base` YAML files that present notes as database-like views with filters, formulas, summaries, and table, card, list, or map layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated `.base` files can surface note metadata from an Obsidian vault through filters and displayed properties.

Mitigation: Review generated `.base` files before use, especially filters and displayed properties.

Risk: Incorrect YAML, formulas, or property references can cause Obsidian Bases to render incorrectly or fail validation.

Mitigation: Validate YAML syntax, confirm formulas and referenced properties exist, and test the `.base` file in Obsidian.

## Reference(s):

- [Complete Functions Reference](references/FUNCTIONS_REFERENCE.md)
- [Obsidian Bases Syntax](https://help.obsidian.md/bases/syntax)
- [Obsidian Bases Functions](https://help.obsidian.md/bases/functions)
- [Obsidian Bases Views](https://help.obsidian.md/bases/views)
- [Obsidian Formulas](https://help.obsidian.md/formulas)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with YAML examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local Obsidian `.base` YAML content and review guidance; users should validate generated YAML in Obsidian before relying on it.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
