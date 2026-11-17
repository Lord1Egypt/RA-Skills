## Description:

Applies an ASD-STE100-derived register to operator and procedural text

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to apply a limited, STE-derived register to operator replies and procedural text. It also provides advisory checks for sentence length, paragraph length, and noun clusters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The style directive may interfere with accuracy or reasoning when applied to text that needs fuller explanation.

Mitigation: Apply the register only to operator-facing and procedural text within the documented scope, then review technical facts and completeness separately.

Risk: Readers may mistake this STE-derived subset for full ASD-STE100 implementation or compliance.

Mitigation: Describe it as an STE-derived authoring aid; do not claim compliance, certification, or endorsement.

Risk: The advisory checks can under-report some procedural text and noun-cluster findings can be inaccurate.

Mitigation: Review each finding against the text's scope and treat noun-cluster results as advisory.

Risk: The security scan did not assess one referenced local path, so its coverage is incomplete.

Mitigation: Review the missing local reference before relying on the skill's guidance.

## Reference(s):

- [Prompt complexity and reasoning (arXiv 2603.13351)](https://arxiv.org/abs/2603.13351)
- [Constraint interference (arXiv 2601.22047)](https://arxiv.org/abs/2601.22047)
- [SimpleEnglish benchmark and audit](https://github.com/AminBlg/SimpleEnglish)
- [Informal code-fact test](https://allaboutcoding.ghinda.com/explain-to-me-in-simple-technical-english/)
- [Nieminen thesis on hallucination judgments](https://gupea.ub.gu.se/items/18568d0f-52af-43ed-8915-abd0d9bf7afe/full)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown and procedural text, with optional command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory style guidance and checks for in-scope operator-facing text; does not establish technical correctness or STE compliance.]

## Skill Version(s):

1.10.3 (source: frontmatter; release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
