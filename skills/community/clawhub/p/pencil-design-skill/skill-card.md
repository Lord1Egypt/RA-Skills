## Description:

Designs UIs in Pencil (.pen files) and helps convert Pencil designs into production-ready code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caopipeline](https://clawhub.ai/user/caopipeline)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, developers, and product teams use this skill to create or edit Pencil UI design files, enforce layout and token rules, and generate React/Tailwind/shadcn-oriented implementation guidance from those designs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated UI copy may default to Simplified Chinese or follow an opinionated visual style that does not match the project.

Mitigation: Specify the desired language, style reference, brand constraints, and token rules before design work begins.

Risk: When Pencil MCP tools are connected, the skill can change existing Pencil documents.

Mitigation: Name the target files and clarify whether existing nodes may be edited, deleted, copied, or only read before allowing MCP-based edits.

Risk: Generated layouts or design-to-code output may still need human review for overflow, alignment, responsiveness, and implementation fit.

Mitigation: Run the documented layout audit, inspect screenshots or layout snapshots, and review generated code before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caopipeline/skills/pencil-design-skill)
- [Pencil format reference](references/pen-format.md)
- [Layout integrity rules](references/layout-integrity.md)
- [Overflow prevention](references/overflow-prevention.md)
- [Design tokens](references/design-tokens.md)
- [Design-to-code workflow](references/codegen-workflow.md)
- [Tailwind and shadcn mapping](references/codegen-mapping.md)
- [Component reuse](references/component-reuse.md)
- [Responsive breakpoints](references/responsive.md)
- [Pencil MCP tools](mcp/mcp-tools.md)
- [Visual verification](mcp/screenshot-qa.md)
- [Asset reuse](mcp/image-reuse.md)
- [PPT preset](ppt/presets-ppt.md)
- [getdesign.md style gallery](https://getdesign.md/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance, Pencil .pen JSON files, code snippets, and tool or shell command sequences]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated .pen designs are expected to use variables, bounded layouts, selected style references, and layout verification before completion.]

## Skill Version(s):

3.2.0 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
