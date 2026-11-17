## Description:

政府采购领域"某项目应选/已选何种采购方式"的法定适用条件判定与合规验证引擎，覆盖六种法定采购方式、框架协议采购和工程招投标法衔接，并提示阈值、程序和红黄蓝风险。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement staff, compliance reviewers, and advisors use this skill to choose or verify a Chinese government procurement method from project facts, budget thresholds, legal conditions, and procedural requirements. It supports forward recommendation and reverse compliance checks while reminding users that final approval remains with the responsible purchaser, budget authority, fiscal department, or legal reviewer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Procurement-law and threshold guidance can become stale as national or local rules change.

Mitigation: Verify conclusions against current official legal texts, local threshold standards, and the skill's retrieved knowledge-base sources before relying on the recommendation.

Risk: Users may mistake the output for an official approval, fiscal-department decision, or legal opinion.

Mitigation: Use the output as compliance guidance only and route final decisions through the purchaser's internal process, fiscal authority, procurement counsel, or other responsible reviewer.

Risk: Incomplete project facts can lead to conditional or incorrect procurement-method selection.

Mitigation: Require the core facts and follow-up questions described by the artifact, and keep the conclusion at a lower confidence level when facts are missing.

Risk: A user may ask the agent to justify split purchases, fabricated urgency, or other procedure-avoidance behavior.

Mitigation: Apply the artifact's refusal posture for unlawful evasion requests and provide only lawful-basis explanations and compliant alternatives.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/govproc-method-selector-plus-1-0-0)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown compliance report with embedded structured JSON fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes procurement method recommendation or compliance verdict, legal basis, condition checks, procedural requirements, red flags, threshold source, law-version note, audit risk level, and disclaimer.]

## Skill Version(s):

1.0.0 (source: evidence release metadata, artifact/SKILL.md frontmatter, artifact/manifest.yaml, artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
