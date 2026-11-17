## Description:

Provides guidance for more reliable, lower-cost self-evaluation of local LLM outputs through predefined scoring criteria, source-backed judgments, and rule-versus-model comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

All Rights Reserved (documentation and theory; MIT applies only to .py code, none included)

## Use Case:

Developers and evaluators use this skill to set scoring rubrics, check evidence for each score, compare rule-based checks with local-model judgments, and reduce evaluation calls through screening, sampling, and caching. Its scores are for internal guidance, not independent certification of model capability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package labels itself MIT, but its documentation and theory are marked All Rights Reserved.

Mitigation: Review the package's licensing notes before copying or redistributing its text; do not assume the MIT license covers documentation.

Risk: Local model self-scores can overstate quality or be mistaken for independent assessment.

Mitigation: Define criteria before scoring, cite the evaluated text, flag rule/model disagreements, and use independent reproducible tests for external claims.

Risk: Broad evaluation terms may invoke the skill outside the intended self-evaluation task.

Mitigation: Confirm the user's intent before applying its scoring guidance.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/local-llm-eval-assist)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown or plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reference scores should cite the evaluated text and flag disagreements between rule-based and model judgments.]

## Skill Version(s):

1.0.3 (source: ClawHub release; artifact frontmatter says 1.0.1 and manifest says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
