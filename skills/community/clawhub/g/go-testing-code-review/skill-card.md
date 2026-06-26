## Description: <br>
Reviews Go test code for proper table-driven tests, assertions, and coverage patterns. Use when reviewing *_test.go files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code reviewers use this skill to review Go test changes for sound test structure, useful assertions, coverage of edge cases, and safe use of table-driven tests, mocks, benchmarks, fuzz tests, HTTP tests, and golden files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill references a separate review-verification-protocol skill for pre-report checks; if that skill is absent or untrusted, a reviewer may not apply the intended verification gate. <br>
Mitigation: Confirm the referenced review-verification-protocol skill is installed and trusted before relying on this skill's review workflow. <br>
Risk: Golden-file update patterns can overwrite expected-output files when a developer intentionally runs tests with an update flag. <br>
Mitigation: Review any suggested golden-file update workflow before execution and require intentional use of update flags. <br>


## Reference(s): <br>
- [Test Structure](references/structure.md) <br>
- [Mocking](references/mocking.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/anderskev/go-testing-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown review findings with file and line references, severity labels, and concise explanations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are gated by a required review sequence and pre-report verification checklist.] <br>

## Skill Version(s): <br>
2.3.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
