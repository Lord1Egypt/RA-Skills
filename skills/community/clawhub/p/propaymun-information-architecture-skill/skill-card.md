## Description:

Shape, review, and validate end-to-end product information architecture, product/UX sitemaps, and stateful user flows when users need clearer structure, labels, relationships, access, findability, destinations, or task paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kamroncorp](https://clawhub.ai/user/kamroncorp)

### License/Terms of Use:

MIT-0

## Use Case:

Product teams, designers, researchers, content strategists, and developers use this skill to shape, review, and validate product information architecture, product/UX sitemaps, stateful user flows, and related handoffs from an evidence-aware semantic foundation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: IA recommendations, sitemaps, user flows, or builder handoffs could be mistaken for approved product decisions.

Mitigation: Review outputs with appropriate product, design, content, engineering, or domain owners before treating them as final decisions.

Risk: Optional helper scripts can create local files when paths are provided.

Mitigation: Provide explicit output paths only when local file creation is intended, and review generated files before sharing or reusing them.

Risk: Generated builder handoffs can carry incorrect or incomplete architecture into downstream visual or prototype tools.

Mitigation: Review handoffs before using them in a builder and keep unresolved assumptions visible until confirmed.

## Reference(s):

- [IA Foundations and Decision Rules](references/ia-foundations.md)
- [Modeling and Option Generation](references/modeling.md)
- [Product and UX Sitemap](references/sitemap.md)
- [Stateful User Flow](references/user-flow.md)
- [IA Deliverables and Semantic Model](references/deliverables.md)
- [IA Validation and Measurement](references/validation.md)
- [Evidence and Uncertainty](references/evidence.md)
- [Capability-Aware Execution and Output Routing](references/capability-routing.md)
- [Visual Builder Handoff](references/visual-builder-handoff.md)
- [Optional IA Diagramming](references/diagramming.md)
- [Contextual Localization](references/localization.md)
- [Discovery and Low-Effort Interaction](references/discovery.md)
- [ProPaymun Semantic IA Model Schema](schema/semantic-ia.schema.json)
- [ProPaymun Product Sitemap Schema](schema/product-sitemap.schema.json)
- [ProPaymun Stateful User Flow Schema](schema/user-flow.schema.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text and Markdown, with optional JSON models, HTML exports, builder handoff files, and shell commands for local validation or export.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional helper scripts can create local validation, HTML, or builder handoff files only when explicit paths are provided.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
