## Description:

Runs a target repository’s Harness checks and reports automated evidence separately from real-host smoke tests and human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huiyonghkw](https://clawhub.ai/user/huiyonghkw)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to select and run working-tree, staged, or CI verification for a Harness. It helps them report observed results while keeping real-host smoke tests and human review as separate evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs scripts supplied by the target repository with the current user’s permissions; local modes may read local Skill and Agent Memory data and write sanitized observation events.

Mitigation: Use local modes only in repositories you own or trust. For an unfamiliar repository, review its verify.sh and use --ci-hermetic by default.

Risk: The benign security verdict has medium confidence and partial scan coverage; the scanner could not confirm the effects of hook changes or adapter repair.

Mitigation: Review the relevant verifier, hook contents, and repair scripts before execution, and do not treat the scan verdict as a guarantee of safety.

## Reference(s):

- [Harness Check product page](https://huiyonghkw.github.io/hekouwang-harness-check-skill/)
- [Harness Check guide](https://huiyonghkw.github.io/hekouwang-harness-check-skill/guide/index.html?lang=zh)
- [Check matrix](references/check-matrix.md)
- [Score rubric](references/score-rubric.json)
- [Scorecard schema](references/scorecard-schema.json)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, Markdown]

**Output Format:** [Markdown report with command results and evidence references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports automated checks separately from real-host smoke tests and human review.]

## Skill Version(s):

1.0.1 (source: frontmatter; CHANGELOG released 2026-10-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
