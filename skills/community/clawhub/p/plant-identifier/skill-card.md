## Description:

Identify plants from photos using trait-based analysis, ranked species candidates, follow-up capture guidance, and a reusable local log.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to identify plants from one or more photos, compare ranked candidates, decide what plant part to photograph next, and optionally save approved local observation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local observation notes may include sensitive location or personal context.

Mitigation: Save notes only with user approval and avoid storing precise home addresses or unrelated personal information.

Risk: Photo-based identification could be mistaken for edible, toxic, or medicinal clearance.

Mitigation: Keep safety decisions separate from identification and answer safety-sensitive requests conservatively.

Risk: Incomplete photos can lead to uncertain species-level identification.

Mitigation: Use ranked candidates with explicit confidence bands and request the single most useful missing plant view.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/plant-identifier)
- [Skill homepage](https://clawic.com/skills/plant-identifier)
- [Plant evidence guide](artifact/evidence-guide.md)
- [Memory template](artifact/memory-template.md)
- [Setup guide](artifact/setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown with ranked candidates, confidence bands, follow-up photo guidance, and optional local observation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local observation files are written only when the user approves]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
