## Description:

原型设计技能 helps agents build complex business-system HTML prototypes using a default Figma style and 58 built-in design-system references for page layouts, statistics cards, filters, tables, modals, detail views, and kanban or list workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[contsun](https://clawhub.ai/user/contsun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product or design teams use this skill to create management-console and business workflow prototypes from requirements, including HTML/CSS/JS pages, modals, data tables, dashboard views, and kanban or list views.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review warns that the skill normalizes broad repository commits and persistent memory writes.

Mitigation: Review generated file operations and allow repository commits or memory-file updates only when the user explicitly requests those side effects.

Risk: The security review warns about unpinned npx server execution.

Mitigation: Pin or approve package versions before running development servers and prefer local project scripts when available.

Risk: The security review flags an active captured HTML reference file.

Mitigation: Inspect and sanitize references/design-systems/linear.app-DESIGN.md before using or redistributing the bundled references.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/contsun/skills/prototype-design)
- [README](README.md)
- [Field norms](references/field-norms.md)
- [Page template](references/page-template.html)
- [Figma design system](references/design-systems/figma-DESIGN.md)
- [Linear design system](references/design-systems/linear-DESIGN.md)
- [Vercel design system](references/design-systems/vercel-DESIGN.md)
- [Notion design system](references/design-systems/notion-DESIGN.md)
- [Stripe design system](references/design-systems/stripe-DESIGN.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local prototype files when the user asks the agent to implement a prototype.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
