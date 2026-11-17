## Description:

Defines test quality metrics, coverage thresholds, anti-patterns, and pytest config.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and test engineers use this skill to set coverage targets and test quality gates, review suites for reliability and maintainability, and apply pytest fixture and CI patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example CI workflow uploads coverage data to Codecov, which may not match every team's data handling or workflow requirements.

Mitigation: Review the workflow and confirm that external coverage uploads are approved before enabling it.

Risk: The skill includes Git fixture operations, and the server security guidance recommends checking that they suit the intended workflow.

Mitigation: Review the fixture commands and run them in an isolated temporary repository.

Risk: The security evidence notes that one reference could not be resolved, leaving the evidence incomplete.

Mitigation: Check relevant references and examples against current project requirements before adopting them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-leyline-testing-quality-standards)
- [Project homepage (Clawdis metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python, shell, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes testing quality checklists, coverage thresholds, and reusable pytest and CI examples.]

## Skill Version(s):

1.10.3 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
