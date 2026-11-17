## Description:

A Chinese-language graph-analysis helper for agent architectures that diagnoses structural smells, proposes refactorings, and records lightweight local learning notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to model an agent architecture as a directed graph, diagnose cycles, bottlenecks, orphan modules, duplicate roles, and missing roles, then generate refactoring proposals with a health-score check.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The learner can retain notes locally, which may preserve sensitive information if users include secrets or private context.

Mitigation: Do not pass secrets or sensitive private notes into learner notes; review or delete the local learned_patterns.json file when needed.

Risk: Refactoring proposals and health-score changes are heuristic graph analyses and may not reflect all real system constraints.

Mitigation: Review proposed architecture changes against the actual system before adoption and validate critical decisions with the original architecture evidence.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON diagnostics from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The learner script may persist call outcomes and notes to a local learned_patterns.json file in the skill scripts directory.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
