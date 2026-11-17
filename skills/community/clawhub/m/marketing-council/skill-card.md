## Description:

Marketing Council convenes a simulated board of documented marketing advisors to review marketing questions, surface disagreements, and synthesize a recommendation with next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coreyhaines31](https://clawhub.ai/user/coreyhaines31)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing teams use this skill to get multiple simulated expert perspectives on strategy, positioning, pricing, copy, launch, brand, channel, and growth decisions. It is intended to expose trade-offs among documented marketing frameworks before the user chooses an execution direction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project marketing context files may contain confidential strategy that the skill is designed to read when present.

Mitigation: Review `.agents/product-marketing.md`, `.claude/product-marketing.md`, and legacy product marketing context files before use, and avoid storing highly confidential strategy there unless it should be considered during council reviews.

Risk: Optional live research may introduce current external claims or source attributions that affect the council's recommendations.

Mitigation: Prefer primary sources, include citations for researched claims, and verify source quality before relying on time-sensitive advice.

Risk: Simulated takes from named advisors could be mistaken for real endorsements, quotes, or opinions about the user's company.

Mitigation: Keep the simulation disclaimer in outputs, avoid fabricated quotes, and describe advisors as applying documented frameworks rather than personally reviewing the user's work.

## Reference(s):

- [Custom Advisor Template](references/advisor-template.md)
- [Alex Hormozi](references/advisors/alex-hormozi.md)
- [Ann Handley](references/advisors/ann-handley.md)
- [April Dunford](references/advisors/april-dunford.md)
- [Byron Sharp](references/advisors/byron-sharp.md)
- [Claude Hopkins](references/advisors/claude-hopkins.md)
- [David Ogilvy](references/advisors/david-ogilvy.md)
- [Eugene Schwartz](references/advisors/eugene-schwartz.md)
- [Gary Halbert](references/advisors/gary-halbert.md)
- [Gary Vaynerchuk](references/advisors/gary-vaynerchuk.md)
- [Rory Sutherland](references/advisors/rory-sutherland.md)
- [Russell Brunson](references/advisors/russell-brunson.md)
- [Seth Godin](references/advisors/seth-godin.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Files]

**Output Format:** [Markdown with structured council sections, advisor takes, disagreement map, synthesis, and optional local advisor dossier files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs must label sessions as simulation, avoid fabricated quotes or endorsements, and use live research when current claims are requested.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
