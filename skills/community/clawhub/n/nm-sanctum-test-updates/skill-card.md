## Description:

Updates, generates, and validates tests using git-workspace context and TDD/BDD methodology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to find test gaps, create and improve test scaffolding, and validate tests after code changes using TDD and BDD practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tests may run in the current process, and source files may remain changed if execution is interrupted.

Mitigation: Review the testing and mutation-testing guidance before use, and inspect the target repository's working tree after any interrupted run.

## Reference(s):

- [Project homepage (declared metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)
- [ClawHub skill release page](https://clawhub.ai/athola/skills/nm-sanctum-test-updates)
- [Publisher profile](https://clawhub.ai/user/athola)

## Skill Output:

**Output Type(s):** [Code, Files, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance and shell command examples; generated test code and scaffolding]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated tests may need developer review and completion before use.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
