## Description:

Generates AI-assisted logo and brand identity kits with logo concepts, color palettes, typography recommendations, and brand guidelines from brand inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, designers, marketers, and developers use this skill to generate structured brand identity documentation for a named brand, including logo concepts, palettes, fonts, and usage guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad read, write, and command execution permissions are requested for a brand-design workflow.

Mitigation: Run the skill only in a constrained workspace and limit use to explicit brand-design actions or known CellCog commands.

Risk: The skill may be given access to sensitive workspaces or credentials while generating design assets.

Mitigation: Avoid exposing secrets, credentials, or unrelated project files; use environment scoping and review generated commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/logo-brand-identity-2)
- [SkillHub homepage](https://skillhub.ai/skills/logo-brand-identity-cellcog)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Structured Markdown with JSON palette blocks, SVG snippets, CSS font stacks, and example shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Brand inputs include name and industry, with optional audience, personality, and competitor references.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
