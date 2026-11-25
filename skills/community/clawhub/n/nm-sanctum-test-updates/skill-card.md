## Description:

Updates, generates, and validates tests using git-workspace context and TDD/BDD methodology.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to find test gaps, generate or update test scaffolds, and validate tests after code changes using TDD and BDD practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation may run repository tests in the current Python process, and mutation testing may modify source files in place.

Mitigation: Review commands first, use an isolated disposable workspace, and inspect changes before keeping them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-sanctum-test-updates)
- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Analysis, Guidance]

**Output Format:** [Markdown guidance and summaries, generated test code and files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify test files and run test-validation workflows.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
