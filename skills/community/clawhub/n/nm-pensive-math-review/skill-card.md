## Description:

Verifies math-heavy code for algorithmic correctness and numerical stability

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review mathematical, scientific, statistical, and machine learning code. It checks requirements, derivations, numerical stability, and test evidence, then produces grounded findings and a review recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running tests or notebook cells from an unfamiliar project may have side effects.

Mitigation: Review the commands and notebook cells first, and run them only in a trusted, appropriately isolated environment.

Risk: Four local references were unresolved, so the scanner could not establish that all referenced material was reviewed.

Mitigation: Check that referenced guidance is available and review it before relying on the complete workflow.

## Reference(s):

- [math-review release on ClawHub](https://clawhub.ai/athola/skills/nm-pensive-math-review)
- [Pensive plugin documentation](https://github.com/athola/claude-night-market/tree/master/plugins/pensive)
- [Requirements Mapping](artifact/modules/requirements-mapping.md)
- [Derivation Verification](artifact/modules/derivation-verification.md)
- [Numerical Stability Analysis](artifact/modules/numerical-stability.md)
- [Testing Strategies for Mathematical Code](artifact/modules/testing-strategies.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown review report with findings, evidence references, and a recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings should include source locations and supporting evidence; unverified findings are labeled or omitted.]

## Skill Version(s):

1.10.3 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
