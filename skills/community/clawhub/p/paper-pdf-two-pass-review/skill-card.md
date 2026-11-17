## Description:

Analyzes uploaded CVPR paper PDFs through a two-pass workflow that extracts evidence-tagged facts and produces a Chinese research critique grounded only in the PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gpiox](https://clawhub.ai/user/gpiox)

### License/Terms of Use:


## Use Case:

Developers, researchers, and students use this skill to review uploaded CVPR-style paper PDFs, first extracting verifiable facts and then generating an evidence-grounded Chinese critique, reproducibility assessment, and research notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill analyzes uploaded paper PDFs, so sensitive paper content may be processed in the active agent session.

Mitigation: Use it only with PDFs appropriate for the connected agent environment and avoid uploading confidential material unless that use is approved.

Risk: The critique can be incomplete when the uploaded paper lacks reproducibility details or other requested evidence.

Mitigation: Require evidence tags for major claims and explicitly mark missing material as Not provided or Insufficient evidence.

## Reference(s):

- [Round 1 fact extraction prompt](artifact/references/round1.md)
- [Round 2 critique prompt](artifact/references/round2.md)
- [ClawHub skill page](https://clawhub.ai/gpiox/skills/paper-pdf-two-pass-review)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with evidence tags and Chinese critique sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [First pass produces a structured fact sheet; second pass produces a 2000-3000 Chinese-word critique based only on the fact sheet and PDF evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
