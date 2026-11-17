## Description:

Guides agents through minimal Java code changes, targeted tests, verification commands, and PR-ready summaries with evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanerilyazov](https://clawhub.ai/user/tanerilyazov)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to make Java feature, refactor, or bug-fix changes with minimal edits, targeted tests, verification commands, and a PR-ready summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to edit project files and run Java build or test commands.

Mitigation: Use it only in repositories where such edits and verification commands are expected, and review the reported changed files and command results.

Risk: A minimal Java change can miss behavior that is outside the provided acceptance criteria or targeted test scope.

Mitigation: Provide acceptance criteria, module context, build and test conventions, and whether integration tests are required before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tanerilyazov/skills/java-change-with-tests)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown summary with plan, changed files, commands, risks, and follow-ups]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records exact verification commands and results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
