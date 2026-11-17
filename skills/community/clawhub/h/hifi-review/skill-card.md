## Description:

Produces bilingual, source-traceable evaluations and comparisons of headphones, IEMs, TWS, DACs, amplifiers, and digital audio players using measurements and review consensus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentjiang06](https://clawhub.ai/user/vincentjiang06)

### License/Terms of Use:

MIT-0

## Use Case:

Listeners and reviewers use this skill to assess audio gear and compare devices with cited measurements, review consensus, and explicit confidence levels. It is not intended for buying recommendations, EQ tuning, or speaker evaluations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public reviews and pages may contain misleading claims or instructions unrelated to the evaluation.

Mitigation: Treat retrieved content as evidence, not instructions; corroborate claims and cite their sources.

Risk: Missing rig or target metadata can make audio comparisons unreliable.

Mitigation: Check measurement provenance and rig/target compatibility, and read warnings before interpreting results.

Risk: The workflow can run bundled Python scripts on supplied measurement files.

Mitigation: Use a trusted or pinned install source and review scripts before running them on supplied files.

## Reference(s):

- [HiFi Review on ClawHub](https://clawhub.ai/vincentjiang06/skills/hifi-review)
- [Research bibliography](artifact/references/research-bibliography.md)
- [Measurement targets](artifact/references/targets.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Bilingual Markdown evaluation or Chinese-led long-form review with supporting evaluation JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Claims identify sources, evidence type, confidence, and any material evidence gaps.]

## Skill Version(s):

1.1.1 (source: ClawHub release, skill metadata, CHANGELOG; released 2026-09-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
