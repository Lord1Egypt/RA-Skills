## Description:

Applies an ASD-STE100-derived register to operator and procedural text

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to shape operator replies and procedural text, and to check sentence and paragraph length and noun clusters. Its checks are advisory; it does not check controlled vocabulary or establish STE compliance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment has medium confidence and partial coverage because a local path-like reference could not be resolved.

Mitigation: Review the unresolved reference and its related component before relying on the scan assessment.

Risk: The American-spelling rule may not fit every audience or locale.

Mitigation: Review and adapt spelling to the intended audience.

Risk: Applying a limited STE-derived register outside procedural text can remove useful reasoning or affect technical accuracy.

Mitigation: Use the register for operator-facing and procedural text, then review the result for accuracy and completeness.

Risk: The advisory checks can under-report procedural text that they cannot classify.

Mitigation: Review the target text manually; treat a clean check as limited evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-scribe-simplified-technical-english)
- [Skill homepage (metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/scribe)
- [Prompt complexity study (arXiv:2603.13351)](https://arxiv.org/abs/2603.13351)
- [Constraint interference study (arXiv:2601.22047)](https://arxiv.org/abs/2601.22047)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Shell commands]

**Output Format:** [Operator-facing text and procedural guidance, with advisory file:line findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory checks; no controlled vocabulary validation]

## Skill Version(s):

1.10.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
