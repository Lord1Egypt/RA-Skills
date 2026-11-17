## Description:

Repairs and maintains PowerPoint PPTX templates with slide masters, placeholders, theme fonts, theme colors, chart links, and branded layouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External users, brand teams, consultants, presentation operations teams, and developers use this skill to diagnose and repair PPTX template failures caused by slide masters, layouts, placeholders, themes, chart links, media relationships, or automated deck generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Template repair can corrupt or overwrite valuable PPTX files if changes are applied directly to originals.

Mitigation: Work from a copy, keep original templates backed up, and review generated file changes before replacing production assets.

Risk: Direct OOXML changes to unsupported master, theme, chart-link, or relationship structures can break template fidelity.

Mitigation: Inspect the exact PowerPoint part or relationship before patching, then validate slide count, layout assignments, placeholders, theme values, fonts, charts, linked media, and rendered appearance.

Risk: Generated repair guidance may bind content to the wrong placeholder or introduce brand-inconsistent overrides.

Mitigation: Map each visible issue to the master, layout, slide, theme, or relationship layer and prefer existing layouts, placeholders, theme references, and brand rules over manual shapes or hard-coded values.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/powerpoint-pptx-layout-export-helper-2-180322)
- [kyro-ma Publisher Profile](https://clawhub.ai/user/kyro-ma)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with diagnostic prose, implementation snippets, and validation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PowerPoint part paths, OOXML changes, python-pptx guidance, and visual or structural validation notes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
