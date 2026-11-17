## Description:

Use when building journal club or literature-report slides from research PDFs and you need a figure-first, audience-facing, visually polished deck that preserves paper logic, keeps crops safe, pairs main and supporting evidence correctly, and passes render-based QA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0928wangyu](https://clawhub.ai/user/0928wangyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn one or more research-paper PDFs into presentation-ready journal club, lab meeting, literature review, or paper-report slide decks. It emphasizes faithful paper logic, safe figure crops, correctly paired supporting evidence, audience-facing wording, and render-based quality assurance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local PDF processing and deck generation can create workspace folders, crops, scripts, decks, and QA output files.

Mitigation: Run the skill in a project-specific workspace, review generated files before sharing, and avoid processing sensitive papers outside approved local environments.

Risk: Unpinned or ad hoc document-processing dependencies can reduce reproducibility.

Mitigation: Use a local virtual environment with pinned or reviewed dependencies before generating presentation assets.

Risk: Generated decks can contain misleading or presentation-useless evidence if figures are cropped unsafely, distorted, paired by page proximity, or left unreadable.

Mitigation: Verify figure-to-claim mapping before layout, preserve aspect ratios, use real support figures when available, and inspect rendered PDF or image outputs before delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0928wangyu/skills/journal-club-slides)
- [MetaEdit journal-club mapping and crop notes](references/metaedit-jcslides-mapping-and-crop-notes.md)
- [Multi-paper plasmid copy-number deck notes](references/multi-paper-plasmid-copy-number-deck.md)
- [Python-pptx first-pass render QA lessons](references/python-pptx-render-qa-first-pass.md)
- [Figure integrity deep-fix notes](references/figure-integrity-deep-fix-notes.md)
- [Metagenomic editing of commensal bacteria in vivo using CRISPR-associated transposases](https://doi.org/10.1126/science.adx7604)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with code and shell commands; may produce presentation decks, figure crops, workspace files, and rendered QA assets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes research PDFs locally and may create working folders, slide-generation scripts, deck files, crops, and render-QA outputs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter: 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
