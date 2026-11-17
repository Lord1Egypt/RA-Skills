## Description:

Create cinematic, narrative, interactive web presentations from a topic or briefing. Use when the user wants an immersive presentable experience rather than a conventional slide deck.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cbbathaglini](https://clawhub.ai/user/cbbathaglini)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to plan, build, review, or improve immersive web presentations, technical explainers, scrollytelling experiences, and speaker-ready interactive microsites. It is intended for presentation work that needs scenes, narrative structure, visual metaphors, motion intent, interaction, presenter controls, accessibility, and responsive behavior rather than conventional slide decks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated presentation projects may add dependencies, sourced assets, or optional GSAP integration that should be reviewed before use.

Mitigation: Review generated dependencies, asset sources, licenses, and motion-library integration in the resulting project before deployment.

Risk: Motion-heavy scenes can reduce accessibility, cause discomfort, or obscure the intended explanation if keyboard navigation, focus states, reduced motion, and readable labels are not preserved.

Mitigation: Verify keyboard controls, visible focus, color contrast, text alternatives for essential visuals, reduced-motion mode, mobile framing, and complete scene navigation before delivery.

Risk: Interactive presentation output can overemphasize visual effect while producing an unclear or misleading narrative.

Mitigation: Review the plan for a clear audience, objective, thesis, acts, scene list, persistent objects, transformations, presenter notes, and final decision or memory image.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cbbathaglini/skills/immersive-presentations)
- [Narrative Architecture](references/narrative-architecture.md)
- [Scene System](references/scene-system.md)
- [Motion And GSAP](references/motion-and-gsap.md)
- [Interaction And Modes](references/interaction-and-modes.md)
- [Accessibility, Responsive Design, And Performance](references/accessibility-responsive-performance.md)
- [Diagrams, Data, And Domains](references/diagrams-data-and-domains.md)
- [Anti-Patterns And Quality Bar](references/anti-patterns-and-quality-bar.md)
- [Presentation Plan Template](references/templates/presentation-plan-template.md)
- [Scene Spec Template](references/templates/scene-spec-template.md)
- [Briefing Template](references/templates/briefing-template.md)
- [Prompt Pack](references/templates/prompt-pack.md)
- [Example: RAG vs Agents](references/examples/rag-vs-agents.md)
- [Example: Climate Risk Boardroom](references/examples/climate-risk-boardroom.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, implementation plans, code, configuration, and shell commands as needed for a web presentation project]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include a presentation plan, scene specifications, web implementation files, presenter and debug controls, responsive behavior, accessibility notes, reduced-motion behavior, and integration guidance for GSAP or native web animation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
