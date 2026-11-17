## Description:

Runs autonomous iterative delivery loops for coding tasks using plan -> execute -> check -> review -> commit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[melonlee](https://clawhub.ai/user/melonlee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to run unattended, small-step coding delivery loops that decompose work, implement changes, run checks, review behavior, and commit each completed loop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to autonomously modify repository files and create commits.

Mitigation: Set explicit boundaries for files in scope, allowed checks, network use, and commit permission before enabling the workflow.

Risk: Automated implementation loops can propagate an incorrect plan if checks or review are incomplete.

Mitigation: Require engineering checks and browser or behavior review evidence before each commit, and stop or re-plan after repeated failures.

Risk: Research steps may use web or GitHub sources when technical choices are uncertain.

Mitigation: Define whether external research is allowed for the target codebase and record chosen sources in the decision log.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/melonlee/skills/hepha-skill)
- [Planning task decomposition](artifact/references/planning_task-decomposition.md)
- [Validation quality gates](artifact/references/validation_quality-gates.md)
- [Decomposition patterns](artifact/references/decomposition-patterns.md)
- [Progress visualization guide](artifact/references/progress-template.md)
- [Backlog template](artifact/templates/backlog.md)
- [Progress template](artifact/templates/progress.md)
- [Decision log template](artifact/templates/decision-log.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update .autopilot backlog, progress, and decision-log files, and may produce commit messages and validation summaries during execution.]

## Skill Version(s):

1.0.0 (source: release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
