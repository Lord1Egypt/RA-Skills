## Description:

Use when building journal club or literature-report slides from research PDFs and you need a figure-first, audience-facing, visually polished deck that preserves paper logic, keeps crops safe, pairs main and supporting evidence correctly, and passes render-based QA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yufeng166977](https://clawhub.ai/user/yufeng166977)

### License/Terms of Use:

MIT-0

## Use Case:

External users, educators, researchers, and agents use this skill to turn one or more research PDFs into presentation-ready journal club, lab meeting, literature review, or paper-report slide decks. It emphasizes paper-logic preservation, figure integrity, support-evidence pairing, bilingual readiness when requested, and render-based quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Processing private papers or unpublished research may expose sensitive source material if dependencies or environments are not reviewed.

Mitigation: Use a local virtual environment and prefer pinned, reviewed package versions from trusted indexes before processing private or unpublished material.

Risk: Generated decks can mislead audiences if figures are cropped, distorted, paired with the wrong support evidence, or accepted without rendered inspection.

Mitigation: Preserve aspect ratios, map support figures by conclusion, inspect rendered PDF or slide images, and repeat fix-and-verify checks before delivery.

## Reference(s):

- [MetaEdit journal-club mapping and crop notes](references/metaedit-jcslides-mapping-and-crop-notes.md)
- [Multi-paper plasmid copy-number deck session notes](references/multi-paper-plasmid-copy-number-deck.md)
- [Python-pptx first-pass render QA lessons for paper journal-club decks](references/python-pptx-render-qa-first-pass.md)
- [Figure integrity deep-fix notes](references/figure-integrity-deep-fix-notes.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with possible code, shell commands, and file path recommendations for generating and checking presentation decks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of PPTX files, rendered QA outputs, figure crops, workspace notes, and local dependency setup.]

## Skill Version(s):

2.0.0 (source: server release metadata; artifact frontmatter states 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
