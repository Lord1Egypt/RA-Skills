## Description:

Paper Framework Figure Studio Pro helps researchers design, prompt, generate, critique, and integrate publication-ready framework-style figures for research papers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c-narcissus](https://clawhub.ai/user/c-narcissus)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, paper authors, and technical teams use this skill to turn paper PDFs, abstracts, method notes, or draft figure ideas into structured framework diagrams, candidate figure directions, image prompts, review guidance, captions, legends, and paper insertion text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research papers or draft methods may contain unpublished or proprietary material that could be sent to an external image-generation provider during rendering.

Mitigation: Confirm that sharing the source material with the selected image provider is acceptable before using image-generation steps.

Risk: The workflow defaults to multi-candidate image generation, commonly six images, which can consume provider quota or create unexpected cost.

Mitigation: Set an explicit candidate count or request text-only planning when cost, latency, or quota matters.

Risk: Chinese-first templates and prompts may not match every user's preferred publication workflow language.

Mitigation: Ask the skill to operate in the preferred language before starting the workflow or before generating final prompt packages.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/c-narcissus/skills/paper-framework-figure-studio-pro)
- [Publisher profile](https://clawhub.ai/user/c-narcissus)
- [Workflow and state contract](artifact/references/workflow-and-state-contract.md)
- [Visual style and board protocol](artifact/references/visual-style-and-board-protocol.md)
- [Prompt generation policy](artifact/references/prompt-generation-policy.md)
- [Figure class taxonomy](artifact/references/figure-class-taxonomy.md)
- [Figure pattern library](artifact/references/figure-pattern-library.md)
- [Evidence lineage summary](artifact/references/evidence-lineage-summary.md)
- [Evidence map index](artifact/references/evidence-map-index.md)
- [Source corpus notes](artifact/references/source-corpus-notes.md)
- [Builder-time acquisition report](artifact/references/builder-time-acquisition-report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Image prompts, Raster images]

**Output Format:** [Markdown text, structured prompt packages, state footers, candidate-review notes, and bitmap image outputs when an approved image-generation route is available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text and image outputs are separated by turn; candidate and formal image generation normally use 4-6 candidates with a default of 6 unless the user explicitly requests one image or text-only work.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter, artifact/metadata.json, evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
