## Description:

Test-Driven Development assistant that generates Python test cases, runs pytest or unittest tests, reports coverage, and guides parts of the red-green-refactor cycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this local Python-focused TDD helper to generate starter tests, run tests, review coverage, and support a red-green-refactor workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation advertises Jest, Go, mutation testing, and full cycle features that the evidence identifies as incomplete.

Mitigation: Use the skill primarily for local Python TDD workflows and verify any non-Python, mutation, or cycle behavior before relying on it.

Risk: Test and coverage helpers use fixed report paths under /tmp, which can be unsuitable in multi-user or high-assurance environments.

Mitigation: Run in an isolated workspace or container and avoid shared temporary directories until report path handling is hardened.

Risk: Generated tests are starter code and may contain incorrect assumptions about expected behavior.

Mitigation: Review generated tests before committing them and run the project test suite after edits.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, CLI output, generated Python test code, and coverage summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated tests or reports to local files when the user provides output paths.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
