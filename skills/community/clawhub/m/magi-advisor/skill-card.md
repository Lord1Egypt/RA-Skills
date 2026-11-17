## Description:

Magi Advisor helps users analyze strategic decisions, compare options, assess risks, and produce confidence-scored recommendations from rational, risk-focused, and intuition-focused perspectives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsmithfan](https://clawhub.ai/user/johnsmithfan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this Chinese-language skill to support complex decisions involving strategic tradeoffs, risk assessment, resource allocation, stakeholder conflict, or comparison across multiple options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML risk reports may be unsafe if populated with externally supplied risk fields before escaping or sanitization is added.

Mitigation: Treat HTML reports as local reports from trusted data only, or add escaping and sanitization before using external input.

## Reference(s):

- [Magi Advisor skill page](https://clawhub.ai/johnsmithfan/skills/magi-advisor)
- [Decision matrix reference](artifact/reference/decision-matrix.md)
- [MAGI framework reference](artifact/reference/magi-framework.md)
- [Strategic analysis prompt](artifact/prompts/strategic-analysis.md)
- [Risk assessment prompt](artifact/prompts/risk-assessment.md)
- [Multi-option comparison prompt](artifact/prompts/multi-option-compare.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with optional Python script output as terminal text, JSON, or local HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include decision matrices, ranked option scores, risk summaries, confidence labels, mitigation suggestions, and monitoring indicators.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
