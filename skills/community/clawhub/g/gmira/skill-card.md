## Description:

Use when building, redesigning, or reviewing a website or web surface that must not look generated.

This skill is ready for commercial/non-commercial use.

## Publisher:

[othmanadi](https://clawhub.ai/user/othmanadi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and design-focused agents use Gmira to plan, build, redesign, and review web surfaces such as landing pages, e-commerce flows, dashboards, portfolios, and marketing sites. It emphasizes visual direction, component taming, canvas/WebGL craft, accessibility, performance, and multi-viewport verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is opinionated and may guide an agent to modify frontend project files, install components, add packages, or change deployment behavior.

Mitigation: Review proposed component installs, package additions, copy tone, locale choices, and deployment steps before approving execution.

Risk: Canvas, WebGL, animation, and registry component choices can introduce performance, accessibility, or visual-regression issues if copied without verification.

Mitigation: Run the skill's recommended accessibility, performance, and multi-viewport visual checks before shipping changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/othmanadi/skills/gmira)
- [Server-Resolved Source Import](https://github.com/OthmanAdi/gmira/tree/main/skills/gmira)
- [Gmira Doctrine](references/DOCTRINE.md)
- [Canvas Craft Rules](references/canvas-craft-rules.md)
- [Canvas Primitives](references/canvas-primitives.md)
- [Finding 01: Tame the Arsenal](references/finding-01-tame-the-arsenal.md)
- [Finding 02: Idle State](references/finding-02-idle-state.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with code snippets, shell commands, configuration notes, and proposed or applied frontend file changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include visual direction, implementation steps, component repair guidance, accessibility and performance checks, and multi-viewport verification recommendations.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
