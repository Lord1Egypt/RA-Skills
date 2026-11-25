## Description:

Defines test quality metrics, coverage thresholds, anti-patterns, and pytest configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to set testing quality gates and coverage targets, improve pytest suites, and apply reusable fixture and CI patterns. It provides checklists and examples for assessing test structure, coverage, maintainability, and reliability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial and marks the release suspicious because it found checks outside the stated testing-quality purpose and a Codecov upload in CI examples; this does not establish malicious intent.

Mitigation: Review the less clearly disclosed checks and Git repository helper before installing. For CI examples, check whether coverage data would leave the environment, especially for private or sensitive repositories.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/athola/skills/nm-leyline-testing-quality-standards)
- [Homepage listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with Python, shell, YAML, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reusable checklists, code examples, and configuration templates to adapt to the project.]

## Skill Version(s):

1.10.4 (source: ClawHub release metadata; artifact frontmatter reports 1.10.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
