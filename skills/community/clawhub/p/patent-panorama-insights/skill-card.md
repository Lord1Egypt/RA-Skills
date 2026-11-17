## Description:

Patent Panorama Insights guides agents through PatSnap patent panorama, landscape, competitor intelligence, technology roadmap, portfolio planning, and evidence-backed HTML reporting workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, patent analysts, and IP strategy teams use this skill to turn a business question into a reproducible patent-data workflow with query design, denoising, statistics, taxonomy planning, manual tagging handoff, and customer-facing HTML reporting. It is intended for decision support, not formal legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install path may fetch mutable remote content through npx.

Mitigation: Install from a pinned version or commit and verify the source before use.

Risk: PatSnap MCP access can expose or retrieve patent data beyond the intended project scope if credentials are over-broad.

Mitigation: Scope PatSnap MCP credentials to the intended patent-data access and confirm required endpoints before running the workflow.

Risk: Generated legal, asset, litigation, transfer, license, pledge, customs, award, or validity information may be mistaken for legal conclusions.

Mitigation: Treat these outputs as signals for expert review and do not use the skill as formal legal advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/patent-panorama-insights)
- [PatSnap Open Platform](https://open.zhihuiya.com/)
- [PatSnap Skill Hub listing](https://open.zhihuiya.com/marketplace/skill-hub/patent-panorama-insights)
- [Query & Taxonomy Construction Methodology](artifact/references/query-and-taxonomy-methodology.md)
- [Report HTML Blueprint](artifact/references/report-html-blueprint.md)
- [Report Visual Style](artifact/references/report-visual-style.md)
- [Scenario: Industry Landscape](artifact/references/scenario-industry-landscape.md)
- [Scenario: Technology Evolution](artifact/references/scenario-technology-evolution.md)
- [Scenario: Competitor Portrait](artifact/references/scenario-competitor-portrait.md)
- [Scenario: Solution Deep Dive](artifact/references/scenario-solution-deep-dive.md)
- [Scenario: Patent Package And Index](artifact/references/scenario-patent-package-and-index.md)
- [Scenario: Asset And Risk Signals](artifact/references/scenario-asset-and-risk-signals.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance, JSON/CSV work products, and single-file HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PatSnap MCP endpoints and scoped credentials; legal and asset information is treated as review signals rather than legal advice.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
