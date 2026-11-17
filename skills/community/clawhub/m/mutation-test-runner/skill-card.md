## Description:

Run mutation testing to measure real test suite effectiveness. Inject code mutations (flip conditions, remove calls, change returns), run tests against mutants, and report mutation score — the truest measure of test quality beyond line coverage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run mutation testing, identify surviving mutants, and improve weak or missing tests beyond line coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or invoke unpinned external mutation-testing tools.

Mitigation: Review and pin tool versions before use, especially in CI or shared development environments.

Risk: The skill may temporarily modify project source files while creating manual mutations.

Mitigation: Run it in a clean branch, disposable worktree, container, or CI sandbox and verify all mutations are reverted.

Risk: Third-party tools and test suites may run with access to local environment variables.

Mitigation: Keep credentials and sensitive tokens out of the environment while mutation tests and related tooling run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/mutation-test-runner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, code examples, and mutation testing report structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recommended tests for surviving mutants and baseline mutation score guidance.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
