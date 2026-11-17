## Description:

Skill Audit evaluates OpenClaw AgentSkills for structural compliance, quality standards, and OpenClaw-specific architecture patterns, producing scored audit reports with grades, dimensional breakdowns, and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haseo-ai](https://clawhub.ai/user/haseo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to audit OpenClaw AgentSkills, compare them against a six-dimension rubric, and receive prioritized improvement recommendations before release or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audited skill files may contain private instructions or sensitive local context that can be written into audit reports.

Mitigation: Audit only files you are authorized to review and clean the OpenClaw report directory when reports may contain private material.

Risk: Audit scores and recommendations may be incomplete or misleading if the target skill files are missing, stale, or evaluated against an unsuitable rubric.

Mitigation: Review the generated scorecard and recommendations before using them for release, deployment, or governance decisions.

## Reference(s):

- [Skill Audit on ClawHub](https://clawhub.ai/haseo-ai/skills/oc-skill-audit)
- [haseo-ai Publisher Profile](https://clawhub.ai/user/haseo-ai)
- [Scoring Rubric](references/scoring-rubric.md)
- [Scoring Rubric Korean](references/scoring-rubric.ko.md)
- [Scoring Rubric Japanese](references/scoring-rubric.ja.md)
- [Scoring Rubric Chinese](references/scoring-rubric.zh.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance, files]

**Output Format:** [Markdown audit report plus a concise response summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a 0-100 score, A-F grade, dimensional breakdown, bilingual report when applicable, and prioritized recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
