## Description:

Picasso helps agents design, build, critique, polish, and systematize production-grade frontend interfaces and visual artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viperrcrypto](https://clawhub.ai/user/viperrcrypto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and design engineers use Picasso to guide frontend design decisions, UI implementation, interaction polish, accessibility checks, and design-system generation for web interfaces, components, dashboards, landing pages, and visual artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may recommend third-party frontend tools or remote component installation commands.

Mitigation: Pin versions, inspect generated files before use, and avoid running unpinned remote commands in sensitive projects.

Risk: The skill includes guidance that may lead agents to use IP-based location defaults in frontend experiences.

Mitigation: Use location defaults only when the application clearly discloses the behavior and genuinely needs it.

Risk: Design and implementation guidance can be incorrect, overbroad, or unsuitable for a specific product context.

Mitigation: Review proposed UI changes, accessibility behavior, dependencies, and generated code before deployment.

## Reference(s):

- [Publisher skill homepage](https://github.com/viperrcrypto/picasso)
- [Anti-Patterns Reference](references/anti-patterns.md)
- [Typography Reference](references/typography.md)
- [Color and Contrast Reference](references/color-and-contrast.md)
- [Spatial Design Reference](references/spatial-design.md)
- [Accessibility and WCAG 2.2 Reference](references/accessibility-wcag.md)
- [Responsive Design Reference](references/responsive-design.md)
- [React Patterns Reference](references/react-patterns.md)
- [Performance Optimization Reference](references/performance-optimization.md)
- [Design System Reference](references/design-system.md)
- [Tools and Libraries Catalog](references/tools-catalog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code blocks, implementation recommendations, and design review notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend frontend libraries, design tokens, accessibility checks, and project-specific UI changes.]

## Skill Version(s):

2.0.3 (source: server release metadata; artifact frontmatter says 2.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
