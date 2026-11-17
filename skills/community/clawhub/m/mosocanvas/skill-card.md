## Description:

MoSoCanvas provides evidence-based visual direction for campaign images, posters, social image series, and physical promotional collateral, including authored shot planning, composition boards, visual narrative, color and light scripts, artifact review, controlled repair, and quality benchmarking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1558695948-crypto](https://clawhub.ai/user/1558695948-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agents through visual-direction workflows for campaign imagery, posters, social image series, and physical promotional collateral. It supports direction, production, repair, review, and bypass modes with evidence records, validation scripts, and independent artifact review checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts can read project files and write workflow artifacts such as masks, manifests, review packets, and release archives.

Mitigation: Point scripts only at files intended for the visual workflow, and review generated artifacts before sharing or release.

Risk: Visual quality claims can be misleading if based on prompts, intended direction, or generator self-assessment instead of inspected artifacts.

Mitigation: Inspect actual returned images, keep independent review records, and require user acceptance before treating an artifact as final.

Risk: Reference-led visual work can create rights or imitation risk if protected source material is copied rather than analyzed for transferable mechanisms.

Mitigation: Classify reference use, record source provenance and do-not-copy constraints, and require authoritative confirmation for cultural, legal, identity, or permissions issues.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/1558695948-crypto/MoSoCanvas/tree/main/mosocanvas)
- [ClawHub skill page](https://clawhub.ai/1558695948-crypto/skills/mosocanvas)
- [Evidence foundations](references/evidence-foundations.md)
- [Reference Deconstruction](references/reference-deconstruction.md)
- [Shot and composition grammar](references/shot-composition-grammar.md)
- [Generated-image authenticity review](references/generated-image-authenticity.md)
- [Preservation and Repair](references/preservation-and-repair.md)
- [Midjourney quality benchmark](references/midjourney-quality-benchmark.md)
- [Pixar in a Box storytelling curriculum](https://www.khanacademy.org/humanities/grammar/storytelling)
- [American Cinematographer Shot Craft](https://theasc.com/articles/shot-craft-where-do-you-put-the-camera)
- [Tatler et al. gaze behavior review](https://pmc.ncbi.nlm.nih.gov/articles/PMC3134223/)
- [CIECAM16 color appearance model](https://www.cie.co.at/publications/cie-2016-colour-appearance-model-colour-management-systems-ciecam16)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON artifacts and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local schemas, validation scripts, masks, manifests, review packets, and release archives when they are part of the visual workflow.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact VERSION and heading report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
