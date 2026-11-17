## Description:

Arrange and review both-hand fingerings for solo piano images, PDF, MusicXML, MXL, or MuseScore, and deliver annotated MusicXML/PDF, previews, and a quality report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yannxinn](https://clawhub.ai/user/yannxinn)

### License/Terms of Use:

MIT-0

## Use Case:

Pianists, music educators, and music software users can use an agent to verify score facts, arrange and review both-hand fingerings, and prepare annotated scores with quality reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated fingerings or label placement may contain defects.

Mitigation: Check hand assignments, fingerings, and placement, require strict validation for final delivery, and treat benchmark percentages cautiously.

Risk: Coordinate refresh or optional label hiding can clear existing fingering assignments in output.

Mitigation: Keep original scores and reviewed plans, use fresh output folders, and inspect affected assignments before relying on results.

Risk: Optional external programs and OCR downloads have runtime behavior outside the static review.

Mitigation: Authorize optional tools and downloads separately and review their behavior before use.

## Reference(s):

- [ClawHub release](https://clawhub.ai/yannxinn/skills/piano-score-fingering)
- [Professional fingering rules](artifact/references/professional-fingering-rules.md)
- [Structured OMR guidance](artifact/references/structured-omr.md)
- [Reliability and recovery architecture](artifact/references/reliability-architecture.md)

## Skill Output:

**Output Type(s):** [MusicXML, PDF, PNG previews, JSON review and quality reports, Markdown delivery reports]

**Output Format:** [Annotated score files, previews, and reviewable quality reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Unresolved score facts or anchors keep results in review-required status.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
