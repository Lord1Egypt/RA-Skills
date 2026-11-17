## Description:

Reviews Go test code for proper table-driven tests, assertions, and coverage patterns. Use when reviewing *_test.go files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code reviewers use this skill to review Go test changes for table-driven structure, clear assertions, coverage gaps, parallel-safety, mocks, benchmarks, fuzz tests, HTTP handlers, and golden-file practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Golden-file update workflows can rewrite expected-output files.

Mitigation: Run update commands only for intentional fixture changes and review resulting golden-file diffs before accepting them.

Risk: The skill references a sibling review-verification protocol that may be absent in some installations.

Mitigation: Confirm the verification skill is installed or apply an equivalent pre-report verification checklist before reporting review findings.

## Reference(s):

- [Test Structure](artifact/references/structure.md)
- [Mocking](artifact/references/mocking.md)
- [ClawHub skill page](https://clawhub.ai/anderskev/skills/go-testing-code-review)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Structured Markdown review findings with file-line references and severity labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Go test commands for benchmark, fuzz, and golden-file update workflows when relevant.]

## Skill Version(s):

2.3.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
