## Description:

Verify Mode guides agents through checking completed work, running relevant tests or build checks, and reporting evidence-backed findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill after code changes or during bug investigation to define verification goals, inspect logic and edge cases, run tests, builds, or lint checks where available, and produce a concise verification report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run the target project's tests, build, or linter during verification.

Mitigation: Apply normal caution in untrusted repositories and review commands before execution.

Risk: A verification report may overstate confidence if tests are absent or only narrow checks were run.

Mitigation: Report the exact evidence gathered, unresolved assumptions, and remaining gaps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-openclaw-verify-mode)
- [Skill homepage](https://github.com/zhaobod1/huo15-openclaw-enhance)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown verification report with checklist, findings, test results, and conclusion]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands run, pass/fail counts, severity labels, suggested fixes, and remaining verification gaps.]

## Skill Version(s):

2.2.1 (source: server release metadata; artifact frontmatter lists 2.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
