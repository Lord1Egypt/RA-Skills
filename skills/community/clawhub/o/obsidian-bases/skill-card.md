## Description:

Create and edit Obsidian Bases (.base files) with views, filters, formulas, and summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sadlay](https://clawhub.ai/user/sadlay)

### License/Terms of Use:


## Use Case:

External users and knowledge-base maintainers use this skill to create and edit Obsidian `.base` files that organize notes with views, filters, formulas, and summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated `.base` YAML may contain syntax errors, mismatched quotes, or references to undefined formulas or properties.

Mitigation: Review generated YAML before applying it to a vault, validate it as YAML, and open the `.base` file in Obsidian to confirm the view renders correctly.

Risk: The trigger wording is broad enough that the skill could be invoked for general Obsidian work outside Bases tasks.

Mitigation: Invoke it explicitly for `.base` files or Obsidian Bases work and confirm the generated content is relevant before using it.

Risk: Map views require latitude and longitude properties and the Maps community plugin.

Mitigation: Use map views only when the vault has location properties and the required Obsidian plugin is installed.

## Reference(s):

- [Obsidian Bases Syntax](https://help.obsidian.md/bases/syntax)
- [Obsidian Bases Functions](https://help.obsidian.md/bases/functions)
- [Obsidian Bases Views](https://help.obsidian.md/bases/views)
- [Obsidian Formulas](https://help.obsidian.md/formulas)
- [Complete Functions Reference](references/FUNCTIONS_REFERENCE.md)
- [ClawHub skill page](https://clawhub.ai/sadlay/skills/obsidian-bases)
- [ClawHub publisher profile](https://clawhub.ai/user/sadlay)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with YAML examples and Obsidian `.base` configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces user-reviewable Obsidian Bases YAML; users should validate syntax and behavior in Obsidian.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
