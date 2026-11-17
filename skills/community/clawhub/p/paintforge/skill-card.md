## Description:

PaintForge helps agents create polished, validated diagrams as standalone interactive HTML with inline SVG, dark/light themes, optional trace motion, and export support for PNG, JPEG, WebP, SVG, and WebM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyforge](https://clawhub.ai/user/anyforge)

### License/Terms of Use:

MIT

## Use Case:

Developers, engineers, and technical teams use PaintForge to turn plain-language requirements, Mermaid input, or bounded repository evidence into architecture, workflow, sequence, dataflow, lifecycle, ER, dependency, org, mind map, flowchart, network, matrix, kanban, Venn, gantt, and sankey diagrams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or replace chosen local HTML diagram outputs.

Mitigation: Review output paths before delivery and rely on the skill's validation and delivery receipts before treating an artifact as final.

Risk: Optional brand capture fetches a user-supplied HTTP(S) URL.

Mitigation: Use official HTTPS brand URLs only when brand identity is needed, and review the captured digest-pinned brand data before rendering.

Risk: Repository evidence reads a specified local Git checkout.

Mitigation: Point repository evidence only at the intended project and avoid sensitive or unrelated local directories.

Risk: Preview and visual-check workflows may start a loopback server, launch Chrome, and write screenshot sidecars.

Mitigation: Run these checks in a trusted local workspace, skip preview unless needed, and review generated sidecars before sharing them.

## Reference(s):

- [PaintForge ClawHub Skill Page](https://clawhub.ai/anyforge/skills/paintforge)
- [Authoring Contract](references/authoring-contract.md)
- [Delivery Contract](references/delivery-contract.md)
- [Viewer Runtime](references/viewer-runtime.md)
- [Brand Marks](references/brand-marks.md)
- [Schemas README](schemas/README.md)
- [Third-Party Notices](THIRD_PARTY_NOTICES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown handoff with generated JSON specifications, standalone HTML artifact paths, validation receipts, and optional browser-evidence status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local diagram artifacts and receipts; optional preview, brand capture, repository evidence, and visual-check flows require explicit local commands.]

## Skill Version(s):

1.0.7 (source: SKILL.md metadata, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
